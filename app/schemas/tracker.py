from datetime import date
from pydantic import BaseModel, Field
from typing import List

class MacroGoals(BaseModel):
    calories: int = Field(default = 2200, description="The daily calorie goal")
    protein: int = Field(default = 150, description="The daily protein goal in grams")
    carbs: int = Field(default = 200, description="The daily carbohydrate goal in grams")
    fats: int = Field(default = 100, description="The daily fat goal in grams")

class MealItem(BaseModel):
    id: str = Field(..., description="The unique identifier for the meal item")
    name: str = Field(..., description="The name of the meal item")
    calories: int = Field(..., description="The calorie content of the meal item")
    protein: int = Field(..., description="The protein content of the meal item in grams")
    carbs: int = Field(..., description="The carbohydrate content of the meal item in grams")
    fats: int = Field(..., description="The fat content of the meal item in grams")

class DailyTrackerState(BaseModel):
    current_date: date = Field(..., description="The date for the daily tracker state in YYYY-MM-DD format")
    macro_goals: MacroGoals = Field(..., description="The macro goals for the day")
    meals: List[MealItem] = Field(default_factory=list, description="A list of meal items consumed during the day")
    total_calories: int = Field(default=0, description="The total calories consumed during the day")
    total_protein: int = Field(default=0, description="The total protein consumed during the day in grams")
    total_carbs: int = Field(default=0, description="The total carbohydrates consumed during the day in grams")
    total_fats: int = Field(default=0, description="The total fats consumed during the day in grams")

class ProcessInputRequest(BaseModel):
    id: str = Field(..., description="The ID of the daily tracker state file to be modified")
    input_date: date = Field(..., description="The date for which to load the tracker state")
    user_input: str = Field(..., description="The user input string to be processed")