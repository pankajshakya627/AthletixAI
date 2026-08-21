"""Coach Agent - Human-like coaching communication."""

import logging
from datetime import datetime
from typing import Any

from src.state import FitnessState
from src.utils.openai_client import get_chat_response
from src.utils.prompts import get_prompt
from src.safety.disclaimers import get_relevant_disclaimers

logger = logging.getLogger(__name__)


def coach_agent_node(state: FitnessState) -> dict[str, Any]:
    """
    Coach Agent node - Generates human-like coaching messages.
    
    Responsibilities:
    - Translate technical plans into friendly guidance
    - Provide daily motivation and technique reminders
    - Generate adherence nudges
    - Surface appropriate disclaimers
    
    Args:
        state: Current fitness state
    
    Returns:
        State updates with coaching_message and daily_tips
    """
    logger.info("Coach Agent: Generating coaching message")
    
    updates: dict[str, Any] = {
        "current_agent": "coach_agent",
    }
    
    # Gather context
    user_profile = state.get("user_profile")
    program = state.get("program")
    wearable = state.get("wearable_metrics")
    nutrition = state.get("nutrition_analysis")
    
    user_name = getattr(user_profile, "name", "there") if user_profile else "there"
    
    # Get today's workout
    workout_str = _format_todays_workout(program)
    
    # Get progress summary
    progress_str = _format_progress(state)
    
    # Get current state
    current_state_str = _format_current_state(wearable, nutrition)
    
    try:
        prompt = get_prompt(
            "coach_agent",
            user_name=user_name,
            workout=workout_str,
            progress=progress_str,
            current_state=current_state_str,
        )
        
        response = get_chat_response(
            system_prompt="""You are an encouraging, knowledgeable fitness coach. 
Keep messages concise, specific, and motivating. 
Avoid medical claims and generic advice.
Include 2-3 specific technique cues for exercises.
Always maintain a supportive but professional tone.""",
            user_message=prompt,
            max_tokens=600,
            temperature=0.7,
        )
        
        # Get relevant disclaimers
        disclaimers = get_relevant_disclaimers(state)
        
        # Combine coaching message
        coaching_message = response
        if disclaimers:
            coaching_message += "\n\n---\n" + "\n".join(f"⚠️ {d}" for d in disclaimers)
        
        updates["coaching_message"] = coaching_message
        
        # Generate daily tips
        updates["daily_tips"] = _generate_daily_tips(state)
        
        logger.info("Coach Agent: Coaching message generated")
        
    except Exception as e:
        logger.error(f"Coach Agent: Failed to generate message: {e}")
        updates["coaching_message"] = _get_fallback_message(user_name)
        updates["daily_tips"] = ["Stay consistent with your training", "Focus on proper form"]
    
    return updates


def _format_todays_workout(program: Any) -> str:
    """Format today's workout for coaching."""
    if not program:
        return "Rest day or custom workout"
    
    schedules = getattr(program, "weekly_schedules", [])
    if not schedules:
        return "Program being prepared"
    
    week = schedules[0]
    workouts = getattr(week, "workouts", [])
    if not workouts:
        return "Rest day"
    
    # Select the workout matching today's weekday (day_number 1=Monday),
    # falling back to the first non-rest day
    weekday = datetime.now().isoweekday()
    workout = next(
        (w for w in workouts if w.day_number == weekday and not w.is_rest_day),
        next((w for w in workouts if not w.is_rest_day), workouts[0]),
    )
    
    exercises = getattr(workout, "exercises", [])
    
    exercise_list = []
    for ex in exercises[:5]:  # Limit to 5 exercises
        exercise_list.append(f"- {ex.name}: {ex.sets}x{ex.reps}")
    
    return f"""**{workout.day_name}** - {workout.focus}
{chr(10).join(exercise_list)}
Duration: ~{workout.estimated_duration_minutes} minutes"""


def _format_progress(state: FitnessState) -> str:
    """Format recent progress."""
    feedback = state.get("weekly_feedback")
    if not feedback:
        return "Starting fresh - let's build momentum!"
    
    adherence = getattr(feedback, "adherence_rate", 1.0)
    trend = getattr(feedback, "performance_trend", "stagnant")
    
    if hasattr(trend, "value"):
        trend = trend.value
    
    return f"Adherence: {adherence*100:.0f}%, Performance: {trend}"


def _format_current_state(wearable: Any, nutrition: Any) -> str:
    """Format current physical state."""
    parts = []
    
    if wearable:
        recovery = getattr(wearable, "recovery_status", "moderate")
        if hasattr(recovery, "value"):
            recovery = recovery.value
        readiness = getattr(wearable, "readiness_score", 70)
        parts.append(f"Recovery: {recovery}, Readiness: {readiness}/100")
    
    if nutrition:
        macros = getattr(nutrition, "daily_totals", None)
        if macros:
            parts.append(
                f"Today's nutrition: {macros.protein_g:.0f}g protein, "
                f"{macros.calories:.0f} cal"
            )
    
    return " | ".join(parts) if parts else "Ready to train!"


def _generate_daily_tips(state: FitnessState) -> list[str]:
    """Generate personalized daily tips."""
    tips = []
    
    wearable = state.get("wearable_metrics")
    nutrition = state.get("nutrition_analysis")
    movement = state.get("movement_assessment")
    
    # Recovery-based tips
    if wearable:
        if getattr(wearable, "should_reduce_intensity", False):
            tips.append("Your recovery is lower today - focus on technique over intensity")
        if getattr(wearable, "is_well_recovered", False):
            tips.append("You're well recovered - great day to push a bit harder!")
    
    # Nutrition tips
    if nutrition:
        if not getattr(nutrition, "protein_target_met", True):
            tips.append("Try to include more protein in your remaining meals today")
    
    # Movement-based tips
    if movement:
        focus_areas = getattr(movement, "recommended_focus_areas", [])
        if focus_areas:
            tips.append(f"Don't forget your mobility work for: {', '.join(focus_areas[:2])}")
    
    # Default tips if none generated
    if not tips:
        tips = [
            "Stay hydrated throughout your workout",
            "Focus on controlled movements and good form",
        ]
    
    return tips[:3]  # Max 3 tips


def _get_fallback_message(name: str) -> str:
    """Get a fallback message if LLM fails."""
    return f"""Hey {name}! 👋

Ready for today's session? Remember:
- Warm up properly before starting
- Focus on form over weight
- Listen to your body

Let's make today count! 💪

---
⚠️ Always consult a healthcare provider before starting any new exercise program."""
