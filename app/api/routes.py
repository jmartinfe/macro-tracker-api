from fastapi import APIRouter, HTTPException, status
from app.schemas.tracker import ProcessInputRequest, DailyTrackerState
from app.services.storage import load_daily_tracker_state
from app.services.orchestrator import process_user_input

router = APIRouter(prefix="/tracker", tags=["Tracker"])

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint to verify that the API is running.
    """
    return {"status": "ok"}

@router.get("/daily_tracker_state", response_model=DailyTrackerState, status_code=status.HTTP_200_OK)
async def get_daily_tracker_state():
    """
    Retrieve the current daily tracker state.
    
    Returns:
        DailyTrackerState: The current daily tracker state.
    """
    try:
        state = load_daily_tracker_state()
        return state
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

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
        updated_state = await process_user_input(request.user_input)    
        return updated_state
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))