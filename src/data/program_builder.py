"""
Program Builder - Creates TrainingProgram from templates.

Uses the level-specific templates with proper Exercise objects.
"""

from typing import Any
from src.models.program import (
    TrainingProgram, WeeklySchedule, DailyWorkout, Exercise, ProgressionRule
)
from src.data.program_templates import (
    BEGINNER_TEMPLATE, INTERMEDIATE_TEMPLATE, ADVANCED_TEMPLATE
)


def build_program_from_template(
    exp_level: str,
    user_name: str = "User"
) -> TrainingProgram:
    """
    Build a complete TrainingProgram from level-specific template.
    
    Args:
        exp_level: 'beginner', 'intermediate', or 'advanced'
        user_name: User's name for personalization
    
    Returns:
        Complete TrainingProgram object
    """
    # Select template based on level
    templates = {
        "beginner": BEGINNER_TEMPLATE,
        "intermediate": INTERMEDIATE_TEMPLATE,
        "advanced": ADVANCED_TEMPLATE,
        "elite": ADVANCED_TEMPLATE,
    }
    template = templates.get(exp_level.lower(), INTERMEDIATE_TEMPLATE)
    
    # Build workouts from template
    workouts = []
    for i, workout_def in enumerate(template["workouts"]):
        day_name = workout_def.get("day_name", f"Day {i+1}")
        focus = workout_def.get("focus", "")
        
        # Handle "same_as_day_1" reference
        sections = workout_def.get("sections", {})
        if sections == "same_as_day_1":
            sections = template["workouts"][0]["sections"]
        
        # Build exercises from sections
        exercises = []
        
        # Warmup exercises
        for ex_def in sections.get("warmup", []):
            exercises.append(_create_exercise(ex_def, is_warmup=True))
        
        # Main exercises
        for ex_def in sections.get("main", []):
            exercises.append(_create_exercise(ex_def, is_warmup=False))
        
        # Cooldown exercises
        for ex_def in sections.get("cooldown", []):
            exercises.append(_create_exercise(ex_def, is_warmup=True))
        
        workouts.append(DailyWorkout(
            day_number=i + 1,
            day_name=day_name,
            focus=focus,
            exercises=exercises,
            estimated_duration_minutes=60 if exp_level != "beginner" else 45,
        ))
    
    # Build progression rules
    progression_rules = []
    for rule_text in template.get("progression_rules", []):
        progression_rules.append(ProgressionRule(
            rule_type="progression",
            condition=rule_text,
            action=rule_text
        ))
    
    return TrainingProgram(
        program_name=template["program_name"],
        program_length_weeks=template.get("program_length_weeks", 4),
        weekly_split=template.get("weekly_split", ""),
        weekly_schedules=[WeeklySchedule(week_number=1, workouts=workouts)],
        progression_rules=progression_rules,
        difficulty_level=exp_level,
        goals_addressed=["Muscle Building", "Strength", "General Fitness"],
    )


def _create_exercise(ex_def: dict, is_warmup: bool = False) -> Exercise:
    """Create an Exercise object from template definition, enriched with details."""
    from src.data.exercise_details import get_exercise_details
    
    name = ex_def.get("name", "Unknown Exercise")
    
    # Look up detailed instructions for this exercise
    details = get_exercise_details(name)
    
    return Exercise(
        name=name,
        sets=ex_def.get("sets", 3),
        reps=str(ex_def.get("reps", "10")),
        rest_seconds=0 if is_warmup else 60,
        technique_cues=[],
        alternatives=[ex_def.get("alternative")] if ex_def.get("alternative") else [],
        description=details.get("description"),
        steps=details.get("steps", []),
        breathing_guide=details.get("breathing_guide"),
    )

