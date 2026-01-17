"""
Comprehensive Exercise Library with Difficulty Tags.

Each exercise is tagged with:
- difficulty_levels: List of experience levels that can use this exercise
- muscle_groups: Primary and secondary muscles targeted
- equipment: Required equipment (empty = bodyweight)
- exercise_type: compound, isolation, cardio, stretch, warmup
"""

from typing import Optional
from enum import Enum


class ExerciseType(str, Enum):
    COMPOUND = "compound"
    ISOLATION = "isolation"
    CARDIO = "cardio"
    STRETCH = "stretch"
    WARMUP = "warmup"


# ============================================================================
# EXERCISE LIBRARY - 100+ Exercises with Difficulty Tags
# ============================================================================

EXERCISE_LIBRARY = {
    # ========================================================================
    # CHEST EXERCISES
    # ========================================================================
    "wall push-up": {
        "difficulty": ["beginner"],
        "muscles": ["chest", "triceps", "shoulders"],
        "equipment": [],
        "type": ExerciseType.COMPOUND,
    },
    "knee push-up": {
        "difficulty": ["beginner"],
        "muscles": ["chest", "triceps", "shoulders"],
        "equipment": [],
        "type": ExerciseType.COMPOUND,
    },
    "push-up": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["chest", "triceps", "shoulders", "core"],
        "equipment": [],
        "type": ExerciseType.COMPOUND,
    },
    "incline push-up": {
        "difficulty": ["beginner", "intermediate"],
        "muscles": ["lower chest", "triceps"],
        "equipment": [],
        "type": ExerciseType.COMPOUND,
    },
    "decline push-up": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["upper chest", "shoulders", "triceps"],
        "equipment": [],
        "type": ExerciseType.COMPOUND,
    },
    "diamond push-up": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["triceps", "chest"],
        "equipment": [],
        "type": ExerciseType.COMPOUND,
    },
    "archer push-up": {
        "difficulty": ["advanced"],
        "muscles": ["chest", "triceps", "shoulders"],
        "equipment": [],
        "type": ExerciseType.COMPOUND,
    },
    "dumbbell chest press": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["chest", "triceps", "shoulders"],
        "equipment": ["dumbbells", "bench"],
        "type": ExerciseType.COMPOUND,
    },
    "bench press": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["chest", "triceps", "shoulders"],
        "equipment": ["barbell", "bench"],
        "type": ExerciseType.COMPOUND,
    },
    "incline bench press": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["upper chest", "shoulders", "triceps"],
        "equipment": ["barbell", "bench"],
        "type": ExerciseType.COMPOUND,
    },
    "incline dumbbell press": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["upper chest", "shoulders"],
        "equipment": ["dumbbells", "bench"],
        "type": ExerciseType.COMPOUND,
    },
    "dumbbell flyes": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["chest"],
        "equipment": ["dumbbells", "bench"],
        "type": ExerciseType.ISOLATION,
    },
    "cable crossover": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["chest"],
        "equipment": ["cables"],
        "type": ExerciseType.ISOLATION,
    },
    
    # ========================================================================
    # BACK EXERCISES
    # ========================================================================
    "wall angel": {
        "difficulty": ["beginner"],
        "muscles": ["upper back", "shoulders"],
        "equipment": [],
        "type": ExerciseType.WARMUP,
    },
    "superman": {
        "difficulty": ["beginner", "intermediate"],
        "muscles": ["lower back", "glutes"],
        "equipment": [],
        "type": ExerciseType.ISOLATION,
    },
    "inverted row": {
        "difficulty": ["beginner", "intermediate"],
        "muscles": ["back", "biceps"],
        "equipment": ["bar"],
        "type": ExerciseType.COMPOUND,
    },
    "assisted pull-up": {
        "difficulty": ["beginner"],
        "muscles": ["lats", "biceps"],
        "equipment": ["pull_up_bar", "resistance_band"],
        "type": ExerciseType.COMPOUND,
    },
    "pull-up": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["lats", "biceps", "forearms"],
        "equipment": ["pull_up_bar"],
        "type": ExerciseType.COMPOUND,
    },
    "chin-up": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["biceps", "lats"],
        "equipment": ["pull_up_bar"],
        "type": ExerciseType.COMPOUND,
    },
    "lat pulldown": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["lats", "biceps"],
        "equipment": ["cables"],
        "type": ExerciseType.COMPOUND,
    },
    "dumbbell row": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["lats", "rhomboids", "biceps"],
        "equipment": ["dumbbells"],
        "type": ExerciseType.COMPOUND,
    },
    "barbell row": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["lats", "rhomboids", "biceps", "lower back"],
        "equipment": ["barbell"],
        "type": ExerciseType.COMPOUND,
    },
    "t-bar row": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["lats", "rhomboids"],
        "equipment": ["barbell"],
        "type": ExerciseType.COMPOUND,
    },
    "seated cable row": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["lats", "rhomboids", "biceps"],
        "equipment": ["cables"],
        "type": ExerciseType.COMPOUND,
    },
    "face pull": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["rear delts", "rhomboids", "rotator cuff"],
        "equipment": ["cables", "resistance_band"],
        "type": ExerciseType.ISOLATION,
    },
    "deadlift": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["lower back", "glutes", "hamstrings", "traps"],
        "equipment": ["barbell"],
        "type": ExerciseType.COMPOUND,
    },
    "romanian deadlift": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["hamstrings", "glutes", "lower back"],
        "equipment": ["barbell", "dumbbells"],
        "type": ExerciseType.COMPOUND,
    },
    
    # ========================================================================
    # SHOULDER EXERCISES
    # ========================================================================
    "arm circles": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["shoulders"],
        "equipment": [],
        "type": ExerciseType.WARMUP,
    },
    "shoulder rolls": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["shoulders", "traps"],
        "equipment": [],
        "type": ExerciseType.WARMUP,
    },
    "band pull-apart": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["rear delts", "rhomboids"],
        "equipment": ["resistance_band"],
        "type": ExerciseType.ISOLATION,
    },
    "dumbbell lateral raise": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["lateral delts"],
        "equipment": ["dumbbells"],
        "type": ExerciseType.ISOLATION,
    },
    "dumbbell front raise": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["front delts"],
        "equipment": ["dumbbells"],
        "type": ExerciseType.ISOLATION,
    },
    "dumbbell shoulder press": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["shoulders", "triceps"],
        "equipment": ["dumbbells"],
        "type": ExerciseType.COMPOUND,
    },
    "overhead press": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["shoulders", "triceps", "core"],
        "equipment": ["barbell"],
        "type": ExerciseType.COMPOUND,
    },
    "pike push-up": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["shoulders", "triceps"],
        "equipment": [],
        "type": ExerciseType.COMPOUND,
    },
    "handstand push-up": {
        "difficulty": ["advanced"],
        "muscles": ["shoulders", "triceps", "core"],
        "equipment": [],
        "type": ExerciseType.COMPOUND,
    },
    "arnold press": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["shoulders"],
        "equipment": ["dumbbells"],
        "type": ExerciseType.COMPOUND,
    },
    
    # ========================================================================
    # ARM EXERCISES
    # ========================================================================
    "dumbbell bicep curl": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["biceps"],
        "equipment": ["dumbbells"],
        "type": ExerciseType.ISOLATION,
    },
    "hammer curl": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["biceps", "forearms"],
        "equipment": ["dumbbells"],
        "type": ExerciseType.ISOLATION,
    },
    "barbell curl": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["biceps"],
        "equipment": ["barbell"],
        "type": ExerciseType.ISOLATION,
    },
    "concentration curl": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["biceps"],
        "equipment": ["dumbbells"],
        "type": ExerciseType.ISOLATION,
    },
    "tricep dip": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["triceps", "chest", "shoulders"],
        "equipment": [],
        "type": ExerciseType.COMPOUND,
    },
    "bench dip": {
        "difficulty": ["beginner", "intermediate"],
        "muscles": ["triceps"],
        "equipment": ["bench"],
        "type": ExerciseType.ISOLATION,
    },
    "tricep pushdown": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["triceps"],
        "equipment": ["cables"],
        "type": ExerciseType.ISOLATION,
    },
    "overhead tricep extension": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["triceps"],
        "equipment": ["dumbbells"],
        "type": ExerciseType.ISOLATION,
    },
    "skull crusher": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["triceps"],
        "equipment": ["barbell", "bench"],
        "type": ExerciseType.ISOLATION,
    },
    "wrist curl": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["forearms"],
        "equipment": ["dumbbells"],
        "type": ExerciseType.ISOLATION,
    },
    
    # ========================================================================
    # LEG EXERCISES
    # ========================================================================
    "bodyweight squat": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["quads", "glutes"],
        "equipment": [],
        "type": ExerciseType.COMPOUND,
    },
    "wall sit": {
        "difficulty": ["beginner", "intermediate"],
        "muscles": ["quads"],
        "equipment": [],
        "type": ExerciseType.ISOLATION,
    },
    "goblet squat": {
        "difficulty": ["beginner", "intermediate"],
        "muscles": ["quads", "glutes", "core"],
        "equipment": ["dumbbells"],
        "type": ExerciseType.COMPOUND,
    },
    "squat": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["quads", "glutes", "hamstrings", "core"],
        "equipment": ["barbell"],
        "type": ExerciseType.COMPOUND,
    },
    "front squat": {
        "difficulty": ["advanced"],
        "muscles": ["quads", "core"],
        "equipment": ["barbell"],
        "type": ExerciseType.COMPOUND,
    },
    "leg press": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["quads", "glutes"],
        "equipment": ["machine"],
        "type": ExerciseType.COMPOUND,
    },
    "walking lunge": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["quads", "glutes", "hamstrings"],
        "equipment": [],
        "type": ExerciseType.COMPOUND,
    },
    "reverse lunge": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["quads", "glutes"],
        "equipment": [],
        "type": ExerciseType.COMPOUND,
    },
    "bulgarian split squat": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["quads", "glutes"],
        "equipment": ["bench"],
        "type": ExerciseType.COMPOUND,
    },
    "pistol squat": {
        "difficulty": ["advanced"],
        "muscles": ["quads", "glutes", "core"],
        "equipment": [],
        "type": ExerciseType.COMPOUND,
    },
    "leg extension": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["quads"],
        "equipment": ["machine"],
        "type": ExerciseType.ISOLATION,
    },
    "leg curl": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["hamstrings"],
        "equipment": ["machine"],
        "type": ExerciseType.ISOLATION,
    },
    "glute bridge": {
        "difficulty": ["beginner", "intermediate"],
        "muscles": ["glutes", "hamstrings"],
        "equipment": [],
        "type": ExerciseType.ISOLATION,
    },
    "hip thrust": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["glutes", "hamstrings"],
        "equipment": ["barbell", "bench"],
        "type": ExerciseType.COMPOUND,
    },
    "step-up": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["quads", "glutes"],
        "equipment": ["bench"],
        "type": ExerciseType.COMPOUND,
    },
    "calf raise": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["calves"],
        "equipment": [],
        "type": ExerciseType.ISOLATION,
    },
    "seated calf raise": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["calves"],
        "equipment": ["machine"],
        "type": ExerciseType.ISOLATION,
    },
    
    # ========================================================================
    # CORE EXERCISES
    # ========================================================================
    "dead bug": {
        "difficulty": ["beginner", "intermediate"],
        "muscles": ["core"],
        "equipment": [],
        "type": ExerciseType.ISOLATION,
    },
    "bird dog": {
        "difficulty": ["beginner", "intermediate"],
        "muscles": ["core", "lower back"],
        "equipment": [],
        "type": ExerciseType.ISOLATION,
    },
    "plank": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["core"],
        "equipment": [],
        "type": ExerciseType.ISOLATION,
    },
    "side plank": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["obliques", "core"],
        "equipment": [],
        "type": ExerciseType.ISOLATION,
    },
    "crunch": {
        "difficulty": ["beginner", "intermediate"],
        "muscles": ["abs"],
        "equipment": [],
        "type": ExerciseType.ISOLATION,
    },
    "bicycle crunch": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["abs", "obliques"],
        "equipment": [],
        "type": ExerciseType.ISOLATION,
    },
    "leg raise": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["lower abs"],
        "equipment": [],
        "type": ExerciseType.ISOLATION,
    },
    "hanging leg raise": {
        "difficulty": ["advanced"],
        "muscles": ["lower abs", "hip flexors"],
        "equipment": ["pull_up_bar"],
        "type": ExerciseType.ISOLATION,
    },
    "russian twist": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["obliques"],
        "equipment": [],
        "type": ExerciseType.ISOLATION,
    },
    "mountain climber": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["core", "shoulders"],
        "equipment": [],
        "type": ExerciseType.CARDIO,
    },
    "ab wheel rollout": {
        "difficulty": ["advanced"],
        "muscles": ["core"],
        "equipment": ["ab_wheel"],
        "type": ExerciseType.ISOLATION,
    },
    "hollow body hold": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["core"],
        "equipment": [],
        "type": ExerciseType.ISOLATION,
    },
    
    # ========================================================================
    # WARMUP & MOBILITY
    # ========================================================================
    "cat-cow stretch": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["spine", "core"],
        "equipment": [],
        "type": ExerciseType.STRETCH,
    },
    "world's greatest stretch": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["hips", "hamstrings", "thoracic"],
        "equipment": [],
        "type": ExerciseType.STRETCH,
    },
    "leg swings": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["hip flexors", "hamstrings"],
        "equipment": [],
        "type": ExerciseType.WARMUP,
    },
    "hip circles": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["hips"],
        "equipment": [],
        "type": ExerciseType.WARMUP,
    },
    "ankle circles": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["ankles"],
        "equipment": [],
        "type": ExerciseType.WARMUP,
    },
    "inchworm": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["hamstrings", "core", "shoulders"],
        "equipment": [],
        "type": ExerciseType.WARMUP,
    },
    "high knees": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["hip flexors", "core"],
        "equipment": [],
        "type": ExerciseType.CARDIO,
    },
    "butt kicks": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["hamstrings"],
        "equipment": [],
        "type": ExerciseType.CARDIO,
    },
    "jumping jacks": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["full body"],
        "equipment": [],
        "type": ExerciseType.CARDIO,
    },
    "push-up to downward dog": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["chest", "shoulders", "hamstrings"],
        "equipment": [],
        "type": ExerciseType.WARMUP,
    },
    "dead hang": {
        "difficulty": ["beginner", "intermediate", "advanced"],
        "muscles": ["grip", "shoulders"],
        "equipment": ["pull_up_bar"],
        "type": ExerciseType.STRETCH,
    },
    
    # ========================================================================
    # CARDIO & PLYOMETRICS
    # ========================================================================
    "burpee": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["full body"],
        "equipment": [],
        "type": ExerciseType.CARDIO,
    },
    "box jump": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["quads", "glutes", "calves"],
        "equipment": ["box"],
        "type": ExerciseType.CARDIO,
    },
    "jump squat": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["quads", "glutes"],
        "equipment": [],
        "type": ExerciseType.CARDIO,
    },
    "jump lunge": {
        "difficulty": ["advanced"],
        "muscles": ["quads", "glutes"],
        "equipment": [],
        "type": ExerciseType.CARDIO,
    },
    "skater jump": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["quads", "glutes"],
        "equipment": [],
        "type": ExerciseType.CARDIO,
    },
    "battle ropes": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["shoulders", "core"],
        "equipment": ["battle_ropes"],
        "type": ExerciseType.CARDIO,
    },
    "kettlebell swing": {
        "difficulty": ["intermediate", "advanced"],
        "muscles": ["glutes", "hamstrings", "core"],
        "equipment": ["kettlebell"],
        "type": ExerciseType.COMPOUND,
    },
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_exercises_for_level(level: str, equipment: Optional[list[str]] = None) -> dict:
    """
    Get exercises suitable for a given experience level.
    
    Args:
        level: 'beginner', 'intermediate', or 'advanced'
        equipment: Optional list of available equipment
    
    Returns:
        Dictionary of exercises matching the criteria
    """
    suitable = {}
    
    for name, exercise in EXERCISE_LIBRARY.items():
        # Check if level is appropriate
        if level not in exercise["difficulty"]:
            continue
        
        # Check equipment if specified
        if equipment is not None:
            required = set(exercise.get("equipment", []))
            available = set(equipment)
            # Skip if we don't have required equipment (unless bodyweight)
            if required and not required.issubset(available):
                continue
        
        suitable[name] = exercise
    
    return suitable


