"""Adaptation Agent - Feedback loop and program optimization."""

import json
import logging
from typing import Any

from src.state import FitnessState
from src.models.feedback import (
    WeeklyFeedback,
    AdaptationAction,
    PerformanceTrend,
    LOW_ADHERENCE_THRESHOLD,
)
from src.utils.openai_client import get_structured_response
from src.utils.prompts import get_prompt

logger = logging.getLogger(__name__)

# Maximum number of replan cycles per run. Prevents the
# adaptation → planner loop from spinning until LangGraph's
# recursion limit raises an exception (static feedback would
# otherwise re-trigger the same adjustment forever).
MAX_REPLAN_CYCLES = 2


def adaptation_agent_node(state: FitnessState) -> dict[str, Any]:
    """
    Adaptation Agent node - Continuous program optimization.
    
    Decision Logic:
    - If fatigue HIGH and performance DOWN → reduce_volume
    - If fatigue HIGH and recovery LOW → deload
    - If performance UP and recovery GOOD → increase_intensity
    - If adherence LOW → reduce_volume or change_exercises
    - Otherwise → maintain
    
    Args:
        state: Current fitness state with feedback
    
    Returns:
        State updates with needs_replan flag and updated feedback
    """
    logger.info("Adaptation Agent: Analyzing for program adjustments")
    
    updates: dict[str, Any] = {
        "current_agent": "adaptation_agent",
    }
    
    # Get current feedback and metrics
    feedback = state.get("weekly_feedback")
    wearable = state.get("wearable_metrics")
    program = state.get("program")
    
    if not feedback:
        logger.info("Adaptation Agent: No feedback available, maintaining program")
        updates["needs_replan"] = False
        return updates
    
    # Analyze and decide
    try:
        decision = _analyze_and_decide(feedback, wearable, program, state)
        
        needs_replan = decision.get("needs_replan", False)
        action = decision.get("recommended_action", "maintain")
        
        # Update feedback with decision
        if isinstance(action, str):
            action_enum = _parse_action(action)
        else:
            action_enum = action
        
        feedback.recommended_action = action_enum
        feedback.needs_adjustment = needs_replan
        feedback.adjustment_reason = decision.get("reasoning", "")
        
        updates["weekly_feedback"] = feedback
        updates["needs_replan"] = needs_replan
        
        logger.info(
            f"Adaptation Agent: Decision - "
            f"action={action_enum.value if hasattr(action_enum, 'value') else action_enum}, "
            f"needs_replan={needs_replan}"
        )
        
    except Exception as e:
        logger.error(f"Adaptation Agent: Analysis failed: {e}")
        updates["needs_replan"] = False
    
    return updates


def _analyze_and_decide(
    feedback: WeeklyFeedback,
    wearable: Any,
    program: Any,
    state: FitnessState
) -> dict:
    """Analyze feedback and decide on adaptations."""
    
    # Quick heuristic checks first
    adherence = getattr(feedback, "adherence_rate", 1.0)
    avg_rpe = getattr(feedback, "average_rpe", 7.0)
    avg_energy = getattr(feedback, "average_energy", 7.0)
    performance = getattr(feedback, "performance_trend", PerformanceTrend.STAGNANT)
    
    if hasattr(performance, "value"):
        performance = performance.value
    
    # Get wearable state
    fatigue_high = False
    recovery_low = False
    recovery_good = False
    
    if wearable:
        fatigue = getattr(wearable, "fatigue_level", None)
        if fatigue:
            fatigue_val = fatigue.value if hasattr(fatigue, "value") else fatigue
            fatigue_high = fatigue_val in ["elevated", "high"]
        
        recovery = getattr(wearable, "recovery_status", None)
        if recovery:
            recovery_val = recovery.value if hasattr(recovery, "value") else recovery
            recovery_low = recovery_val in ["poor", "low"]
            recovery_good = recovery_val in ["good", "optimal"]
    
    # Decision logic
    if fatigue_high and performance == "declining":
        return {
            "needs_replan": True,
            "recommended_action": "reduce_volume",
            "reasoning": "High fatigue with declining performance - reducing training volume",
        }
    
    if fatigue_high and recovery_low:
        return {
            "needs_replan": True,
            "recommended_action": "deload",
            "reasoning": "High fatigue and poor recovery - initiating deload week",
        }
    
    if adherence < LOW_ADHERENCE_THRESHOLD:
        return {
            "needs_replan": True,
            "recommended_action": "reduce_volume",
            "reasoning": "Low adherence - simplifying program to improve consistency",
        }
    
    if avg_rpe > 8.5:
        return {
            "needs_replan": True,
            "recommended_action": "reduce_intensity",
            "reasoning": "Perceived difficulty too high - reducing intensity",
        }
    
    if performance in ["improving", "rapid_improvement"] and recovery_good:
        return {
            "needs_replan": True,
            "recommended_action": "increase_intensity",
            "reasoning": "Good performance with strong recovery - progressive overload",
        }
    
    if avg_energy < 4:
        return {
            "needs_replan": True,
            "recommended_action": "deload",
            "reasoning": "Consistently low energy - recommending recovery week",
        }
    
    # Default: maintain current program
    return {
        "needs_replan": False,
        "recommended_action": "maintain",
        "reasoning": "Metrics look good - continuing current program",
    }


def _parse_action(action_str: str) -> AdaptationAction:
    """Parse action string to enum."""
    action_map = {
        "reduce_volume": AdaptationAction.REDUCE_VOLUME,
        "reduce_intensity": AdaptationAction.REDUCE_INTENSITY,
        "maintain": AdaptationAction.MAINTAIN,
        "increase_volume": AdaptationAction.INCREASE_VOLUME,
        "increase_intensity": AdaptationAction.INCREASE_INTENSITY,
        "deload": AdaptationAction.DELOAD,
        "change_exercises": AdaptationAction.CHANGE_EXERCISES,
    }
    return action_map.get(action_str.lower(), AdaptationAction.MAINTAIN)


def should_replan(state: FitnessState) -> bool:
    """
    Conditional edge function for LangGraph.
    
    Determines if the graph should loop back to the planner
    or proceed to end. Caps the loop at MAX_REPLAN_CYCLES so
    repeated identical feedback cannot loop forever.
    
    Args:
        state: Current fitness state
    
    Returns:
        True if replanning is needed, False otherwise
    """
    if state.get("replan_count", 0) >= MAX_REPLAN_CYCLES:
        logger.warning(
            f"Replan limit ({MAX_REPLAN_CYCLES}) reached - ending instead of looping"
        )
        return False
    
    return state.get("needs_replan", False)
