from datetime import date
import os
from fastapi import APIRouter, HTTPException, Security, status, Header, Depends
from fastapi.security import APIKeyHeader
from app.core.exceptions import AppError, InvalidInputError
from app.core.logging import get_logger
from app.schemas.tracker import MealItem, ProcessInputRequest, DailyTrackerState
from app.services.storage import load_daily_tracker_state
from app.services.orchestrator import process_user_input, clean_old_states, delete_meal as orchestrator_delete_meal, update_meal as orchestrator_update_meal

logger = get_logger(__name__)
router = APIRouter(prefix="/tracker", tags=["Tracker"])

API_KEY = os.getenv("API_KEY")
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key():
    """
    Retrieve the API key from environment variables.
    Raises an exception if the API key is not set.
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        logger.error("API_KEY environment variable is not set.")
        raise RuntimeError("API_KEY environment variable is not set.")
    return api_key

def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    if not api_key:
        logger.warning("Missing API Key in request headers.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: API Key required"
        )
    valid_key = get_api_key()
    if api_key != valid_key:
        logger.warning("Invalid API Key provided", extra={"provided_key": api_key})
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Invalid API Key"
        )
    logger.info("API Key verified successfully")
    return api_key

# Health check endpoint
@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint to verify that the API is running.
    """
    logger.info("Health check requested")
    return {"status": "ok"}

# Retrieve the current daily tracker state
@router.get("/daily_tracker_state/{id}", response_model=DailyTrackerState, status_code=status.HTTP_200_OK)
async def get_daily_tracker_state_by_id(id: str, input_date: date = date.today(), api_key: str = Depends(verify_api_key)):
    """
    Retrieve the current daily tracker state based on the provided ID.
    
    Args:
        id (str): The ID of the daily tracker state file to be retrieved.
        input_date (date): The date for which to load the tracker state.
    
    Returns:
        DailyTrackerState: The current daily tracker state for the specified ID.
    """
    logger.info("Loading daily tracker state for id=%s", id)
    try:
        state = load_daily_tracker_state(id=id, input_date=input_date)
        return state
    except Exception as e:
        logger.exception("Failed to load daily tracker state for id=%s", id)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Process user input and update the daily tracker state
@router.post("/process_input", response_model=DailyTrackerState, status_code=status.HTTP_200_OK)
async def process_input(request: ProcessInputRequest, api_key: str = Depends(verify_api_key)):
    """
    Process user input and update the daily tracker state accordingly.
    
    Args:
        request (ProcessInputRequest): The request body containing user input and current tracker state.
        api_key (str): The API key for authentication.
    
    Returns:
        DailyTrackerState: The updated daily tracker state after processing the input.
    """
    if not request.user_input.strip():
        logger.warning("Received empty user input for id=%s", request.id)
        raise InvalidInputError("User input cannot be empty.")

    logger.info("Processing user input for id=%s", request.id)
    try:
        updated_state = await process_user_input(request.user_input, id=request.id, input_date=request.input_date)
        logger.info("Processed user input for id=%s", request.id)
        return updated_state
    except AppError:
        raise
    except Exception as e:
        logger.exception("Failed to process input for id=%s", request.id)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Delete meal entry from the daily tracker state
@router.delete("/delete_meal_entry", response_model=DailyTrackerState, status_code=status.HTTP_200_OK)
async def delete_meal(meal_id: str, id: str, input_date: date = date.today(), api_key: str = Depends(verify_api_key)):
    """
    Delete a meal entry from the daily tracker state.
    
    Args:
        meal_id (str): The ID of the meal entry to be deleted.
        id (str): The ID of the daily tracker state file to be modified.
        input_date (date): The date for which to load the tracker state.
        api_key (str): The API key for authentication.
    
    Returns:
        DailyTrackerState: The updated daily tracker state after deleting the meal entry.
    """
    logger.info("Deleting meal entry meal_id=%s for id=%s", meal_id, id)
    try:
        deleted_state = await orchestrator_delete_meal(meal_id, id=id, input_date=input_date)
        logger.info("Deleted meal entry meal_id=%s for id=%s", meal_id, id)
        return deleted_state
    except AppError:
        raise
    except Exception as e:
        logger.exception("Failed to delete meal entry meal_id=%s for id=%s", meal_id, id)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Update meal entry in the daily tracker state
@router.put("/update_meal_entry", response_model=DailyTrackerState, status_code=status.HTTP_200_OK)
async def update_meal(updated_meal: MealItem, id: str, input_date: date = date.today(), api_key: str = Depends(verify_api_key)):
    """
    Update a meal entry in the daily tracker state.
    
    Args:
        updated_meal: The updated meal data.
        id (str): The ID of the daily tracker state file to be modified.
        input_date (date): The date for which to load the tracker state.
        api_key (str): The API key for authentication.
    
    Returns:
        DailyTrackerState: The updated daily tracker state after updating the meal entry.
    """
    logger.info("Updating meal entry id=%s meal_id=%s", id, updated_meal.id)
    try:
        updated_state = await orchestrator_update_meal(updated_meal, id=id, input_date=input_date)
        logger.info("Updated meal entry id=%s meal_id=%s", id, updated_meal.id)
        return updated_state
    except AppError:
        raise
    except Exception as e:
        logger.exception("Failed to update meal entry id=%s meal_id=%s", id, updated_meal.id)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Clean old daily tracker state files
@router.delete("/clean_old_states", status_code=status.HTTP_200_OK)
async def clean_old_states_endpoint(input_date: date = date.today(), api_key: str = Depends(verify_api_key)):
    """
    Delete old daily tracker state files that are not for today.
    This endpoint checks the data directory for any JSON files representing
    daily tracker states and removes those that are not for the current date.
    """
    logger.info("Cleaning old tracker state files")
    try:
        await clean_old_states(input_date=input_date)
        logger.info("Cleaned old tracker state files successfully")
        return {"status": "Old daily tracker state files cleaned successfully."}
    except AppError:
        raise
    except Exception as e:
        logger.exception("Failed to clean old tracker state files")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    