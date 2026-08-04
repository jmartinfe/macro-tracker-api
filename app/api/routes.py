import traceback

from fastapi import APIRouter, HTTPException, status
from app.schemas.tracker import MealItem, ProcessInputRequest, DailyTrackerState
from app.services.storage import load_daily_tracker_state
from app.services.orchestrator import process_user_input, clean_old_states,delete_meal as orchestrator_delete_meal, update_meal as orchestrator_update_meal

router = APIRouter(prefix="/tracker", tags=["Tracker"])

# Health check endpoint
@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint to verify that the API is running.
    """
    return {"status": "ok"}

# Retrieve the current daily tracker state
@router.get("/daily_tracker_state/{id}", response_model=DailyTrackerState, status_code=status.HTTP_200_OK)
async def get_daily_tracker_state_by_id(id: str):
    """
    Retrieve the current daily tracker state based on the provided ID.
    
    Args:
        id (str): The ID of the daily tracker state file to be retrieved.
    
    Returns:
        DailyTrackerState: The current daily tracker state for the specified ID.
    """
    try:
        state = load_daily_tracker_state(id=id)
        return state
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Process user input and update the daily tracker state
@router.post("/process_input", response_model=DailyTrackerState, status_code=status.HTTP_200_OK)
async def process_input(request: ProcessInputRequest):
    """
    Process user input and update the daily tracker state accordingly.
    
    Args:
        request (ProcessInputRequest): The request body containing user input and current tracker state.
    
    Returns:
        DailyTrackerState: The updated daily tracker state after processing the input.
    """
    
    if not request.user_input.strip():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User input cannot be empty.")
    try:
        updated_state = await process_user_input(request.user_input, id=request.id)
        return updated_state
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Delete meal entry from the daily tracker state
@router.delete("/delete_meal_entry", response_model=DailyTrackerState, status_code=status.HTTP_200_OK)
async def delete_meal(meal_id: str, id: str):
    """
    Delete a meal entry from the daily tracker state.
    
    Args:
        meal_id (str): The ID of the meal entry to be deleted.
        id (str): The ID of the daily tracker state file to be modified.
    
    Returns:
        DailyTrackerState: The updated daily tracker state after deleting the meal entry.
    """
    try:
        deleted_state = await orchestrator_delete_meal(meal_id, id=id)
        return deleted_state
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Update meal entry in the daily tracker state
@router.put("/update_meal_entry", response_model=DailyTrackerState, status_code=status.HTTP_200_OK)
async def update_meal(updated_meal: MealItem, id: str):
    """
    Update a meal entry in the daily tracker state.
    
    Args:
        updated_meal: The updated meal data.
        id (str): The ID of the daily tracker state file to be modified.
    
    Returns:
        DailyTrackerState: The updated daily tracker state after updating the meal entry.
    """
    try:
        updated_state = await orchestrator_update_meal(updated_meal, id=id)
        return updated_state
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Clean old daily tracker state files
@router.delete("/clean_old_states", status_code=status.HTTP_200_OK)
async def clean_old_states_endpoint():
    """
    Delete old daily tracker state files that are not for today.
    This endpoint checks the data directory for any JSON files representing
    daily tracker states and removes those that are not for the current date.
    """
    try:
        await clean_old_states()
        return {"status": "Old daily tracker state files cleaned successfully."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    