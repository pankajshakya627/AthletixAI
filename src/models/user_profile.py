"""User profile, food preferences, and fitness goals models."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ExperienceLevel(str, Enum):
    """User's fitness experience level."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    ELITE = "elite"


class Gender(str, Enum):
    """User's gender for fitness calculations."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Language(str, Enum):
    """User's preferred language for responses."""
    ENGLISH = "english"
    HINDI = "hindi"
    HINGLISH = "hinglish"  # Hindi-English mix


class DietaryRestriction(str, Enum):
    """Common dietary restrictions."""
    NONE = "none"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    PESCATARIAN = "pescatarian"
    HALAL = "halal"
    KOSHER = "kosher"
    GLUTEN_FREE = "gluten_free"
    DAIRY_FREE = "dairy_free"
    KETO = "keto"
    PALEO = "paleo"


class FoodPreferences(BaseModel):
    """User's food preferences and dietary requirements."""
    
    dietary_restrictions: list[DietaryRestriction] = Field(
        default_factory=lambda: [DietaryRestriction.NONE],
        description="List of dietary restrictions"
    )
    allergies: list[str] = Field(
        default_factory=list,
        description="Food allergies (e.g., 'peanuts', 'shellfish')"
    )
    cuisine_preferences: list[str] = Field(
        default_factory=list,
        description="Preferred cuisines (e.g., 'Mediterranean', 'Asian')"
    )
    disliked_foods: list[str] = Field(
        default_factory=list,
        description="Foods the user dislikes"
    )
    meal_frequency: int = Field(
        default=3,
        ge=1,
        le=6,
        description="Number of meals per day"
    )
    calorie_target: Optional[int] = Field(
        default=None,
        ge=1000,
        le=6000,
        description="Daily calorie target"
    )
    protein_target_g: Optional[float] = Field(
        default=None,
        description="Daily protein target in grams"
    )
    carbs_target_g: Optional[float] = Field(
        default=None,
        description="Daily carbohydrates target in grams"
    )
    fats_target_g: Optional[float] = Field(
        default=None,
        description="Daily fats target in grams"
    )


class FitnessGoals(BaseModel):
    """User's fitness goals and objectives."""
    
    primary_goal: str = Field(
        default="general_fitness",
        description="Primary fitness goal (e.g., 'muscle_gain', 'fat_loss', 'strength')"
    )
    secondary_goals: list[str] = Field(
        default_factory=list,
        description="Secondary fitness goals"
    )
    target_weight_kg: Optional[float] = Field(
        default=None,
        description="Target body weight in kg"
    )
    weekly_workout_days: int = Field(
        default=3,
        ge=1,
        le=7,
        description="Target workout days per week"
    )
    session_duration_minutes: int = Field(
        default=60,
        ge=15,
        le=180,
        description="Target workout session duration"
    )


class UserProfile(BaseModel):
    """Complete user profile for the fitness coach."""
    
    user_id: str = Field(description="Unique user identifier")
    name: str = Field(description="User's name")
    age: int = Field(ge=13, le=100, description="User's age")
    gender: Gender = Field(description="User's gender")
    height_cm: float = Field(ge=100, le=250, description="Height in centimeters")
    weight_kg: float = Field(ge=30, le=300, description="Weight in kilograms")
    experience_level: ExperienceLevel = Field(
        default=ExperienceLevel.BEGINNER,
        description="Fitness experience level"
    )
    injury_history: list[str] = Field(
        default_factory=list,
        description="Past injuries to consider (e.g., 'lower back', 'right knee')"
    )
    current_injuries: list[str] = Field(
        default_factory=list,
        description="Current active injuries"
    )
    
    # NEW: Language preference
    preferred_language: Language = Field(
        default=Language.ENGLISH,
        description="Preferred language for responses (English, Hindi, Hinglish)"
    )

    equipment_available: list[str] = Field(
        default_factory=list,
        description="Available equipment (e.g., 'dumbbells', 'barbell', 'pull_up_bar')"
    )
    medical_conditions: list[str] = Field(
        default_factory=list,
        description="Medical conditions to consider"
    )
    
    @property
    def bmi(self) -> float:
        """Calculate Body Mass Index."""
        height_m = self.height_cm / 100
        return round(self.weight_kg / (height_m ** 2), 1)
