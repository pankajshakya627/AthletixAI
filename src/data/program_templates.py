"""
Program Templates for Different Experience Levels.

Provides pre-built workout structures optimized for each level:
- Beginner: 3 days, full body, simple movements
- Intermediate: 5 days, Push/Pull/Legs, progressive overload
- Advanced: 6 days, body part split, high volume
"""

from src.data.exercise_library import EXERCISE_LIBRARY, get_exercises_for_level


# ============================================================================
# BEGINNER TEMPLATE - 3 Day Full Body
# ============================================================================

BEGINNER_TEMPLATE = {
    "program_name": "Beginner Full Body Foundation",
    "program_length_weeks": 4,
    "weekly_split": "Full Body A/B/A",
    "days_per_week": 3,
    "description": "Build foundational strength with simple, safe movements",
    "workouts": [
        {
            "day_name": "Full Body A",
            "focus": "Push, Squat, Core",
            "sections": {
                "warmup": [
                    {"name": "Arm Circles", "sets": 2, "reps": "30 seconds"},
                    {"name": "Leg Swings", "sets": 2, "reps": "15 each leg"},
                    {"name": "Cat-Cow Stretch", "sets": 2, "reps": "10"},
                ],
                "main": [
                    {"name": "Bodyweight Squat", "sets": 3, "reps": "12-15"},
                    {"name": "Push-up", "sets": 3, "reps": "8-12", "alternative": "Knee Push-up"},
                    {"name": "Dumbbell Row", "sets": 3, "reps": "10-12"},
                    {"name": "Glute Bridge", "sets": 3, "reps": "12-15"},
                    {"name": "Plank", "sets": 3, "reps": "30 seconds"},
                ],
                "cooldown": [
                    {"name": "World's Greatest Stretch", "sets": 2, "reps": "5 each side"},
                ],
            },
        },
        {
            "day_name": "Full Body B",
            "focus": "Pull, Hinge, Core",
            "sections": {
                "warmup": [
                    {"name": "Shoulder Rolls", "sets": 2, "reps": "15 each direction"},
                    {"name": "Hip Circles", "sets": 2, "reps": "10 each direction"},
                    {"name": "Inchworm", "sets": 2, "reps": "5"},
                ],
                "main": [
                    {"name": "Goblet Squat", "sets": 3, "reps": "10-12"},
                    {"name": "Lat Pulldown", "sets": 3, "reps": "10-12", "alternative": "Assisted Pull-up"},
                    {"name": "Dumbbell Shoulder Press", "sets": 3, "reps": "10-12"},
                    {"name": "Walking Lunge", "sets": 3, "reps": "10 each leg"},
                    {"name": "Dead Bug", "sets": 3, "reps": "10 each side"},
                ],
                "cooldown": [
                    {"name": "Cat-Cow Stretch", "sets": 2, "reps": "10"},
                ],
            },
        },
        {
            "day_name": "Full Body A (Repeat)",
            "focus": "Push, Squat, Core",
            "sections": "same_as_day_1",
        },
    ],
    "progression_rules": [
        "Add 1-2 reps per set each week",
        "When you can do 15+ reps with good form, increase weight",
        "Focus on form over weight",
    ],
}


# ============================================================================
# INTERMEDIATE TEMPLATE - 5 Day Push/Pull/Legs
# ============================================================================

