from fastapi import APIRouter, status
from app.schemas.tracker import ProcessInputRequest, DailyTrackerState

router = APIRouter(prefix="/tracker", tags=["Tracker"])

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint to verify that the API is running.
    """
    return {"status": "ok"}

@router.post("/process_input", response_model=DailyTrackerState, status_code=status.HTTP_200_OK)
async def process_input(request: ProcessInputRequest):
    """
    Process user input and update the daily tracker state accordingly.
    
    Args:
        request (ProcessInputRequest): The request body containing user input and current tracker state.
    
    Returns:
        DailyTrackerState: The updated daily tracker state after processing the input.
    """
    # Placeholder for processing logic
    # In a real implementation, you would parse the user_input, update the current_state,
    # and return the updated state. For now, we will just return the current state.
    
    return request.current_state