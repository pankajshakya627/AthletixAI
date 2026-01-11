"""Program Planner Agent - Training program generation."""

import json
import logging
import re
from typing import Any

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
    else:
        logger.info("Planner Agent: Creating new program")
        program = _create_new_program(state)
    
    updates["program"] = program
    updates["needs_replan"] = False  # Reset the flag
    
    logger.info(
        f"Planner Agent: Program generated - "
        f"{program.program_length_weeks} weeks, "
        f"{program.weekly_split}"
    )
    
    return updates


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
    
    return existing


def _modify_volume(program: TrainingProgram, multiplier: float) -> TrainingProgram:
    """Modify program volume by a multiplier."""
    for week in program.weekly_schedules:
        for workout in week.workouts:
            for exercise in workout.exercises:
                exercise.sets = max(1, int(exercise.sets * multiplier))
    
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
                    sets=ex_data.get("sets", 3),
                    reps=str(ex_data.get("reps", "8-12")),
                    rest_seconds=ex_data.get("rest_seconds", ex_data.get("rest", 90)),
                    weight_suggestion=ex_data.get("weight_suggestion"),
                    technique_cues=ex_data.get("technique_cues", ex_data.get("cues", [])),
                ))
            
            workouts.append(DailyWorkout(
                day_number=day_data.get("day_number", day_data.get("day", 1)),
                day_name=day_data.get("day_name", day_data.get("name", "Workout")),
                focus=day_data.get("focus", "General"),
                exercises=exercises,
                estimated_duration_minutes=day_data.get("duration", 60),
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
    """Create a default beginner-friendly program."""
    
    days = getattr(goals, "weekly_workout_days", 3) if goals else 3
    
    # Simple full body program
    base_exercises = [
        Exercise(name="Goblet Squat", sets=3, reps="10-12", rest_seconds=90,
                 technique_cues=["Keep chest up", "Push knees out"]),
        Exercise(name="Push-ups", sets=3, reps="8-12", rest_seconds=60,
                 technique_cues=["Maintain plank position", "Full range of motion"]),
        Exercise(name="Dumbbell Rows", sets=3, reps="10-12", rest_seconds=60,
                 technique_cues=["Pull to hip", "Squeeze shoulder blade"]),
        Exercise(name="Plank", sets=3, reps="30-45 seconds", rest_seconds=45,
                 technique_cues=["Keep hips level", "Engage core"]),
    ]
    
    workouts = []
    for d in range(days):
        workouts.append(DailyWorkout(
            day_number=d * 2 + 1,  # Spread across week
            day_name=f"Full Body Day {d + 1}",
            focus="Full Body Strength",
            exercises=base_exercises,
            estimated_duration_minutes=45,
        ))
    
    return TrainingProgram(
        program_name="Beginner Full Body Program",
        program_length_weeks=4,
        weekly_split="Full Body",
        weekly_schedules=[WeeklySchedule(week_number=1, workouts=workouts)],
        progression_rules=[
            ProgressionRule(
                rule_type="double_progression",
                condition="Complete all reps with good form",
                action="Add 1-2 reps next session, then increase weight"
            )
        ],
        difficulty_level="beginner",
        goals_addressed=["General Fitness", "Strength Foundation"],
    )


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