INTERMEDIATE_TEMPLATE = {
    "program_name": "Intermediate 5-Day PPL",
    "program_length_weeks": 4,
    "weekly_split": "Push/Pull/Legs/Upper/Lower",
    "days_per_week": 5,
    "description": "Build muscle and strength with progressive overload",
    "workouts": [
        {
            "day_name": "Push Day",
            "focus": "Chest, Shoulders, Triceps",
            "sections": {
                "warmup": [
                    {"name": "Arm Circles", "sets": 2, "reps": "30 seconds"},
                    {"name": "Band Pull-Apart", "sets": 2, "reps": "15"},
                    {"name": "Push-up to Downward Dog", "sets": 2, "reps": "8"},
                ],
                "main": [
                    {"name": "Bench Press", "sets": 4, "reps": "6-8"},
                    {"name": "Incline Dumbbell Press", "sets": 3, "reps": "8-10"},
                    {"name": "Overhead Press", "sets": 3, "reps": "8-10"},
                    {"name": "Dumbbell Lateral Raise", "sets": 3, "reps": "12-15"},
                    {"name": "Tricep Pushdown", "sets": 3, "reps": "10-12"},
                    {"name": "Overhead Tricep Extension", "sets": 3, "reps": "10-12"},
                ],
                "cooldown": [
                    {"name": "Chest Stretch", "sets": 2, "reps": "30 seconds each side"},
                ],
            },
        },
        {
            "day_name": "Pull Day",
            "focus": "Back, Biceps, Rear Delts",
            "sections": {
                "warmup": [
                    {"name": "Cat-Cow Stretch", "sets": 2, "reps": "10"},
                    {"name": "Band Pull-Apart", "sets": 2, "reps": "15"},
                    {"name": "Dead Hang", "sets": 2, "reps": "20-30 seconds"},
                ],
                "main": [
                    {"name": "Pull-up", "sets": 4, "reps": "6-10", "alternative": "Lat Pulldown"},
                    {"name": "Barbell Row", "sets": 4, "reps": "8-10"},
                    {"name": "Seated Cable Row", "sets": 3, "reps": "10-12"},
                    {"name": "Face Pull", "sets": 3, "reps": "15-20"},
                    {"name": "Barbell Curl", "sets": 3, "reps": "10-12"},
                    {"name": "Hammer Curl", "sets": 3, "reps": "10-12"},
                ],
                "cooldown": [
                    {"name": "Lat Stretch", "sets": 2, "reps": "30 seconds each side"},
                ],
            },
        },
        {
            "day_name": "Legs Day",
            "focus": "Quads, Hamstrings, Glutes, Calves",
            "sections": {
                "warmup": [
                    {"name": "Leg Swings", "sets": 2, "reps": "15 each leg"},
                    {"name": "Bodyweight Squat", "sets": 2, "reps": "15"},
                    {"name": "Walking Lunge", "sets": 2, "reps": "10 each leg"},
                ],
                "main": [
                    {"name": "Squat", "sets": 4, "reps": "6-8"},
                    {"name": "Romanian Deadlift", "sets": 3, "reps": "8-10"},
                    {"name": "Leg Press", "sets": 3, "reps": "10-12"},
                    {"name": "Leg Curl", "sets": 3, "reps": "10-12"},
                    {"name": "Bulgarian Split Squat", "sets": 3, "reps": "10 each leg"},
                    {"name": "Calf Raise", "sets": 4, "reps": "15-20"},
                ],
                "cooldown": [
                    {"name": "Hamstring Stretch", "sets": 2, "reps": "30 seconds each leg"},
                ],
            },
        },
        {
            "day_name": "Upper Day",
            "focus": "Chest, Back, Shoulders, Arms",
            "sections": {
                "warmup": [
                    {"name": "Arm Circles", "sets": 2, "reps": "30 seconds"},
                    {"name": "Band Pull-Apart", "sets": 2, "reps": "15"},
                ],
                "main": [
                    {"name": "Incline Bench Press", "sets": 3, "reps": "8-10"},
                    {"name": "Chin-up", "sets": 3, "reps": "6-10"},
                    {"name": "Dumbbell Shoulder Press", "sets": 3, "reps": "10-12"},
                    {"name": "Dumbbell Row", "sets": 3, "reps": "10-12"},
                    {"name": "Dumbbell Bicep Curl", "sets": 3, "reps": "10-12"},
                    {"name": "Tricep Dip", "sets": 3, "reps": "8-12"},
                ],
                "cooldown": [
                    {"name": "Shoulder Stretch", "sets": 2, "reps": "30 seconds each"},
                ],
            },
        },
        {
            "day_name": "Lower Day",
            "focus": "Quads, Glutes, Hamstrings",
            "sections": {
                "warmup": [
                    {"name": "Hip Circles", "sets": 2, "reps": "10 each direction"},
                    {"name": "Leg Swings", "sets": 2, "reps": "15 each leg"},
                ],
                "main": [
                    {"name": "Deadlift", "sets": 4, "reps": "5-6"},
                    {"name": "Goblet Squat", "sets": 3, "reps": "10-12"},
                    {"name": "Hip Thrust", "sets": 3, "reps": "10-12"},
                    {"name": "Walking Lunge", "sets": 3, "reps": "12 each leg"},
                    {"name": "Leg Extension", "sets": 3, "reps": "12-15"},
                    {"name": "Seated Calf Raise", "sets": 3, "reps": "15-20"},
                ],
                "cooldown": [
                    {"name": "Glute Stretch", "sets": 2, "reps": "30 seconds each"},
                ],
            },
        },
    ],
    "progression_rules": [
        "Increase weight by 2.5-5 lbs when you hit the top of rep range",
        "Deload every 4th week (reduce volume by 40%)",
        "Track your lifts - aim for progressive overload",
    ],
}


