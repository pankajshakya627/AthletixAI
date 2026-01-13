"""Main entry point for the AI Fitness Coach."""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from src.state import FitnessState, create_initial_state
from src.models.user_profile import UserProfile, FoodPreferences, FitnessGoals
from src.graph import get_compiled_graph
from src.memory.persistence import PersistenceManager
from src.safety.validators import validate_user_profile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_user_profile(profile_path: str) -> UserProfile:
    """Load user profile from JSON file."""
    with open(profile_path) as f:
        data = json.load(f)
    return UserProfile(**data)


def load_food_preferences(prefs_path: Optional[str]) -> Optional[FoodPreferences]:
    """Load food preferences from JSON file if provided."""
    if not prefs_path:
        return None
    with open(prefs_path) as f:
        data = json.load(f)
    return FoodPreferences(**data)


def load_goals(goals_path: Optional[str]) -> Optional[FitnessGoals]:
    """Load fitness goals from JSON file if provided."""
    if not goals_path:
        return None
    with open(goals_path) as f:
        data = json.load(f)
    return FitnessGoals(**data)


def load_wearable_data(wearable_path: Optional[str]) -> Optional[dict]:
    """Load wearable data from JSON file if provided."""
    if not wearable_path:
        return None
    with open(wearable_path) as f:
        return json.load(f)


# ============================================================
# INTERACTIVE PROFILE CREATION
# ============================================================

def create_profile_interactive() -> UserProfile:
    """
    Interactively prompt user for profile information.
    
    Returns:
        UserProfile created from user input
    """
    from src.models.user_profile import Gender, ExperienceLevel
    import uuid
    
    print("\n" + "=" * 60)
    print("📋 CREATE YOUR FITNESS PROFILE")
    print("=" * 60 + "\n")
    
    # Name
    name = input("👤 What's your name? ").strip()
    if not name:
        name = "User"
    
    # Age
    while True:
        try:
            age = int(input("🎂 Your age: "))
            if 13 <= age <= 100:
                break
            print("   Please enter an age between 13-100")
        except ValueError:
            print("   Please enter a valid number")
    
    # Gender
    print("\n🚻 Gender:")
    print("   1. Male")
    print("   2. Female")
    print("   3. Other")
    gender_choice = input("   Choose (1-3): ").strip()
    gender_map = {"1": Gender.MALE, "2": Gender.FEMALE, "3": Gender.OTHER}
    gender = gender_map.get(gender_choice, Gender.OTHER)
    
    # Height
    while True:
        try:
            height = float(input("\n📏 Height in cm (e.g., 175): "))
            if 100 <= height <= 250:
                break
            print("   Please enter height between 100-250 cm")
        except ValueError:
            print("   Please enter a valid number")
    
    # Weight
    while True:
        try:
            weight = float(input("⚖️  Weight in kg (e.g., 70): "))
            if 30 <= weight <= 300:
                break
            print("   Please enter weight between 30-300 kg")
        except ValueError:
            print("   Please enter a valid number")
    
    # Experience level
    print("\n💪 Training Experience:")
    print("   1. Beginner (0-1 year)")
    print("   2. Intermediate (1-3 years)")
    print("   3. Advanced (3-5 years)")
    print("   4. Elite (5+ years)")
    exp_choice = input("   Choose (1-4): ").strip()
    exp_map = {
        "1": ExperienceLevel.BEGINNER,
        "2": ExperienceLevel.INTERMEDIATE,
        "3": ExperienceLevel.ADVANCED,
        "4": ExperienceLevel.ELITE
    }
    experience = exp_map.get(exp_choice, ExperienceLevel.BEGINNER)
    
    # Equipment (optional)
    print("\n🏋️ Available Equipment (comma-separated, or press Enter to skip):")
    print("   Examples: dumbbells, barbell, pull_up_bar, bench, cables")
    equipment_input = input("   Equipment: ").strip()
    equipment = [e.strip() for e in equipment_input.split(",") if e.strip()] if equipment_input else []
    
    # Injuries (optional)
    print("\n⚠️  Any past injuries or current issues? (comma-separated, or press Enter to skip)")
    print("   Examples: lower back, knee, shoulder")
    injury_input = input("   Injuries: ").strip()
    injuries = [i.strip() for i in injury_input.split(",") if i.strip()] if injury_input else []
    
    # Create profile
    profile = UserProfile(
        user_id=str(uuid.uuid4())[:8],
        name=name,
        age=age,
        gender=gender,
        height_cm=height,
        weight_kg=weight,
        experience_level=experience,
        equipment_available=equipment,
        injury_history=injuries,
    )
    
    print("\n✅ Profile created successfully!")
    print(f"   Name: {name}, Age: {age}, BMI: {profile.bmi}")
    print("-" * 60)
    
    return profile


