"""Program Planner Agent - Training program planner agent using GPT-4o."""

import json
import logging
import re
from typing import Any, Optional

from src.state import FitnessState
from src.models.program import (
    TrainingProgram,
    WeeklySchedule,
    DailyWorkout,
    Exercise,
    ProgressionRule,
    MuscleGroup,
    ExerciseType,
)
from src.utils.openai_client import get_structured_response
from src.utils.prompts import get_prompt
from src.safety.guardrails import apply_safety_limits

logger = logging.getLogger(__name__)


def _extract_json(text: str) -> str:
    """Extract JSON from markdown code blocks or raw text."""
    patterns = [
        r'```json\s*([\s\S]*?)\s*```',
        r'```\s*([\s\S]*?)\s*```',
        r'\{[\s\S]*\}',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            json_str = match.group(1) if '```' in pattern else match.group(0)
            try:
                json.loads(json_str)
                return json_str
            except json.JSONDecodeError:
                continue
    
    return text


def planner_agent_node(state: FitnessState) -> dict[str, Any]:
    """
    Program Planner Agent node - Generates structured training programs.
    
    Creates personalized programs based on:
    - User profile and goals
    - Movement assessment results
    - Wearable recovery metrics
    - Available equipment
    
    Enforces:
    - Progressive overload principles
    - Recovery-aware volume
    - Equipment constraints
    - Injury considerations
    
    Args:
        state: Current fitness state
    
    Returns:
        State updates with training program
    """
    logger.info("Planner Agent: Generating training program")
    
    updates: dict[str, Any] = {
        "current_agent": "planner_agent",
    }
    
    # Gather context
    user_profile = state.get("user_profile")
    goals = state.get("goals")
    movement = state.get("movement_assessment")
    wearable = state.get("wearable_metrics")
    
    # Check if we need to adapt existing program
    needs_replan = state.get("needs_replan", False)
    existing_program = state.get("program")
    
    if needs_replan and existing_program:
        logger.info("Planner Agent: Adapting existing program based on feedback")
        program = _adapt_program(existing_program, state)
        updates["replan_count"] = state.get("replan_count", 0) + 1
    else:
        logger.info("Planner Agent: Creating new program")
        program = _create_new_program(state)
    
    # NOTE: Enrichment with research URLs now happens in research_agent (runs after planner)
    
    # Enforce safety limits (volume caps, injury-aware filtering)
    program = apply_safety_limits(program, user_profile)
    
    updates["program"] = program
    updates["needs_replan"] = False  # Reset the flag
    
    logger.info(
        f"Planner Agent: Program generated - "
        f"{program.program_length_weeks} weeks, "
        f"{program.weekly_split}"
    )
    
    return updates


def _enrich_program_with_resources(
    program: TrainingProgram,
    research_results
) -> TrainingProgram:
    """
    Enrich program exercises with tutorial URLs from research agent.
    
    Args:
        program: Generated training program
        research_results: ResearchResults from research agent
    
    Returns:
        Program with exercises enriched with URLs
    """
    enriched_count = 0
    not_found = []
    
    for week in program.weekly_schedules:
        for workout in week.workouts:
            for exercise in workout.exercises:
                # Try to find matching resource with fuzzy matching
                resource = _find_matching_resource(exercise.name, research_results)
                
                if resource:
                    exercise.tutorial_url = resource.tutorial_url
                    exercise.gif_url = resource.gif_url
                    exercise.video_url = resource.video_url
                    exercise.image_urls = resource.image_urls
                    exercise.breathing_guide = resource.breathing_guide
                    exercise.common_mistakes = resource.common_mistakes
                    enriched_count += 1
                else:
                    not_found.append(exercise.name)
    
    logger.info(f"✓ Enriched {enriched_count} exercises with tutorial URLs")
    if not_found:
        logger.warning(f"⚠️  No resources found for: {', '.join(set(not_found[:5]))}")
    
    return program


def _find_matching_resource(exercise_name: str, research_results) -> Optional[any]:
    """
    Find matching resource with fuzzy name matching.
    
    Handles variations like:
    - "Bench Press / Push-ups" -> "bench press"
    - "Barbell Row" -> "barbell row"
    - Case insensitive matching
    """
    # Try exact match first (case-insensitive)
    exact_match = research_results.get_resource(exercise_name.lower())
    if exact_match:
        return exact_match
    
    # Try first part if there's a slash (alternative exercises)
    if '/' in exercise_name:
        first_exercise = exercise_name.split('/')[0].strip()
        match = research_results.get_resource(first_exercise.lower())
        if match:
            return match
    
    # Try without modifiers (e.g., "Dumbbell Bench Press" -> "bench press")
    exercise_keywords = exercise_name.lower()
    for cached_name in research_results.exercises.keys():
        # Check if the cached name is in the exercise name
        if cached_name in exercise_keywords:
            return research_results.exercises[cached_name]
    
    return None


def _create_new_program(state: FitnessState) -> TrainingProgram:
    """Create a new training program using LLM."""
    
    user_profile = state.get("user_profile")
    goals = state.get("goals")
    movement = state.get("movement_assessment")
    wearable = state.get("wearable_metrics")
    
    # Build context strings
    profile_str = _format_profile(user_profile)
    movement_str = _format_assessment(movement)
    wearable_str = _format_wearable(wearable)
    history_str = _format_history(state.get("user_history"))
    
    goals_str = f"Primary: {getattr(goals, 'primary_goal', 'general_fitness')}"
    equipment = getattr(user_profile, "equipment_available", [])
    intensity_mod = getattr(wearable, "recommended_intensity_modifier", 0) if wearable else 0
    days_per_week = getattr(goals, "weekly_workout_days", 3) if goals else 3
    
    prompt = get_prompt(
        "planner_agent",
        user_profile=profile_str,
        movement_assessment=movement_str,
        wearable_metrics=wearable_str,
        goals=goals_str,
        equipment=", ".join(equipment) if equipment else "Bodyweight only",
        intensity_modifier=intensity_mod,
        program_length=4,
        days_per_week=days_per_week,
        history=history_str,
    )
    
    try:
        response = get_structured_response(
            system_prompt="You are an expert strength coach. Generate a complete training program in JSON format.",
            user_message=prompt,
            max_tokens=3000,
        )
        
        json_str = _extract_json(response)
        program_data = json.loads(json_str)
        return _parse_program(program_data)
        
    except Exception as e:
        logger.error(f"Planner Agent: LLM generation failed: {e}")
        return _create_default_program(user_profile, goals)


def _adapt_program(existing: TrainingProgram, state: FitnessState) -> TrainingProgram:
    """Adapt existing program based on feedback."""
    
    feedback = state.get("weekly_feedback")
    if not feedback:
        return existing
    
    action = getattr(feedback, "recommended_action", None)
    
    if action:
        action_value = action.value if hasattr(action, "value") else str(action)
        
        if action_value == "reduce_volume":
            # Reduce sets by 20%
            return _modify_volume(existing, multiplier=0.8)
        elif action_value == "increase_volume":
            # Increase sets by 10%
            return _modify_volume(existing, multiplier=1.1)
        elif action_value == "deload":
            # Reduce intensity significantly
            return _modify_volume(existing, multiplier=0.5)
        elif action_value == "reduce_intensity":
            return _modify_intensity(existing, increase=False)
        elif action_value == "increase_intensity":
            return _modify_intensity(existing, increase=True)
        elif action_value == "change_exercises":
            return _swap_exercises(existing)
    
    return existing


def _modify_volume(program: TrainingProgram, multiplier: float) -> TrainingProgram:
    """Modify program volume by a multiplier."""
    import math
    
    for week in program.weekly_schedules:
        for workout in week.workouts:
            for exercise in workout.exercises:
                # Ceil for increases / floor for decreases so the change
                # always takes effect even on low set counts
                if multiplier >= 1:
                    new_sets = math.ceil(exercise.sets * multiplier)
                else:
                    new_sets = math.floor(exercise.sets * multiplier)
                exercise.sets = max(1, min(new_sets, 10))
    
    return program


def _modify_intensity(program: TrainingProgram, increase: bool) -> TrainingProgram:
    """Adjust workout intensity via rest periods and intensity labels.
    
    Reducing intensity lengthens rest periods and lowers the intensity label;
    increasing intensity shortens rest periods (progressive overload).
    """
    for week in program.weekly_schedules:
        week.intensity_modifier = max(-50, min(20, week.intensity_modifier + (5 if increase else -5)))
        for workout in week.workouts:
            workout.intensity_level = "high" if increase else "moderate"
            for exercise in workout.exercises:
                if increase:
                    exercise.rest_seconds = max(30, int(exercise.rest_seconds * 0.85))
                else:
                    exercise.rest_seconds = min(300, int(exercise.rest_seconds * 1.25) + 5)
    
    return program


def _swap_exercises(program: TrainingProgram) -> TrainingProgram:
    """Swap exercises for their listed alternatives where available."""
    swapped = 0
    for week in program.weekly_schedules:
        for workout in week.workouts:
            for exercise in workout.exercises:
                if exercise.alternatives:
                    old_name = exercise.name
                    exercise.name = exercise.alternatives[0]
                    exercise.alternatives = [old_name] + exercise.alternatives[1:]
                    swapped += 1
    
    logger.info(f"Planner Agent: Swapped {swapped} exercises for alternatives")
    return program


def _parse_program(data: dict) -> TrainingProgram:
    """Parse LLM response into TrainingProgram model."""
    
    weekly_schedules = []
    for week_data in data.get("weekly_schedules", data.get("weeks", [])):
        workouts = []
        for day_data in week_data.get("workouts", week_data.get("days", [])):
            exercises = []
            for ex_data in day_data.get("exercises", []):
                exercises.append(Exercise(
                    name=ex_data.get("name", "Unknown"),
                    category=ex_data.get("category", "main"),
                    sets=ex_data.get("sets", 3),
                    reps=str(ex_data.get("reps", "8-12")),
                    rest_seconds=ex_data.get("rest_seconds", ex_data.get("rest", 90)),
                    weight_suggestion=ex_data.get("weight_suggestion"),
                    technique_cues=ex_data.get("technique_cues", ex_data.get("cues", [])),
                    description=ex_data.get("description"),
                    steps=ex_data.get("steps", []),
                    breathing_guide=ex_data.get("breathing_guide"),
                ))
            
            workouts.append(DailyWorkout(
                day_number=day_data.get("day_number", day_data.get("day", 1)),
                day_name=day_data.get("day_name", day_data.get("name", "Workout")),
                focus=day_data.get("focus", "General"),
                exercises=exercises,
                estimated_duration_minutes=day_data.get(
                    "estimated_duration_minutes", day_data.get("duration", 60)
                ),
                is_rest_day=day_data.get("is_rest_day", False),
            ))
        
        weekly_schedules.append(WeeklySchedule(
            week_number=week_data.get("week_number", week_data.get("week", 1)),
            workouts=workouts,
        ))
    
    progression = []
    for rule_data in data.get("progression_rules", []):
        progression.append(ProgressionRule(
            rule_type=rule_data.get("type", "linear"),
            condition=rule_data.get("condition", "Complete all reps"),
            action=rule_data.get("action", "Add 2.5kg"),
        ))
    
    return TrainingProgram(
        program_name=data.get("program_name", "Custom Training Program"),
        program_length_weeks=data.get("program_length_weeks", data.get("length", 4)),
        weekly_split=data.get("weekly_split", data.get("split", "Full Body")),
        weekly_schedules=weekly_schedules,
        progression_rules=progression,
        equipment_required=data.get("equipment_required", []),
        difficulty_level=data.get("difficulty_level", "intermediate"),
        goals_addressed=data.get("goals_addressed", []),
    )


def _create_default_program(user_profile: Any, goals: Any) -> TrainingProgram:
    """
    Create a level-appropriate default program using pre-built templates.
    
    Selects template based on experience level:
    - Beginner: 3-day full body
    - Intermediate: 5-day Push/Pull/Legs
    - Advanced: 6-day body part split
    """
    from src.data.program_builder import build_program_from_template
    
    # Get experience level
    exp_level = getattr(user_profile, "experience_level", "beginner") if user_profile else "beginner"
    if hasattr(exp_level, "value"):
        exp_level = exp_level.value
    
    # Get user name
    user_name = getattr(user_profile, "name", "User") if user_profile else "User"
    
    logger.info(f"Creating {exp_level} program using template-based builder")
    
    # Use the new template-based program builder
    return build_program_from_template(exp_level, user_name)


def _format_history(history: Any) -> str:
    """Format recent workout history for prompt grounding."""
    if not history:
        return "No previous workout history available (new user)"
    
    lines = []
    for entry in history[:5]:
        date = entry.get("workout_date", "unknown date")
        exercises = entry.get("exercises_completed") or []
        fatigue = entry.get("fatigue_level", "n/a")
        performance = entry.get("performance_rating", "n/a")
        lines.append(
            f"- {date}: {len(exercises)} exercises, "
            f"fatigue {fatigue}/10, performance {performance}/10"
        )
    
    return "\n".join(lines)


def _format_profile(profile: Any) -> str:
    """Format user profile for prompt."""
    if not profile:
        return "No profile available"
    
    return f"""Age: {getattr(profile, 'age', 'Unknown')}
Experience: {getattr(profile, 'experience_level', 'beginner')}
Injuries: {', '.join(getattr(profile, 'injury_history', [])) or 'None'}
Current Issues: {', '.join(getattr(profile, 'current_injuries', [])) or 'None'}"""


def _format_assessment(assessment: Any) -> str:
    """Format movement assessment for prompt."""
    if not assessment:
        return "No assessment available"
    
    return f"""Mobility Score: {getattr(assessment, 'mobility_score', 7)}/10
Strength Level: {getattr(assessment, 'strength_level', 'beginner')}
Form Issues: {len(getattr(assessment, 'form_issues', []))} identified
Focus Areas: {', '.join(getattr(assessment, 'recommended_focus_areas', []))}"""


def _format_wearable(wearable: Any) -> str:
    """Format wearable metrics for prompt."""
    if not wearable:
        return "No wearable data available"
    
    return f"""Recovery: {getattr(wearable, 'recovery_status', 'moderate')}
Fatigue: {getattr(wearable, 'fatigue_level', 'moderate')}
Readiness: {getattr(wearable, 'readiness_score', 70)}/100
Intensity Modifier: {getattr(wearable, 'recommended_intensity_modifier', 0)}%"""
