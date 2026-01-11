"""Wearable Analysis Agent - Physiological metrics and recovery analysis."""

import json
import logging
from typing import Any

from src.state import FitnessState
from src.models.wearables import (
    WearableMetrics,
    RecoveryStatus,
    FatigueLevel,
    SleepQuality,
)
from src.utils.openai_client import get_structured_response
from src.utils.prompts import get_prompt

logger = logging.getLogger(__name__)


def wearable_agent_node(state: FitnessState) -> dict[str, Any]:
    """
    Wearable Analysis Agent node - Interprets physiological metrics.
    
    Analyzes:
    - Heart rate and HRV data
    - Sleep quality and duration
    - Activity load and training stress
    - Recovery status and readiness
    
    Args:
        state: Current fitness state with wearable_data
    
    Returns:
        State updates with wearable_metrics including recovery recommendations
    """
    logger.info("Wearable Agent: Starting physiological analysis")
    
    updates: dict[str, Any] = {
        "current_agent": "wearable_agent",
    }
    
    wearable_data = state.get("wearable_data", {})
    
    if not wearable_data:
        logger.info("Wearable Agent: No wearable data provided, using defaults")
        updates["wearable_metrics"] = _create_default_metrics()
        return updates
    
    # Create initial metrics from raw data
    metrics = _parse_raw_wearable_data(wearable_data)
    
    # Use LLM to analyze and derive recovery status
    try:
        analysis = _analyze_with_llm(wearable_data, state)
        
        # Update metrics with LLM analysis
        metrics.recovery_status = _parse_recovery_status(analysis.get("recovery_status", "moderate"))
        metrics.fatigue_level = _parse_fatigue_level(analysis.get("fatigue_level", "moderate"))
        metrics.readiness_score = analysis.get("readiness_score", 70)
        metrics.recommended_intensity_modifier = analysis.get("recommended_intensity_modifier", 0)
        
        logger.info(
            f"Wearable Agent: Analysis complete - "
            f"recovery={metrics.recovery_status.value}, "
            f"fatigue={metrics.fatigue_level.value}, "
            f"readiness={metrics.readiness_score}"
        )
        
    except Exception as e:
        logger.error(f"Wearable Agent: LLM analysis failed: {e}")
        # Keep the basic parsed metrics
    
    updates["wearable_metrics"] = metrics
    return updates


def _parse_raw_wearable_data(data: dict) -> WearableMetrics:
    """Parse raw wearable data into WearableMetrics model."""
    
    # Parse sleep quality
    sleep_score = data.get("sleep_score", 70)
    if sleep_score >= 85:
        sleep_quality = SleepQuality.EXCELLENT
    elif sleep_score >= 70:
        sleep_quality = SleepQuality.GOOD
    elif sleep_score >= 50:
        sleep_quality = SleepQuality.FAIR
    else:
        sleep_quality = SleepQuality.POOR
    
    return WearableMetrics(
        resting_heart_rate=data.get("resting_heart_rate"),
        heart_rate_variability=data.get("hrv") or data.get("heart_rate_variability"),
        max_heart_rate_today=data.get("max_heart_rate"),
        sleep_duration_hours=data.get("sleep_hours") or data.get("sleep_duration"),
        sleep_score=sleep_score,
        sleep_quality=sleep_quality,
        deep_sleep_hours=data.get("deep_sleep"),
        rem_sleep_hours=data.get("rem_sleep"),
        steps_today=data.get("steps", 0),
        active_calories=data.get("active_calories", 0),
        activity_load=data.get("activity_load", 0),
        weekly_training_load=data.get("weekly_load", 0),
    )


def _analyze_with_llm(wearable_data: dict, state: FitnessState) -> dict:
    """Use LLM to analyze wearable data and derive insights."""
    
    # Build context
    training_load = wearable_data.get("weekly_load", 0)
    sleep_quality = wearable_data.get("sleep_score", 70)
    hrv_baseline = wearable_data.get("hrv_baseline", 50)
    
    prompt = get_prompt(
        "wearable_agent",
        wearable_data=json.dumps(wearable_data, indent=2),
        training_load=training_load,
        sleep_quality=sleep_quality,
        hrv_baseline=hrv_baseline,
    )
    
    response = get_structured_response(
        system_prompt="You are a sports physiologist analyzing wearable metrics. Respond in JSON.",
        user_message=prompt,
        max_tokens=800,
    )
    
    return json.loads(response)


def _parse_recovery_status(status: str) -> RecoveryStatus:
    """Parse recovery status string to enum."""
    status_map = {
        "poor": RecoveryStatus.POOR,
        "low": RecoveryStatus.LOW,
        "moderate": RecoveryStatus.MODERATE,
        "good": RecoveryStatus.GOOD,
        "optimal": RecoveryStatus.OPTIMAL,
    }
    return status_map.get(status.lower(), RecoveryStatus.MODERATE)


def _parse_fatigue_level(level: str) -> FatigueLevel:
    """Parse fatigue level string to enum."""
    level_map = {
        "minimal": FatigueLevel.MINIMAL,
        "low": FatigueLevel.LOW,
        "moderate": FatigueLevel.MODERATE,
        "elevated": FatigueLevel.ELEVATED,
        "high": FatigueLevel.HIGH,
    }
    return level_map.get(level.lower(), FatigueLevel.MODERATE)


def _create_default_metrics() -> WearableMetrics:
    """Create default metrics when no wearable data is available."""
    return WearableMetrics(
        recovery_status=RecoveryStatus.MODERATE,
        fatigue_level=FatigueLevel.MODERATE,
        readiness_score=70,
        recommended_intensity_modifier=0,
    )
