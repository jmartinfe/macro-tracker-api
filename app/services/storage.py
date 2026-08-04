from datetime import date, timedelta
from pathlib import Path
from app.schemas.tracker import DailyTrackerState, MacroGoals, MealItem

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
FILE_NAME = "daily_tracker_state.json"

def _ensure_data_dir_exists():
    """
    Ensure that the data directory exists. If it does not exist, create it.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_daily_tracker_state(id: str) -> DailyTrackerState:
    """
    Load the daily tracker state from a JSON file. If the file does not exist,
    return a default DailyTrackerState with today's date and default macro goals.
    
    Returns:
        DailyTrackerState: The loaded or default daily tracker state.
    """
    _ensure_data_dir_exists()

    FILE_PATH = DATA_DIR / f"daily_tracker_state_{id}.json"

    if not FILE_PATH.exists():
        # Return a default state if the file does not exist
        return DailyTrackerState(
            current_date=date.today(),
            macro_goals=MacroGoals(),
            meals=[],
            total_calories=0,
            total_protein=0,
            total_carbs=0,
            total_fats=0
        )

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data = file.read()        

        # If the loaded state is not for today, reset to default
        state = DailyTrackerState.model_validate_json(data)
        
        if state.current_date < date.today():            
            return DailyTrackerState(
                current_date=date.today(),
                macro_goals=MacroGoals(),
                meals=[],
                total_calories=0,
                total_protein=0,
                total_carbs=0,
                total_fats=0
            )
        return state
    
    except Exception as e:
        error_message = f"Error loading daily tracker state: {str(e)}"
        try:
            fallback_state = DailyTrackerState(
                current_date=date.today(),
                macro_goals=MacroGoals(),
                meals=[],
                total_calories=0,
                total_protein=0,
                total_carbs=0,
                total_fats=0
            )
            save_daily_tracker_state(fallback_state, id=id)
            return fallback_state
        except Exception as save_error:
            raise RuntimeError(f"{error_message}. Additionally, failed to save fallback state: {str(save_error)}")

def save_daily_tracker_state(state: DailyTrackerState, id: str = None):
    """
    Save the daily tracker state to a JSON file.
    
    Args:
        state (DailyTrackerState): The daily tracker state to be saved.
    """
    try:
        _ensure_data_dir_exists()
        if id:
            FILE_PATH = DATA_DIR / f"daily_tracker_state_{id}.json"
        else:
            FILE_PATH = DATA_DIR / "daily_tracker_state.json"
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            file.write(state.model_dump_json(indent=2))
    except Exception as e:
        raise IOError(f"Error saving daily tracker state: {str(e)}")

def delete_meal_entry(meal_id: str, id: str) -> DailyTrackerState:
    """
    Delete a meal entry from the daily tracker state by its ID.
    
    Args:
        meal_id (str): The ID of the meal entry to be deleted.
        id (str): The ID of the daily tracker state file to be modified.
    
    Returns:
        DailyTrackerState: The updated daily tracker state after deleting the meal entry.
    """
    state = load_daily_tracker_state(id=id)
    state.meals = [meal for meal in state.meals if meal.id != meal_id]
    update_state_totals(state)
    save_daily_tracker_state(state, id=id)
    return state

def update_meal_entry(updated_meal: MealItem, id: str) -> DailyTrackerState:
    """
    Update a meal entry in the daily tracker state by its ID.
    
    Args:
        updated_meal (MealItem): The updated meal data.
        id (str): The ID of the daily tracker state file to be modified.
    
    Returns:
        DailyTrackerState: The updated daily tracker state after updating the meal entry.
    """
    state = load_daily_tracker_state(id=id)
    for i, meal in enumerate(state.meals):
        if meal.id == updated_meal.id:
            state.meals[i] = updated_meal
            break
    update_state_totals(state)
    save_daily_tracker_state(state, id=id)
    return state

def update_state_totals(state: DailyTrackerState) -> DailyTrackerState:
    """
    Update the total calories, protein, carbs, and fats in the daily tracker state
    based on the current meals.
    
    Args:
        state (DailyTrackerState): The daily tracker state to be updated.
    
    Returns:
        DailyTrackerState: The updated daily tracker state with recalculated totals.
    """
    state.total_calories = sum(meal.calories for meal in state.meals)
    state.total_protein = sum(meal.protein for meal in state.meals)
    state.total_carbs = sum(meal.carbs for meal in state.meals)
    state.total_fats = sum(meal.fats for meal in state.meals)
    return state

def delete_old_states():
    """
    Delete old daily tracker state files that are not for today or yesterday.
    This function checks the data directory for any JSON files representing
    daily tracker states and removes those that are not for the current date.
    """
    _ensure_data_dir_exists()
    for file in DATA_DIR.glob("daily_tracker_state*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                state = DailyTrackerState.model_validate_json(f.read())
                if state.current_date < date.today() - timedelta(days=1):
                    file.unlink()  # Delete the old state file
        except Exception as e:
            print(f"Error processing file {file}: {str(e)}")