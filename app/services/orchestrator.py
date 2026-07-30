from app.schemas.tracker import DailyTrackerState
from app.services.storage import load_daily_tracker_state, save_daily_tracker_state
from app.services.agent import run_agent

async def process_user_input(user_input: str) -> DailyTrackerState:
    """
    Process the user input and update the daily tracker state accordingly.

    Args:
        user_input (str): The user input string to be processed.
        """
    # Load the current daily tracker state from storage
    current_state = load_daily_tracker_state()

    # Run the agent to process the user input and get the updated state
    updated_state = run_agent(user_input, current_state)

    # Save the updated state back to storage
    save_daily_tracker_state(updated_state)

    return updated_state
