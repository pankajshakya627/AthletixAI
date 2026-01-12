"""Training program models."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class MuscleGroup(str, Enum):
    """Target muscle groups."""
    CHEST = "chest"
    BACK = "back"
    SHOULDERS = "shoulders"
    BICEPS = "biceps"
    TRICEPS = "triceps"
    FOREARMS = "forearms"
    CORE = "core"
    QUADS = "quads"
    HAMSTRINGS = "hamstrings"
    GLUTES = "glutes"
    CALVES = "calves"
    FULL_BODY = "full_body"


class ExerciseType(str, Enum):
    """Type of exercise."""
    COMPOUND = "compound"
    ISOLATION = "isolation"
    CARDIO = "cardio"
    MOBILITY = "mobility"
    PLYOMETRIC = "plyometric"


class Exercise(BaseModel):
    """Individual exercise in a workout."""
    
    name: str = Field(description="Exercise name")
    exercise_type: ExerciseType = Field(
        default=ExerciseType.COMPOUND,
        description="Type of exercise"
    )
    target_muscles: list[MuscleGroup] = Field(
        default_factory=list,
        description="Primary muscles targeted"
    )
    sets: int = Field(ge=1, le=10, description="Number of sets")
    reps: str = Field(description="Rep range (e.g., '8-12', '5', 'AMRAP')")
    rest_seconds: int = Field(
        default=90,
        ge=0,
        le=300,
        description="Rest period between sets in seconds"
    )
    weight_suggestion: Optional[str] = Field(
        default=None,
        description="Weight suggestion (e.g., 'RPE 7', '70% 1RM')"
    )
    technique_cues: list[str] = Field(
        default_factory=list,
        description="Form and technique cues"
    )
    alternatives: list[str] = Field(
        default_factory=list,
        description="Alternative exercises if equipment unavailable"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional exercise notes"
    )
    
    # NEW: Educational resources from research agent
    tutorial_url: Optional[str] = Field(
        default=None,
        description="URL to tutorial or guide"
    )
    gif_url: Optional[str] = Field(
        default=None,
        description="URL to animated GIF demonstration"
    )
    video_url: Optional[str] = Field(
        default=None,
        description="URL to video tutorial (YouTube, etc.)"
    )
    image_urls: list[str] = Field(
        default_factory=list,
        description="URLs to reference images showing proper form"
    )
    breathing_guide: Optional[str] = Field(
        default=None,
        description="Instructions for breathing during the exercise"
    )
    common_mistakes: list[str] = Field(
        default_factory=list,
        description="Common mistakes to avoid"
    )


class DailyWorkout(BaseModel):
    """Single day's workout plan."""
    
    day_number: int = Field(ge=1, le=7, description="Day of the week (1=Monday)")
    day_name: str = Field(description="Descriptive name (e.g., 'Push Day', 'Upper Body')")
    focus: str = Field(description="Primary focus of the workout")
    exercises: list[Exercise] = Field(
        default_factory=list,
        description="List of exercises"
    )
    warmup_notes: str = Field(
        default="5-10 minutes light cardio and dynamic stretching",
        description="Warmup instructions"
    )
    cooldown_notes: str = Field(
        default="5 minutes stretching",
        description="Cooldown instructions"
    )
    estimated_duration_minutes: int = Field(
        default=60,
        ge=15,
        le=180,
        description="Estimated workout duration"
    )
    intensity_level: str = Field(
        default="moderate",
        description="Overall intensity level"
    )
    is_rest_day: bool = Field(
        default=False,
        description="Whether this is a rest/recovery day"
    )
    
    @property
    def total_sets(self) -> int:
        """Calculate total sets in workout."""
        return sum(ex.sets for ex in self.exercises)


class WeeklySchedule(BaseModel):
    """One week of workouts."""
    
    week_number: int = Field(ge=1, description="Week number in the program")
    workouts: list[DailyWorkout] = Field(
        default_factory=list,
        description="Daily workouts for the week"
    )
    weekly_volume_target: Optional[int] = Field(
        default=None,
        description="Target total sets for the week"
    )
    intensity_modifier: int = Field(
        default=0,
        ge=-50,
        le=20,
        description="Intensity adjustment based on recovery"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Week-specific notes"
    )


class ProgressionRule(BaseModel):
    """Rule for progressing exercises over time."""
    
    rule_type: str = Field(description="Type of progression (e.g., 'linear', 'double_progression')")
    condition: str = Field(description="When to apply progression")
    action: str = Field(description="What to increase (e.g., 'add 2.5kg', 'add 1 rep')")


class TrainingProgram(BaseModel):
    """Complete training program."""
    
    program_name: str = Field(description="Name of the program")
    program_length_weeks: int = Field(
        ge=1,
        le=52,
        description="Total program length in weeks"
    )
    weekly_split: str = Field(
        description="Training split (e.g., 'Push/Pull/Legs', 'Upper/Lower', 'Full Body')"
    )
    weekly_schedules: list[WeeklySchedule] = Field(
        default_factory=list,
        description="Weekly workout schedules"
    )
    progression_rules: list[ProgressionRule] = Field(
        default_factory=list,
        description="Rules for progressing over time"
    )
    deload_frequency: Optional[int] = Field(
        default=4,
        description="Deload every N weeks"
    )
    equipment_required: list[str] = Field(
        default_factory=list,
        description="Equipment needed for the program"
    )
    difficulty_level: str = Field(
        default="intermediate",
        description="Overall program difficulty"
    )
    goals_addressed: list[str] = Field(
        default_factory=list,
        description="Fitness goals this program targets"
    )
    notes: Optional[str] = Field(
        default=None,
        description="General program notes and guidelines"
    )
    
    @property
    def current_week(self) -> Optional[WeeklySchedule]:
        """Get the first week schedule (for display purposes)."""
        return self.weekly_schedules[0] if self.weekly_schedules else None