def get_user_profile_choice() -> tuple[str, Optional[UserProfile]]:
    """
    Ask user whether to use sample profile or create new one.
    
    Returns:
        Tuple of (choice, optional_profile)
        - "sample": Use sample_user.json
        - "interactive": Profile created interactively
        - "file": User specified their own file path
    """
    print("\n" + "=" * 60)
    print("🏃 ATHLETIX AI - Fitness Coach")
    print("=" * 60)
    print("\n📋 User Profile Options:")
    print("   1. Use sample profile (sample_user.json)")
    print("   2. Create new profile (answer a few questions)")
    print("   3. Specify profile file path")
    print("   Or type a filename directly (e.g., sample_user_02.json)")
    
    choice = input("\nChoose option (1-3) or filename: ").strip()
    
    if choice == "1":
        return ("sample", None)
    elif choice == "2":
        profile = create_profile_interactive()
        return ("interactive", profile)
    elif choice == "3":
        file_path = input("Enter path to profile JSON: ").strip()
        return ("file", file_path)
    elif choice.endswith(".json"):
        # User typed a filename directly
        return ("file", choice)
    else:
        print("Invalid choice, using sample profile...")
        return ("sample", None)


# ============================================================
# NUTRITION ONLY MODE
# ============================================================

def run_nutrition_analysis(food_images: list[str], food_prefs_path: Optional[str] = None) -> dict:
    """
    Run nutrition analysis ONLY on food images.
    
    Args:
        food_images: List of food image paths
        food_prefs_path: Optional path to food preferences JSON
    
    Returns:
        Nutrition analysis result
    """
    load_dotenv()
    
    from src.agents.nutrition_agent import nutrition_agent_node
    from src.models.user_profile import FoodPreferences
    
    logger.info("Running nutrition analysis only...")
    
    food_preferences = load_food_preferences(food_prefs_path)
    
    # Create minimal state for nutrition agent
    state = {
        "food_images": food_images,
        "food_preferences": food_preferences or FoodPreferences(),
    }
    
    result = nutrition_agent_node(state)
    return result


def display_nutrition_only(result: dict) -> None:
    """Display nutrition analysis results only."""
    print("\n" + "=" * 70)
    print("🍎 NUTRITION ANALYSIS")
    print("=" * 70)
    
    nutrition = result.get("nutrition_analysis")
    if not nutrition or not nutrition.daily_meals:
        print("\n  No food items detected in the image(s).")
        print("=" * 70)
        return
    
    # Display each meal and its food items
    for meal in nutrition.daily_meals:
        meal_type = meal.meal_type.value.upper() if hasattr(meal.meal_type, 'value') else str(meal.meal_type).upper()
        print(f"\n📍 {meal_type}")
        print("-" * 70)
        
        if meal.food_items:
            # Header
            print(f"{'Food Item':<28} {'Protein':>8} {'Carbs':>8} {'Fats':>7} {'Fiber':>7} {'Cal':>7}")
            print("-" * 80)
            
            # Each food item
            for item in meal.food_items:
                name = item.name[:26] + ".." if len(item.name) > 28 else item.name
                fiber = getattr(item, 'fiber_g', 0) or 0
                print(f"{name:<28} {item.protein_g:>7.1f}g {item.carbs_g:>7.1f}g {item.fats_g:>6.1f}g {fiber:>6.1f}g {item.calories:>6.0f}")
            
            print("-" * 80)
            # Meal subtotal
            m = meal.total_macros
            fiber_total = getattr(m, 'fiber_g', 0) or sum(getattr(i, 'fiber_g', 0) or 0 for i in meal.food_items)
            print(f"{'MEAL TOTAL':<28} {m.protein_g:>7.1f}g {m.carbs_g:>7.1f}g {m.fats_g:>6.1f}g {fiber_total:>6.1f}g {m.calories:>6.0f}")
        
        # Health score
        print(f"\n  ⭐ Health Score: {meal.health_score:.1f}/10")
        
        # Suggestions
        if meal.suggestions:
            print(f"  💡 Suggestions:")
            for suggestion in meal.suggestions[:3]:
                print(f"     • {suggestion}")
    
    # Daily totals
    print("\n" + "=" * 70)
    print("📊 DAILY TOTALS")
    print("-" * 70)
    macros = nutrition.daily_totals
    print(f"  🥩 Protein:  {macros.protein_g:>8.1f}g")
    print(f"  🍞 Carbs:    {macros.carbs_g:>8.1f}g")
    print(f"  🥑 Fats:     {macros.fats_g:>8.1f}g")
    print(f"  🔥 Calories: {macros.calories:>8.0f}")
    print("=" * 70 + "\n")


