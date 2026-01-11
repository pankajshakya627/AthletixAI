"""Movement assessment models from CV analysis."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class StrengthLevel(str, Enum):
    """Assessed strength level."""
    NOVICE = "novice"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    ELITE = "elite"


class FormIssue(BaseModel):
    """Individual form issue identified during movement analysis."""
    
    issue: str = Field(description="Description of the form issue")
    severity: str = Field(
        default="moderate",
        description="Severity level: minor, moderate, major"
    )
    body_part: str = Field(description="Affected body part")
    correction: str = Field(description="Suggested correction")


class InjuryRiskFlag(BaseModel):
    """Potential injury risk identified during movement analysis."""
    
    risk_type: str = Field(description="Type of injury risk")
    affected_area: str = Field(description="Body area at risk")
    risk_level: str = Field(
        default="low",
        description="Risk level: low, moderate, high"
    )
    recommendation: str = Field(description="Safety recommendation")


class MovementAssessment(BaseModel):
    """Complete movement assessment from CV agent analysis."""
    
    mobility_score: float = Field(
        ge=0,
        le=10,
        description="Overall mobility score (0-10)"
    )
    strength_level: StrengthLevel = Field(
        description="Assessed strength level"
    )
    stability_score: float = Field(
        default=7.0,
        ge=0,
        le=10,
        description="Core and joint stability score (0-10)"
    )
    flexibility_score: float = Field(
        default=7.0,
        ge=0,
        le=10,
        description="Flexibility assessment score (0-10)"
    )
    form_quality_score: float = Field(
        default=7.0,
        ge=0,
        le=10,
        description="Overall form quality score (0-10)"
    )
    form_issues: list[FormIssue] = Field(
        default_factory=list,
        description="List of identified form issues"
    )
    injury_risk_flags: list[InjuryRiskFlag] = Field(
        default_factory=list,
        description="Potential injury risk flags"
    )
    range_of_motion: dict[str, str] = Field(
        default_factory=dict,
        description="Range of motion assessment per joint"
    )
    recommended_focus_areas: list[str] = Field(
        default_factory=list,
        description="Areas requiring improvement focus"
    )
    assessment_notes: Optional[str] = Field(
        default=None,
        description="Additional assessment notes from CV agent"
    )
    
    @property
    def overall_score(self) -> float:
        """Calculate weighted overall movement score."""
        return round(
            (self.mobility_score * 0.25) +
            (self.stability_score * 0.25) +
            (self.flexibility_score * 0.2) +
            (self.form_quality_score * 0.3),
            1
        )
    
    @property
    def is_high_risk(self) -> bool:
        """Check if any high-risk injury flags exist."""
        return any(flag.risk_level == "high" for flag in self.injury_risk_flags)
