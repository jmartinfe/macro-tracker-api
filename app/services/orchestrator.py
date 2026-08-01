from app.schemas.tracker import DailyTrackerState
from app.services.storage import load_daily_tracker_state, save_daily_tracker_state, delete_meal_entry, update_meal_entry, delete_old_states
from app.services.agent import run_agent

async def process_user_input(user_input: str, id: str) -> DailyTrackerState:
    """
    Process the user input and update the daily tracker state accordingly.

    Args:
        user_input (str): The user input string to be processed.
        id (str): The ID of the daily tracker state file to be modified.
        """
    # Load the current daily tracker state from storage
    current_state = load_daily_tracker_state(id=id)

    # Run the agent to process the user input and get the updated state
    updated_state = run_agent(user_input, current_state)

    # Save the updated state back to storage
    save_daily_tracker_state(updated_state, id=id)

    return updated_state

async def delete_meal(meal_id: str, id: str) -> DailyTrackerState:
    """
    Delete a meal entry from the daily tracker state.

    Args:
        meal_id (str): The ID of the meal entry to be deleted.
        id (str): The ID of the daily tracker state file to be modified.

    Returns:
        DailyTrackerState: The updated daily tracker state after deleting the meal entry.
    """
    deleted_state = delete_meal_entry(meal_id, id=id)

    # Save the updated state back to storage
    save_daily_tracker_state(deleted_state, id=id)

    return deleted_state

async def update_meal(updated_meal, id: str) -> DailyTrackerState:
    """
    Update a meal entry in the daily tracker state.

    Args:
        updated_meal: The updated meal data.
        id (str): The ID of the daily tracker state file to be modified.

    Returns:
        DailyTrackerState: The updated daily tracker state after updating the meal entry.
    """
    updated_state = update_meal_entry(updated_meal, id=id)

    # Save the updated state back to storage
    save_daily_tracker_state(updated_state, id=id)

    return updated_state

async def clean_old_states():
    """
    Delete old daily tracker state files that are not for today.
    This function checks the data directory for any JSON files representing
    daily tracker states and removes those that are not for the current date.
    """
    delete_old_states()