# ============================================================
# PROGRAM ONLY MODE
# ============================================================

def run_program_generation(
    profile_path: str,
    goals_path: Optional[str] = None,
    wearable_path: Optional[str] = None,
) -> dict:
    """
    Run program generation ONLY (no nutrition analysis).
    
    Args:
        profile_path: Path to user profile JSON
        goals_path: Optional path to fitness goals JSON
        wearable_path: Optional path to wearable data JSON
    
    Returns:
        Program generation result with coaching
    """
    load_dotenv()
    
    from src.agents.orchestrator import orchestrator_node
    from src.agents.cv_agent import cv_agent_node
    from src.agents.wearable_agent import wearable_agent_node
    from src.agents.planner_agent import planner_agent_node
    from src.agents.coach_agent import coach_agent_node
    
    logger.info("Running program generation only...")
    
    user_profile = load_user_profile(profile_path)
    is_valid, errors = validate_user_profile(user_profile)
    if not is_valid:
        raise ValueError(f"Invalid profile: {errors}")
    
    goals = load_goals(goals_path)
    wearable_data = load_wearable_data(wearable_path)
    
    # Create initial state
    state = create_initial_state(user_profile=user_profile, goals=goals)
    state["wearable_data"] = wearable_data
    
    # Run only the program-related agents
    state.update(orchestrator_node(state))
    state.update(cv_agent_node(state))
    state.update(wearable_agent_node(state))
    state.update(planner_agent_node(state))
    state.update(coach_agent_node(state))
    
    return state


def display_program_only(state: dict) -> None:
    """Display program and coaching results only."""
    print("\n" + "=" * 70)
    print("🏋️ TRAINING PROGRAM")
    print("=" * 70)
    
    # Coaching message
    coaching_message = state.get("coaching_message")
    if coaching_message:
        print("\n📣 COACHING MESSAGE:")
        print("-" * 70)
        print(coaching_message)
    
    # Daily tips
    tips = state.get("daily_tips", [])
    if tips:
        print("\n💡 DAILY TIPS:")
        for tip in tips:
            print(f"  • {tip}")
    
    # Program details
    program = state.get("program")
    if program:
        print("\n📋 PROGRAM DETAILS:")
        print("-" * 70)
        print(f"  Program: {program.program_name}")
        print(f"  Duration: {program.program_length_weeks} weeks")
        print(f"  Split: {program.weekly_split}")
        
        # Show first week's workouts
        if program.weekly_schedules:
            week = program.weekly_schedules[0]
            print(f"\n  Week 1 Workouts:")
            for workout in week.workouts[:3]:
                print(f"    • {workout.day_name}: {workout.focus}")
                for ex in workout.exercises[:3]:
                    print(f"        - {ex.name}: {ex.sets}x{ex.reps}")
    
    print("\n" + "=" * 70 + "\n")


def run_program_with_profile(
    user_profile: UserProfile,
    goals_path: Optional[str] = None,
    wearable_path: Optional[str] = None,
) -> dict:
    """Run program generation with a UserProfile object directly."""
    load_dotenv()
    
    from src.agents.orchestrator import orchestrator_node
    from src.agents.cv_agent import cv_agent_node
    from src.agents.wearable_agent import wearable_agent_node
    from src.agents.planner_agent import planner_agent_node
    from src.agents.coach_agent import coach_agent_node
    
    logger.info(f"Running program for: {user_profile.name}")
    
    goals = load_goals(goals_path)
    wearable_data = load_wearable_data(wearable_path)
    
    state = create_initial_state(user_profile=user_profile, goals=goals)
    state["wearable_data"] = wearable_data
    
    state.update(orchestrator_node(state))
    state.update(cv_agent_node(state))
    state.update(wearable_agent_node(state))
    state.update(planner_agent_node(state))
    state.update(coach_agent_node(state))
    
    return state