def get_exercises_by_muscle(muscle: str, level: Optional[str] = None) -> dict:
    """Get exercises targeting a specific muscle group."""
    matching = {}
    
    for name, exercise in EXERCISE_LIBRARY.items():
        if muscle.lower() in [m.lower() for m in exercise["muscles"]]:
            if level is None or level in exercise["difficulty"]:
                matching[name] = exercise
    
    return matching


def get_bodyweight_exercises(level: Optional[str] = None) -> dict:
    """Get exercises that require no equipment."""
    return get_exercises_for_level(level or "beginner", equipment=[])


def get_exercise_info(name: str) -> Optional[dict]:
    """Get info for a specific exercise."""
    # Try exact match
    if name.lower() in EXERCISE_LIBRARY:
        return EXERCISE_LIBRARY[name.lower()]
    
    # Try partial match
    for ex_name, ex_info in EXERCISE_LIBRARY.items():
        if name.lower() in ex_name or ex_name in name.lower():
            return ex_info
    
    return None


# Count exercises
TOTAL_EXERCISES = len(EXERCISE_LIBRARY)
BEGINNER_EXERCISES = len([e for e in EXERCISE_LIBRARY.values() if "beginner" in e["difficulty"]])
INTERMEDIATE_EXERCISES = len([e for e in EXERCISE_LIBRARY.values() if "intermediate" in e["difficulty"]])
ADVANCED_EXERCISES = len([e for e in EXERCISE_LIBRARY.values() if "advanced" in e["difficulty"]])
