"""
Session models for workout tracking.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid


class WorkoutSession(BaseModel):
    """Represents a single workout session."""
    
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    session_date: datetime = Field(default_factory=datetime.now)
    exercises_completed: list[dict] = Field(default_factory=list)
    notes: Optional[str] = None
    fatigue_level: Optional[int] = Field(None, ge=1, le=10)
    performance_rating: Optional[int] = Field(None, ge=1, le=10)
    completed: bool = False
    
    def add_exercise(self, exercise_data: dict) -> None:
        """Add completed exercise to session."""
        self.exercises_completed.append(exercise_data)
    
    def mark_complete(self) -> None:
        """Mark session as completed."""
        self.completed = True


class SessionSummary(BaseModel):
    """Summary of a workout session for history."""
    
    session_id: str
    session_date: datetime
    total_exercises: int
    total_sets: int
    fatigue_level: Optional[int] = None
    performance_rating: Optional[int] = None
