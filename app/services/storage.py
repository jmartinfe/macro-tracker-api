from datetime import date
from pathlib import Path
from app.schemas.tracker import DailyTrackerState, MacroGoals

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
FILE_PATH = DATA_DIR / "daily_tracker_state.json"

def _ensure_data_dir_exists():
    """
    Ensure that the data directory exists. If it does not exist, create it.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_daily_tracker_state() -> DailyTrackerState:
    """
    Load the daily tracker state from a JSON file. If the file does not exist,
    return a default DailyTrackerState with today's date and default macro goals.
    
    Returns:
        DailyTrackerState: The loaded or default daily tracker state.
    """
    _ensure_data_dir_exists()
    
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
            save_daily_tracker_state(fallback_state)
            return fallback_state
        except Exception as save_error:
            raise RuntimeError(f"{error_message}. Additionally, failed to save fallback state: {str(save_error)}")

def save_daily_tracker_state(state: DailyTrackerState):
    """
    Save the daily tracker state to a JSON file.
    
    Args:
        state (DailyTrackerState): The daily tracker state to be saved.
    """
    try:
        _ensure_data_dir_exists()
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            file.write(state.model_dump_json(indent=2))
    except Exception as e:
        raise IOError(f"Error saving daily tracker state: {str(e)}")