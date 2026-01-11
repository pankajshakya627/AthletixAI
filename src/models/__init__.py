"""Pydantic models for the fitness coach system."""

from src.models.user_profile import UserProfile, FoodPreferences, FitnessGoals
from src.models.assessment import MovementAssessment
from src.models.wearables import WearableMetrics
from src.models.nutrition import FoodItem, MealAnalysis, NutritionAnalysis, DailyMacros
from src.models.program import Exercise, DailyWorkout, TrainingProgram
from src.models.feedback import WeeklyFeedback

__all__ = [
    "UserProfile",
    "FoodPreferences",
    "FitnessGoals",
    "MovementAssessment",
    "WearableMetrics",
    "FoodItem",
    "MealAnalysis",
    "NutritionAnalysis",
    "DailyMacros",
    "Exercise",
    "DailyWorkout",
    "TrainingProgram",
    "WeeklyFeedback",
]