# ============================================================================
# ADVANCED TEMPLATE - 6 Day Body Part Split
# ============================================================================

ADVANCED_TEMPLATE = {
    "program_name": "Advanced 6-Day Body Part Split",
    "program_length_weeks": 4,
    "weekly_split": "Push/Pull/Legs/Push/Pull/Legs",
    "days_per_week": 6,
    "description": "High volume training for advanced muscle development",
    "workouts": [
        {
            "day_name": "Push A - Heavy",
            "focus": "Chest, Shoulders, Triceps",
            "sections": {
                "warmup": [
                    {"name": "Band Pull-Apart", "sets": 3, "reps": "15"},
                    {"name": "Arm Circles", "sets": 2, "reps": "30 seconds"},
                ],
                "main": [
                    {"name": "Bench Press", "sets": 5, "reps": "5"},
                    {"name": "Overhead Press", "sets": 4, "reps": "6"},
                    {"name": "Incline Dumbbell Press", "sets": 4, "reps": "8"},
                    {"name": "Dumbbell Flyes", "sets": 3, "reps": "12"},
                    {"name": "Dumbbell Lateral Raise", "sets": 4, "reps": "12"},
                    {"name": "Skull Crusher", "sets": 3, "reps": "10"},
                    {"name": "Tricep Pushdown", "sets": 3, "reps": "12"},
                ],
            },
        },
        {
            "day_name": "Pull A - Heavy",
            "focus": "Back, Biceps",
            "sections": {
                "warmup": [
                    {"name": "Dead Hang", "sets": 2, "reps": "30 seconds"},
                    {"name": "Band Pull-Apart", "sets": 2, "reps": "15"},
                ],
                "main": [
                    {"name": "Deadlift", "sets": 5, "reps": "5"},
                    {"name": "Pull-up", "sets": 4, "reps": "6-8"},
                    {"name": "Barbell Row", "sets": 4, "reps": "6-8"},
                    {"name": "T-bar Row", "sets": 3, "reps": "10"},
                    {"name": "Face Pull", "sets": 4, "reps": "15"},
                    {"name": "Barbell Curl", "sets": 3, "reps": "10"},
                    {"name": "Hammer Curl", "sets": 3, "reps": "12"},
                ],
            },
        },
        {
            "day_name": "Legs A - Quad Focus",
            "focus": "Quads, Glutes, Calves",
            "sections": {
                "warmup": [
                    {"name": "Leg Swings", "sets": 2, "reps": "15 each"},
                    {"name": "Bodyweight Squat", "sets": 2, "reps": "15"},
                ],
                "main": [
                    {"name": "Squat", "sets": 5, "reps": "5"},
                    {"name": "Front Squat", "sets": 4, "reps": "8"},
                    {"name": "Leg Press", "sets": 4, "reps": "12"},
                    {"name": "Bulgarian Split Squat", "sets": 3, "reps": "10 each"},
                    {"name": "Leg Extension", "sets": 3, "reps": "15"},
                    {"name": "Calf Raise", "sets": 4, "reps": "15"},
                ],
            },
        },
        {
            "day_name": "Push B - Volume",
            "focus": "Chest, Shoulders, Triceps",
            "sections": {
                "main": [
                    {"name": "Incline Bench Press", "sets": 4, "reps": "8"},
                    {"name": "Dumbbell Chest Press", "sets": 4, "reps": "10"},
                    {"name": "Cable Crossover", "sets": 3, "reps": "12"},
                    {"name": "Arnold Press", "sets": 4, "reps": "10"},
                    {"name": "Dumbbell Lateral Raise", "sets": 4, "reps": "15"},
                    {"name": "Overhead Tricep Extension", "sets": 3, "reps": "12"},
                    {"name": "Diamond Push-up", "sets": 3, "reps": "AMRAP"},
                ],
            },
        },
        {
            "day_name": "Pull B - Volume",
            "focus": "Back, Biceps",
            "sections": {
                "main": [
                    {"name": "Chin-up", "sets": 4, "reps": "8"},
                    {"name": "Seated Cable Row", "sets": 4, "reps": "10"},
                    {"name": "Lat Pulldown", "sets": 4, "reps": "12"},
                    {"name": "Dumbbell Row", "sets": 3, "reps": "10 each"},
                    {"name": "Rope Face Pull", "sets": 4, "reps": "15"},
                    {"name": "Concentration Curl", "sets": 3, "reps": "12"},
                    {"name": "Wrist Curl", "sets": 3, "reps": "15"},
                ],
            },
        },
        {
            "day_name": "Legs B - Hamstring Focus",
            "focus": "Hamstrings, Glutes",
            "sections": {
                "main": [
                    {"name": "Romanian Deadlift", "sets": 4, "reps": "8"},
                    {"name": "Hip Thrust", "sets": 4, "reps": "10"},
                    {"name": "Leg Curl", "sets": 4, "reps": "12"},
                    {"name": "Walking Lunge", "sets": 3, "reps": "12 each"},
                    {"name": "Step-up", "sets": 3, "reps": "10 each"},
                    {"name": "Kettlebell Swing", "sets": 3, "reps": "15"},
                    {"name": "Seated Calf Raise", "sets": 4, "reps": "15"},
                ],
            },
        },
    ],
    "progression_rules": [
        "Heavy days: increase weight when you hit all reps",
        "Volume days: add sets or reps before increasing weight",
        "Deload every 4th week",
        "Prioritize recovery - sleep and nutrition are critical",
    ],
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_template_for_level(level: str) -> dict:
    """Get the appropriate program template for experience level."""
    templates = {
        "beginner": BEGINNER_TEMPLATE,
        "intermediate": INTERMEDIATE_TEMPLATE,
        "advanced": ADVANCED_TEMPLATE,
        "elite": ADVANCED_TEMPLATE,  # Elite uses advanced template with modifications
    }
    return templates.get(level.lower(), INTERMEDIATE_TEMPLATE)


def get_exercise_alternatives(exercise_name: str, user_level: str) -> list[str]:
    """Get alternative exercises suitable for user's level."""
    from src.data.exercise_library import EXERCISE_LIBRARY
    
    # Get the original exercise info
    original = EXERCISE_LIBRARY.get(exercise_name.lower())
    if not original:
        return []
    
    # Find exercises targeting same muscles at appropriate level
    alternatives = []
    target_muscles = set(original["muscles"])
    
    for name, ex in EXERCISE_LIBRARY.items():
        if name == exercise_name.lower():
            continue
        if user_level not in ex["difficulty"]:
            continue
        # Check muscle overlap
        if target_muscles.intersection(set(ex["muscles"])):
            alternatives.append(name)
    
    return alternatives[:3]  # Return top 3 alternatives
