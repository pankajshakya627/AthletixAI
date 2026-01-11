"""Wearable device metrics models."""

from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class RecoveryStatus(str, Enum):
    """Recovery status levels."""
    POOR = "poor"
    LOW = "low"
    MODERATE = "moderate"
    GOOD = "good"
    OPTIMAL = "optimal"


class FatigueLevel(str, Enum):
    """Fatigue level assessment."""
    MINIMAL = "minimal"
    LOW = "low"
    MODERATE = "moderate"
    ELEVATED = "elevated"
    HIGH = "high"


class SleepQuality(str, Enum):
    """Sleep quality assessment."""
    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"


class WearableMetrics(BaseModel):
    """Metrics collected from wearable devices."""
    
    # Heart Rate Metrics
    resting_heart_rate: Optional[int] = Field(
        default=None,
        ge=30,
        le=120,
        description="Resting heart rate in BPM"
    )
    heart_rate_variability: Optional[float] = Field(
        default=None,
        ge=0,
        le=200,
        description="HRV in milliseconds (RMSSD)"
    )
    max_heart_rate_today: Optional[int] = Field(
        default=None,
        ge=60,
        le=220,
        description="Maximum heart rate recorded today"
    )
    
    # Sleep Metrics
    sleep_duration_hours: Optional[float] = Field(
        default=None,
        ge=0,
        le=24,
        description="Total sleep duration in hours"
    )
    sleep_score: Optional[int] = Field(
        default=None,
        ge=0,
        le=100,
        description="Overall sleep quality score (0-100)"
    )
    sleep_quality: SleepQuality = Field(
        default=SleepQuality.GOOD,
        description="Qualitative sleep assessment"
    )
    deep_sleep_hours: Optional[float] = Field(
        default=None,
        ge=0,
        le=12,
        description="Deep sleep duration"
    )
    rem_sleep_hours: Optional[float] = Field(
        default=None,
        ge=0,
        le=12,
        description="REM sleep duration"
    )
    
    # Activity Metrics
    steps_today: int = Field(
        default=0,
        ge=0,
        description="Steps taken today"
    )
    active_calories: int = Field(
        default=0,
        ge=0,
        description="Active calories burned today"
    )
    activity_load: float = Field(
        default=0,
        ge=0,
        le=1000,
        description="Training load score"
    )
    weekly_training_load: float = Field(
        default=0,
        ge=0,
        description="Cumulative weekly training load"
    )
    
    # Derived Metrics (set by Wearable Agent)
    recovery_status: RecoveryStatus = Field(
        default=RecoveryStatus.MODERATE,
        description="Overall recovery status"
    )
    fatigue_level: FatigueLevel = Field(
        default=FatigueLevel.MODERATE,
        description="Current fatigue level"
    )
    recommended_intensity_modifier: int = Field(
        default=0,
        ge=-50,
        le=20,
        description="Suggested intensity adjustment percentage"
    )
    readiness_score: int = Field(
        default=70,
        ge=0,
        le=100,
        description="Overall workout readiness score"
    )
    
    # Timestamp
    recorded_at: datetime = Field(
        default_factory=datetime.now,
        description="When metrics were recorded"
    )
    
    @property
    def should_reduce_intensity(self) -> bool:
        """Check if workout intensity should be reduced."""
        return (
            self.recovery_status in [RecoveryStatus.POOR, RecoveryStatus.LOW] or
            self.fatigue_level in [FatigueLevel.ELEVATED, FatigueLevel.HIGH] or
            self.readiness_score < 50
        )
    
    @property
    def is_well_recovered(self) -> bool:
        """Check if user is well-recovered for intense training."""
        return (
            self.recovery_status in [RecoveryStatus.GOOD, RecoveryStatus.OPTIMAL] and
            self.fatigue_level in [FatigueLevel.MINIMAL, FatigueLevel.LOW] and
            self.readiness_score >= 75
        )
