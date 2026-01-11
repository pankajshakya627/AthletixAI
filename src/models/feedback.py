"""Feedback and adaptation models."""

from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class PerformanceTrend(str, Enum):
    """Performance trend direction."""
    DECLINING = "declining"
    STAGNANT = "stagnant"
    IMPROVING = "improving"
    RAPID_IMPROVEMENT = "rapid_improvement"


class AdaptationAction(str, Enum):
    """Actions the adaptation agent can take."""
    REDUCE_VOLUME = "reduce_volume"
    REDUCE_INTENSITY = "reduce_intensity"
    MAINTAIN = "maintain"
    INCREASE_VOLUME = "increase_volume"
    INCREASE_INTENSITY = "increase_intensity"
    DELOAD = "deload"
    CHANGE_EXERCISES = "change_exercises"


class SessionFeedback(BaseModel):
    """Feedback from a single workout session."""
    
    session_date: datetime = Field(default_factory=datetime.now)
    workout_completed: bool = Field(default=True)
    completion_percentage: int = Field(
        default=100,
        ge=0,
        le=100,
        description="Percentage of workout completed"
    )
    perceived_difficulty: int = Field(
        ge=1,
        le=10,
        description="Rate of Perceived Exertion (1-10)"
    )
    energy_level: int = Field(
        ge=1,
        le=10,
        description="Pre-workout energy level"
    )
    notes: Optional[str] = Field(default=None)


class WeeklyFeedback(BaseModel):
    """Weekly feedback aggregation for adaptation decisions."""
    
    week_number: int = Field(ge=1, description="Week number in program")
    session_feedbacks: list[SessionFeedback] = Field(
        default_factory=list,
        description="Individual session feedbacks"
    )
    
    # Aggregated metrics
    performance_trend: PerformanceTrend = Field(
        default=PerformanceTrend.STAGNANT,
        description="Overall performance trend"
    )
    adherence_rate: float = Field(
        default=1.0,
        ge=0,
        le=1,
        description="Workout adherence rate (0-1)"
    )
    average_rpe: float = Field(
        default=7.0,
        ge=1,
        le=10,
        description="Average perceived exertion"
    )
    average_energy: float = Field(
        default=7.0,
        ge=1,
        le=10,
        description="Average energy level"
    )
    fatigue_accumulation: str = Field(
        default="normal",
        description="Fatigue accumulation level"
    )
    
    # Adaptation decision
    needs_adjustment: bool = Field(
        default=False,
        description="Whether program needs adjustment"
    )
    recommended_action: AdaptationAction = Field(
        default=AdaptationAction.MAINTAIN,
        description="Recommended adaptation action"
    )
    adjustment_reason: Optional[str] = Field(
        default=None,
        description="Reason for recommended adjustment"
    )
    
    # Progress metrics
    strength_progress: dict[str, float] = Field(
        default_factory=dict,
        description="Strength progress per exercise (%)"
    )
    body_metrics_change: dict[str, float] = Field(
        default_factory=dict,
        description="Body composition changes"
    )
    
    def calculate_metrics(self) -> None:
        """Calculate aggregated metrics from session feedbacks."""
        if not self.session_feedbacks:
            return
        
        completed = sum(1 for s in self.session_feedbacks if s.workout_completed)
        self.adherence_rate = completed / len(self.session_feedbacks)
        
        self.average_rpe = sum(s.perceived_difficulty for s in self.session_feedbacks) / len(self.session_feedbacks)
        self.average_energy = sum(s.energy_level for s in self.session_feedbacks) / len(self.session_feedbacks)
        
        # Determine if adjustment needed
        if self.adherence_rate < 0.7:
            self.needs_adjustment = True
            self.recommended_action = AdaptationAction.REDUCE_VOLUME
            self.adjustment_reason = "Low adherence - reducing volume to improve consistency"
        elif self.average_rpe > 8.5:
            self.needs_adjustment = True
            self.recommended_action = AdaptationAction.REDUCE_INTENSITY
            self.adjustment_reason = "High perceived difficulty - reducing intensity"
        elif self.average_energy < 4:
            self.needs_adjustment = True
            self.recommended_action = AdaptationAction.DELOAD
            self.adjustment_reason = "Low energy levels - recommending deload week"
