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
    
    # NOTE: Enrichment with research URLs now happens in research_agent (runs after planner)
    
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
    """
    Create a level-appropriate default program using pre-built templates.
    
    Selects template based on experience level:
    - Beginner: 3-day full body
    - Intermediate: 5-day Push/Pull/Legs
    - Advanced: 6-day body part split
    """
    from src.data.program_templates import get_template_for_level
    from src.data.exercise_library import get_exercises_for_level, EXERCISE_LIBRARY
    
    # Get experience level
    exp_level = getattr(user_profile, "experience_level", "beginner") if user_profile else "beginner"
    if hasattr(exp_level, "value"):
        exp_level = exp_level.value
    
    # Get available equipment
    equipment = getattr(user_profile, "equipment_available", []) if user_profile else []
    
    # Get template for this level
    template = get_template_for_level(exp_level)
    days = template.get("days_per_week", 5)
    
    logger.info(f"Creating {exp_level} program: {template['program_name']} ({days} days/week)")
    
    # Build workout templates from the level-specific template
    workout_templates = [
        # Day 1: Push (Chest, Shoulders, Triceps)
        {
            "day_name": "Push Day",
            "focus": "Chest, Shoulders, Triceps",
            "exercises": [
                # Warmup
                Exercise(name="Arm Circles", sets=2, reps="30 seconds", rest_seconds=0, technique_cues=["Forward then backward"]),
                Exercise(name="Shoulder Rolls", sets=2, reps="15 each direction", rest_seconds=0, technique_cues=["Slow controlled movement"]),
                Exercise(name="Push-up to Downward Dog", sets=2, reps="8", rest_seconds=30, technique_cues=["Dynamic stretch"]),
                # Main exercises
                Exercise(name="Bench Press / Push-ups", sets=4, reps="8-12", rest_seconds=90, technique_cues=["Control the descent", "Drive through chest"]),
                Exercise(name="Incline Dumbbell Press", sets=3, reps="10-12", rest_seconds=75, technique_cues=["30-45 degree angle", "Full range of motion"]),
                Exercise(name="Overhead Press", sets=3, reps="8-10", rest_seconds=90, technique_cues=["Brace core", "Lock out at top"]),
                Exercise(name="Dumbbell Lateral Raises", sets=3, reps="12-15", rest_seconds=60, technique_cues=["Slight bend in elbows", "Control the weight"]),
                Exercise(name="Tricep Dips / Bench Dips", sets=3, reps="10-12", rest_seconds=60, technique_cues=["Elbows back", "Full lockout"]),
                Exercise(name="Tricep Pushdowns", sets=3, reps="12-15", rest_seconds=45, technique_cues=["Keep elbows pinned", "Squeeze at bottom"]),
                # Core
                Exercise(name="Plank", sets=3, reps="45-60 seconds", rest_seconds=30, technique_cues=["Keep hips level", "Engage entire core"]),
                Exercise(name="Mountain Climbers", sets=3, reps="20 each leg", rest_seconds=30, technique_cues=["Keep hips stable"]),
                # Stretching
                Exercise(name="Chest Doorway Stretch", sets=2, reps="30 seconds each", rest_seconds=0, technique_cues=["Hold stretch, breathe"]),
                Exercise(name="Tricep Overhead Stretch", sets=2, reps="30 seconds each arm", rest_seconds=0, technique_cues=["Gentle pull"]),
            ]
        },
        # Day 2: Pull (Back, Biceps)
        {
            "day_name": "Pull Day",
            "focus": "Back, Biceps, Rear Delts",
            "exercises": [
                # Warmup
                Exercise(name="Cat-Cow Stretch", sets=2, reps="10", rest_seconds=0, technique_cues=["Slow controlled movement"]),
                Exercise(name="Band Pull-Aparts", sets=2, reps="15", rest_seconds=0, technique_cues=["Squeeze shoulder blades"]),
                Exercise(name="Dead Hang", sets=2, reps="20-30 seconds", rest_seconds=30, technique_cues=["Relax shoulders"]),
                # Main exercises
                Exercise(name="Pull-ups / Lat Pulldown", sets=4, reps="8-12", rest_seconds=90, technique_cues=["Lead with chest", "Full stretch at bottom"]),
                Exercise(name="Barbell / Dumbbell Rows", sets=4, reps="8-12", rest_seconds=75, technique_cues=["Pull to hip", "Squeeze at top"]),
                Exercise(name="Seated Cable Row", sets=3, reps="10-12", rest_seconds=60, technique_cues=["Keep chest up", "Retract scapula"]),
                Exercise(name="Face Pulls", sets=3, reps="15", rest_seconds=45, technique_cues=["External rotation at end", "High pull"]),
                Exercise(name="Dumbbell Bicep Curls", sets=3, reps="10-12", rest_seconds=60, technique_cues=["Control the negative", "Full range"]),
                Exercise(name="Hammer Curls", sets=3, reps="12", rest_seconds=45, technique_cues=["Neutral grip", "No swinging"]),
                # Core
                Exercise(name="Dead Bug", sets=3, reps="10 each side", rest_seconds=30, technique_cues=["Keep lower back pressed down"]),
                Exercise(name="Superman Hold", sets=3, reps="30 seconds", rest_seconds=30, technique_cues=["Squeeze glutes"]),
                # Stretching
                Exercise(name="Lat Stretch", sets=2, reps="30 seconds each side", rest_seconds=0, technique_cues=["Hold and breathe"]),
                Exercise(name="Child's Pose", sets=1, reps="60 seconds", rest_seconds=0, technique_cues=["Relax completely"]),
            ]
        },
        # Day 3: Legs (Quads, Hamstrings, Glutes)
        {
            "day_name": "Legs Day",
            "focus": "Quads, Hamstrings, Glutes, Calves",
            "exercises": [
                # Warmup
                Exercise(name="Leg Swings", sets=2, reps="15 each leg", rest_seconds=0, technique_cues=["Front to back, side to side"]),
                Exercise(name="Bodyweight Squats", sets=2, reps="15", rest_seconds=0, technique_cues=["Full depth, controlled"]),
                Exercise(name="Walking Lunges", sets=2, reps="10 each leg", rest_seconds=30, technique_cues=["Knee tracks over toe"]),
                # Main exercises
                Exercise(name="Barbell Squat / Goblet Squat", sets=4, reps="8-10", rest_seconds=120, technique_cues=["Break at hips", "Chest up", "Push knees out"]),
                Exercise(name="Romanian Deadlift", sets=4, reps="10-12", rest_seconds=90, technique_cues=["Hinge at hips", "Slight knee bend"]),
                Exercise(name="Leg Press / Bulgarian Split Squat", sets=3, reps="10-12 each", rest_seconds=75, technique_cues=["Full range of motion"]),
                Exercise(name="Leg Curls", sets=3, reps="12-15", rest_seconds=60, technique_cues=["Control the eccentric"]),
                Exercise(name="Leg Extensions", sets=3, reps="12-15", rest_seconds=60, technique_cues=["Squeeze at top"]),
                Exercise(name="Standing Calf Raises", sets=4, reps="15-20", rest_seconds=45, technique_cues=["Full stretch at bottom", "Pause at top"]),
                # Core
                Exercise(name="Hanging Leg Raises / Knee Raises", sets=3, reps="12-15", rest_seconds=45, technique_cues=["Control the swing"]),
                Exercise(name="Russian Twists", sets=3, reps="20 total", rest_seconds=30, technique_cues=["Rotate from core"]),
                # Stretching
                Exercise(name="Quad Stretch", sets=2, reps="30 seconds each", rest_seconds=0, technique_cues=["Hold stable"]),
                Exercise(name="Hamstring Stretch", sets=2, reps="30 seconds each", rest_seconds=0, technique_cues=["Keep leg straight"]),
                Exercise(name="Pigeon Pose", sets=2, reps="45 seconds each", rest_seconds=0, technique_cues=["Hip opener, breathe"]),
            ]
        },
        # Day 4: Upper Body (Combination)
        {
            "day_name": "Upper Body",
            "focus": "Full Upper Body",
            "exercises": [
                # Warmup
                Exercise(name="Jumping Jacks", sets=2, reps="30 seconds", rest_seconds=0, technique_cues=["Light cardio warmup"]),
                Exercise(name="Arm Circles", sets=2, reps="20 each direction", rest_seconds=0, technique_cues=["Increase range"]),
                Exercise(name="Inchworms", sets=2, reps="8", rest_seconds=30, technique_cues=["Walk hands out, walk back"]),
                # Main exercises
                Exercise(name="Dumbbell Bench Press", sets=3, reps="10-12", rest_seconds=75, technique_cues=["Squeeze chest at top"]),
                Exercise(name="One-Arm Dumbbell Row", sets=3, reps="10 each", rest_seconds=60, technique_cues=["Drive elbow back"]),
                Exercise(name="Arnold Press", sets=3, reps="10", rest_seconds=60, technique_cues=["Rotate as you press"]),
                Exercise(name="Incline Dumbbell Flyes", sets=3, reps="12", rest_seconds=60, technique_cues=["Slight elbow bend"]),
                Exercise(name="Straight Arm Pulldown", sets=3, reps="12-15", rest_seconds=45, technique_cues=["Engage lats"]),
                Exercise(name="EZ Bar Curl", sets=3, reps="12", rest_seconds=45, technique_cues=["Controlled tempo"]),
                Exercise(name="Overhead Tricep Extension", sets=3, reps="12", rest_seconds=45, technique_cues=["Keep elbows in"]),
                # Core
                Exercise(name="Bicycle Crunches", sets=3, reps="20 each side", rest_seconds=30, technique_cues=["Touch elbow to knee"]),
                Exercise(name="Plank Shoulder Taps", sets=3, reps="10 each side", rest_seconds=30, technique_cues=["Minimize hip rotation"]),
                # Stretching
                Exercise(name="Cross-Body Shoulder Stretch", sets=2, reps="30 seconds each", rest_seconds=0, technique_cues=["Hold gently"]),
                Exercise(name="Neck Stretches", sets=2, reps="20 seconds each side", rest_seconds=0, technique_cues=["Gentle tilt"]),
            ]
        },
        # Day 5: Lower Body & Core Focus
        {
            "day_name": "Lower & Core",
            "focus": "Glutes, Hamstrings, Core",
            "exercises": [
                # Warmup
                Exercise(name="Hip Circles", sets=2, reps="10 each direction", rest_seconds=0, technique_cues=["Open up hips"]),
                Exercise(name="Glute Bridges", sets=2, reps="15", rest_seconds=0, technique_cues=["Squeeze glutes at top"]),
                Exercise(name="Fire Hydrants", sets=2, reps="12 each leg", rest_seconds=30, technique_cues=["Control the movement"]),
                # Main exercises
                Exercise(name="Hip Thrusts", sets=4, reps="12", rest_seconds=75, technique_cues=["Drive through heels", "Squeeze at top"]),
                Exercise(name="Sumo Deadlift / Sumo Squat", sets=4, reps="10", rest_seconds=90, technique_cues=["Wide stance", "Chest up"]),
                Exercise(name="Step-Ups", sets=3, reps="12 each leg", rest_seconds=60, technique_cues=["Push through heel"]),
                Exercise(name="Good Mornings", sets=3, reps="12", rest_seconds=60, technique_cues=["Hinge at hips", "Keep back straight"]),
                Exercise(name="Cable Kickbacks / Donkey Kicks", sets=3, reps="15 each", rest_seconds=45, technique_cues=["Squeeze glute"]),
                Exercise(name="Seated Calf Raises", sets=3, reps="15-20", rest_seconds=45, technique_cues=["Full contraction"]),
                # Core
                Exercise(name="Ab Wheel Rollout / Plank", sets=3, reps="10", rest_seconds=45, technique_cues=["Brace core throughout"]),
                Exercise(name="Side Plank", sets=3, reps="30 seconds each", rest_seconds=30, technique_cues=["Keep hips elevated"]),
                Exercise(name="Reverse Crunches", sets=3, reps="15", rest_seconds=30, technique_cues=["Lift hips off ground"]),
                # Stretching
                Exercise(name="90-90 Hip Stretch", sets=2, reps="45 seconds each", rest_seconds=0, technique_cues=["Sink into stretch"]),
                Exercise(name="Figure-4 Stretch", sets=2, reps="30 seconds each", rest_seconds=0, technique_cues=["Relax and breathe"]),
                Exercise(name="Standing Quad Stretch", sets=2, reps="30 seconds each", rest_seconds=0, technique_cues=["Hold balance"]),
            ]
        },
    ]
    
    workouts = []
    for d in range(min(days, 5)):
        template = workout_templates[d]
        workouts.append(DailyWorkout(
            day_number=d + 1,
            day_name=template["day_name"],
            focus=template["focus"],
            exercises=template["exercises"],
            estimated_duration_minutes=60,
        ))
    
    return TrainingProgram(
        program_name=f"{exp_level.title()} 5-Day Push/Pull/Legs Program",
        program_length_weeks=4,
        weekly_split="Push/Pull/Legs/Upper/Lower",
        weekly_schedules=[WeeklySchedule(week_number=1, workouts=workouts)],
        progression_rules=[
            ProgressionRule(
                rule_type="double_progression",
                condition="Complete all reps with good form for 2 sessions",
                action="Add 1-2 reps, then increase weight by 2.5-5kg"
            ),
            ProgressionRule(
                rule_type="deload",
                condition="Every 4th week or when fatigue is high",
                action="Reduce weight by 10-15%, focus on form"
            )
        ],
        difficulty_level=exp_level,
        goals_addressed=["Muscle Building", "Strength", "General Fitness"],
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
