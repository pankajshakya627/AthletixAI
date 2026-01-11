"""Computer Vision Agent - Exercise form and movement analysis."""

import json
import logging
from typing import Any

from src.state import FitnessState
from src.models.assessment import (
    MovementAssessment,
    StrengthLevel,
    FormIssue,
    InjuryRiskFlag,
)
from src.utils.openai_client import get_vision_response, get_structured_response
from src.utils.prompts import get_prompt

logger = logging.getLogger(__name__)


def cv_agent_node(state: FitnessState) -> dict[str, Any]:
    """
    Computer Vision Agent node - Analyzes exercise form from video frames.
    
    Uses OpenAI Vision API to:
    - Evaluate form quality and range of motion
    - Identify stability and balance issues
    - Detect injury risk indicators
    - Provide movement assessment scores
    
    Args:
        state: Current fitness state with video_frames
    
    Returns:
        State updates with movement_assessment
    """
    logger.info("CV Agent: Starting movement analysis")
    
    updates: dict[str, Any] = {
        "current_agent": "cv_agent",
    }
    
    video_frames = state.get("video_frames", [])
    
    if not video_frames:
        logger.info("CV Agent: No video frames provided, using default assessment")
        updates["movement_assessment"] = _create_default_assessment()
        return updates
    
    # Get user context for the prompt
    user_profile = state.get("user_profile")
    experience_level = getattr(user_profile, "experience_level", "beginner")
    injuries = getattr(user_profile, "injury_history", [])
    current_injuries = getattr(user_profile, "current_injuries", [])
    
    # Build the prompt
    prompt = get_prompt(
        "cv_agent",
        experience_level=experience_level,
        injuries=", ".join(injuries) if injuries else "None",
        current_injuries=", ".join(current_injuries) if current_injuries else "None",
    )
    
    try:
        # Call OpenAI Vision API
        logger.info(f"CV Agent: Analyzing {len(video_frames)} frames")
        response = get_vision_response(
            prompt=prompt,
            images=video_frames,
            max_tokens=1500,
        )
        
        # Parse the JSON response
        assessment_data = json.loads(response)
        assessment = _parse_assessment(assessment_data)
        updates["movement_assessment"] = assessment
        
        logger.info(
            f"CV Agent: Assessment complete - "
            f"mobility={assessment.mobility_score}, "
            f"strength={assessment.strength_level.value}"
        )
        
    except json.JSONDecodeError as e:
        logger.error(f"CV Agent: Failed to parse response: {e}")
        updates["movement_assessment"] = _create_default_assessment()
    except Exception as e:
        logger.error(f"CV Agent: Error during analysis: {e}")
        updates["movement_assessment"] = _create_default_assessment()
    
    return updates


def _parse_assessment(data: dict) -> MovementAssessment:
    """Parse API response into MovementAssessment model."""
    
    # Parse form issues
    form_issues = []
    for issue_data in data.get("form_issues", []):
        form_issues.append(FormIssue(
            issue=issue_data.get("issue", "Unknown issue"),
            severity=issue_data.get("severity", "moderate"),
            body_part=issue_data.get("body_part", "general"),
            correction=issue_data.get("correction", "Consult a trainer"),
        ))
    
    # Parse injury risk flags
    injury_flags = []
    for flag_data in data.get("injury_risk_flags", []):
        injury_flags.append(InjuryRiskFlag(
            risk_type=flag_data.get("risk_type", "general"),
            affected_area=flag_data.get("affected_area", "unknown"),
            risk_level=flag_data.get("risk_level", "low"),
            recommendation=flag_data.get("recommendation", "Monitor and adjust"),
        ))
    
    # Map strength level string to enum
    strength_map = {
        "novice": StrengthLevel.NOVICE,
        "beginner": StrengthLevel.BEGINNER,
        "intermediate": StrengthLevel.INTERMEDIATE,
        "advanced": StrengthLevel.ADVANCED,
        "elite": StrengthLevel.ELITE,
    }
    strength_level = strength_map.get(
        data.get("strength_level", "beginner").lower(),
        StrengthLevel.BEGINNER
    )
    
    return MovementAssessment(
        mobility_score=data.get("mobility_score", 7.0),
        strength_level=strength_level,
        stability_score=data.get("stability_score", 7.0),
        flexibility_score=data.get("flexibility_score", 7.0),
        form_quality_score=data.get("form_quality_score", 7.0),
        form_issues=form_issues,
        injury_risk_flags=injury_flags,
        range_of_motion=data.get("range_of_motion", {}),
        recommended_focus_areas=data.get("recommended_focus_areas", []),
        assessment_notes=data.get("assessment_notes"),
    )


def _create_default_assessment() -> MovementAssessment:
    """Create a default assessment when no video is available."""
    return MovementAssessment(
        mobility_score=7.0,
        strength_level=StrengthLevel.BEGINNER,
        stability_score=7.0,
        flexibility_score=7.0,
        form_quality_score=7.0,
        form_issues=[],
        injury_risk_flags=[],
        range_of_motion={},
        recommended_focus_areas=["General mobility", "Core stability"],
        assessment_notes="Default assessment - no video provided for analysis",
    )