def run_full_with_profile(
    user_profile: UserProfile,
    food_prefs_path: Optional[str] = None,
    goals_path: Optional[str] = None,
    wearable_path: Optional[str] = None,
    food_images: Optional[list[str]] = None,
    video_frames: Optional[list[str]] = None,
) -> dict:
    """Run full fitness coach with a UserProfile object directly."""
    load_dotenv()
    
    logger.info(f"Running full coach for: {user_profile.name}")
    
    food_preferences = load_food_preferences(food_prefs_path)
    goals = load_goals(goals_path)
    wearable_data = load_wearable_data(wearable_path)
    
    initial_state = create_initial_state(
        user_profile=user_profile,
        food_preferences=food_preferences,
        goals=goals,
    )
    
    if wearable_data:
        initial_state["wearable_data"] = wearable_data
    if food_images:
        initial_state["food_images"] = food_images
    if video_frames:
        initial_state["video_frames"] = video_frames
    
    graph = get_compiled_graph()
    return graph.invoke(initial_state)


# ============================================================
# FULL MODE (Both Nutrition + Program)
# ============================================================

def run_fitness_coach(
    profile_path: str,
    food_prefs_path: Optional[str] = None,
    goals_path: Optional[str] = None,
    wearable_path: Optional[str] = None,
    food_images: Optional[list[str]] = None,
    video_frames: Optional[list[str]] = None,
) -> dict:
    """Run the full AI Fitness Coach workflow."""
    load_dotenv()
    
    logger.info("Loading user profile...")
    user_profile = load_user_profile(profile_path)
    
    is_valid, errors = validate_user_profile(user_profile)
    if not is_valid:
        raise ValueError(f"Invalid user profile: {errors}")
    
    food_preferences = load_food_preferences(food_prefs_path)
    goals = load_goals(goals_path)
    wearable_data = load_wearable_data(wearable_path)
    
    logger.info(f"Loaded profile for: {user_profile.name}")
    
    initial_state = create_initial_state(
        user_profile=user_profile,
        food_preferences=food_preferences,
        goals=goals,
    )
    
    if wearable_data:
        initial_state["wearable_data"] = wearable_data
    if food_images:
        initial_state["food_images"] = food_images
    if video_frames:
        initial_state["video_frames"] = video_frames
    
    logger.info("Initializing fitness coach graph...")
    graph = get_compiled_graph()
    
    logger.info("Running fitness coach analysis...")
    final_state = graph.invoke(initial_state)
    
    logger.info("Analysis complete!")
    return final_state


def display_results(state: dict) -> None:
    """Display full results (nutrition + program)."""
    print("\n" + "=" * 70)
    print("🏋️ AI FITNESS COACH RESULTS")
    print("=" * 70 + "\n")
    
    # Coaching message
    coaching_message = state.get("coaching_message")
    if coaching_message:
        print("📣 TODAY'S COACHING MESSAGE:")
        print("-" * 70)
        print(coaching_message)
        print()
    
    # Daily tips
    tips = state.get("daily_tips", [])
    if tips:
        print("� DAILY TIPS:")
        for tip in tips:
            print(f"  • {tip}")
        print()
    
    # Nutrition section
    nutrition = state.get("nutrition_analysis")
    if nutrition and nutrition.daily_meals:
        display_nutrition_only({"nutrition_analysis": nutrition})
    
    # Program section
    program = state.get("program")
    if program:
        print("\n📋 TRAINING PROGRAM:")
        print("-" * 70)
        print(f"  Program: {program.program_name}")
        print(f"  Duration: {program.program_length_weeks} weeks")
        print(f"  Split: {program.weekly_split}")
        print()
    
    print("=" * 70)


# ============================================================
# CLI ENTRY POINT
# ============================================================

def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI-Driven Virtual Fitness Coach",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes:
  --nutrition-only  Analyze food images only (no program generation)
  --program-only    Generate program only (no nutrition analysis)
  (default)         Full mode - both nutrition and program

