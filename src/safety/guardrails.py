"""Safety guardrails for training recommendations."""

from typing import Any

# Maximum weekly volume caps by experience level (total sets)
MAX_WEEKLY_VOLUME = {
    "beginner": 60,
    "novice": 60,
    "intermediate": 100,
    "advanced": 140,
    "elite": 180,
}

# Maximum weekly progression rate (percentage)
MAX_WEEKLY_PROGRESSION = 10

# Minimum rest days per week by experience
MIN_REST_DAYS = {
    "beginner": 3,
    "novice": 3,
    "intermediate": 2,
    "advanced": 2,
    "elite": 1,
}


def apply_safety_limits(program: Any, user_profile: Any) -> Any:
    """
    Apply safety limits to a training program.
    
    Enforces:
    - Maximum volume caps
    - Minimum rest days
    - Injury-aware modifications
    
    Args:
        program: TrainingProgram instance
        user_profile: UserProfile instance
    
    Returns:
        Modified program with safety limits applied
    """
    if not program:
        return program
    
    # Get experience level
    exp_level = getattr(user_profile, "experience_level", "beginner")
    if hasattr(exp_level, "value"):
        exp_level = exp_level.value
    
    max_volume = MAX_WEEKLY_VOLUME.get(exp_level.lower(), 60)
    
    # Check and cap weekly volume
    for week in getattr(program, "weekly_schedules", []):
        total_sets = 0
        for workout in getattr(week, "workouts", []):
            for exercise in getattr(workout, "exercises", []):
                total_sets += getattr(exercise, "sets", 0)
        
        # If over limit, reduce proportionally
        if total_sets > max_volume:
            reduction_factor = max_volume / total_sets
            for workout in week.workouts:
                for exercise in workout.exercises:
                    exercise.sets = max(1, int(exercise.sets * reduction_factor))
    
    # Check for injury-related exercises
    current_injuries = getattr(user_profile, "current_injuries", [])
    if current_injuries:
        program = _apply_injury_modifications(program, current_injuries)
    
    return program


def _apply_injury_modifications(program: Any, injuries: list[str]) -> Any:
    """Modify program based on current injuries."""
    
    # Mapping of injury areas to exercises to avoid/modify
    injury_cautions = {
        "lower back": ["deadlift", "barbell row", "good morning"],
        "knee": ["deep squat", "leg extension", "jumping"],
        "shoulder": ["overhead press", "upright row", "behind neck"],
        "wrist": ["barbell curl", "push-up"],
    }
    
    injury_lower = [i.lower() for i in injuries]
    
    for week in getattr(program, "weekly_schedules", []):
        for workout in getattr(week, "workouts", []):
            exercises = getattr(workout, "exercises", [])
            filtered_exercises = []
            
            for exercise in exercises:
                exercise_lower = getattr(exercise, "name", "").lower()
                should_include = True
                
                for injury in injury_lower:
                    for key, avoid_exercises in injury_cautions.items():
                        if key in injury:
                            for avoid in avoid_exercises:
                                if avoid in exercise_lower:
                                    should_include = False
                                    break
                
                if should_include:
                    filtered_exercises.append(exercise)
            
            workout.exercises = filtered_exercises
    
    return program


def check_progression_safety(
    previous_weight: float,
    new_weight: float,
    max_percentage: float = MAX_WEEKLY_PROGRESSION
) -> tuple[bool, float]:
    """
    Check if a weight progression is within safe limits.
    
    Args:
        previous_weight: Previous working weight
        new_weight: Proposed new weight
        max_percentage: Maximum allowed increase
    
    Returns:
        Tuple of (is_safe, recommended_weight)
    """
    if previous_weight <= 0:
        return True, new_weight
    
    percentage_increase = ((new_weight - previous_weight) / previous_weight) * 100
    
    if percentage_increase <= max_percentage:
        return True, new_weight
    
    # Calculate safe progression
    safe_weight = previous_weight * (1 + max_percentage / 100)
    return False, safe_weight


def get_max_heart_rate(age: int) -> int:
    """Calculate estimated maximum heart rate."""
    return 220 - age


def get_training_zones(max_hr: int) -> dict[str, tuple[int, int]]:
    """Get heart rate training zones."""
    return {
        "recovery": (int(max_hr * 0.5), int(max_hr * 0.6)),
        "fat_burn": (int(max_hr * 0.6), int(max_hr * 0.7)),
        "cardio": (int(max_hr * 0.7), int(max_hr * 0.8)),
        "hard": (int(max_hr * 0.8), int(max_hr * 0.9)),
        "maximum": (int(max_hr * 0.9), max_hr),
    }