Examples:
  # Nutrition analysis only
  python -m src.main --nutrition-only --food-images meal.jpg
  
  # Program generation only
  python -m src.main --program-only --profile user.json
  
  # Full mode (both)
  python -m src.main --profile user.json --food-images meal.jpg
        """
    )
    
    # Mode selection
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--nutrition-only", "-n",
        action="store_true",
        help="Run nutrition analysis only (no program generation)"
    )
    mode_group.add_argument(
        "--program-only",
        action="store_true",
        help="Run program generation only (no nutrition analysis)"
    )
    
    # Input files
    parser.add_argument(
        "--profile", "-p",
        help="Path to user profile JSON file (required for program/full mode)"
    )
    parser.add_argument(
        "--food-prefs",
        help="Path to food preferences JSON file"
    )
    parser.add_argument(
        "--goals",
        help="Path to fitness goals JSON file"
    )
    parser.add_argument(
        "--wearable", "-w",
        help="Path to wearable data JSON file"
    )
    parser.add_argument(
        "--food-images", "-f",
        nargs="+",
        help="Food image paths or URLs for nutrition analysis"
    )
    parser.add_argument(
        "--video-frames", "-v",
        nargs="+",
        help="Exercise video frame paths or URLs for form analysis"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file for results (JSON format)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # NUTRITION ONLY MODE
        if args.nutrition_only:
            if not args.food_images:
                parser.error("--nutrition-only requires --food-images")
            
            result = run_nutrition_analysis(
                food_images=args.food_images,
                food_prefs_path=args.food_prefs,
            )
            display_nutrition_only(result)
        
        # PROGRAM ONLY MODE
        elif args.program_only:
            # Get profile interactively if not provided
            if not args.profile:
                choice, profile_data = get_user_profile_choice()
                if choice == "sample":
                    args.profile = "sample_user.json"
                elif choice == "interactive":
                    # Run with interactive profile directly
                    result = run_program_with_profile(
                        user_profile=profile_data,
                        goals_path=args.goals,
                        wearable_path=args.wearable,
                    )
                    display_program_only(result)
                    return
                elif choice == "file":
                    args.profile = profile_data
            
            result = run_program_generation(
                profile_path=args.profile,
                goals_path=args.goals,
                wearable_path=args.wearable,
            )
            display_program_only(result)
        
        # FULL MODE
        else:
            # Get profile interactively if not provided
            if not args.profile:
                choice, profile_data = get_user_profile_choice()
                if choice == "sample":
                    args.profile = "sample_user.json"
                elif choice == "interactive":
                    # Run with interactive profile directly
                    result = run_full_with_profile(
                        user_profile=profile_data,
                        food_prefs_path=args.food_prefs,
                        goals_path=args.goals,
                        wearable_path=args.wearable,
                        food_images=args.food_images,
                        video_frames=args.video_frames,
                    )
                    display_results(result)
                    return
                elif choice == "file":
                    args.profile = profile_data
            
            result = run_fitness_coach(
                profile_path=args.profile,
                food_prefs_path=args.food_prefs,
                goals_path=args.goals,
                wearable_path=args.wearable,
                food_images=args.food_images,
                video_frames=args.video_frames,
            )
            display_results(result)
        
        # Save output if requested
        if args.output:
            output_data = {}
            
            if "nutrition_analysis" in result and result["nutrition_analysis"]:
                na = result["nutrition_analysis"]
                output_data["nutrition"] = {
                    "meals": [
                        {
                            "type": m.meal_type.value if hasattr(m.meal_type, 'value') else str(m.meal_type),
                            "items": [
                                {"name": i.name, "protein_g": i.protein_g, "carbs_g": i.carbs_g, "fats_g": i.fats_g, "calories": i.calories}
                                for i in m.food_items
                            ],
                            "total": {"protein_g": m.total_macros.protein_g, "carbs_g": m.total_macros.carbs_g, "fats_g": m.total_macros.fats_g, "calories": m.total_macros.calories}
                        }
                        for m in na.daily_meals
                    ],
                    "daily_totals": {
                        "protein_g": na.daily_totals.protein_g,
                        "carbs_g": na.daily_totals.carbs_g,
                        "fats_g": na.daily_totals.fats_g,
                        "calories": na.daily_totals.calories,
                    }
                }
            
            if "coaching_message" in result:
                output_data["coaching_message"] = result.get("coaching_message")
                output_data["daily_tips"] = result.get("daily_tips", [])
            
            with open(args.output, "w") as f:
                json.dump(output_data, f, indent=2)
            print(f"\nResults saved to: {args.output}")
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
