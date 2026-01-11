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


def run_fitness_coach(
    profile_path: str,
    food_prefs_path: Optional[str] = None,
    goals_path: Optional[str] = None,
    wearable_path: Optional[str] = None,
    food_images: Optional[list[str]] = None,
    video_frames: Optional[list[str]] = None,
) -> dict:
    """
    Run the AI Fitness Coach workflow.
    
    Args:
        profile_path: Path to user profile JSON
        food_prefs_path: Optional path to food preferences JSON
        goals_path: Optional path to fitness goals JSON
        wearable_path: Optional path to wearable data JSON
        food_images: Optional list of food image paths/URLs
        video_frames: Optional list of exercise video frame paths/URLs
    
    Returns:
        Final state with coaching output
    """
    # Load environment
    load_dotenv()
    
    # Load user data
    logger.info("Loading user profile...")
    user_profile = load_user_profile(profile_path)
    
    # Validate profile
    is_valid, errors = validate_user_profile(user_profile)
    if not is_valid:
        raise ValueError(f"Invalid user profile: {errors}")
    
    food_preferences = load_food_preferences(food_prefs_path)
    goals = load_goals(goals_path)
    wearable_data = load_wearable_data(wearable_path)
    
    logger.info(f"Loaded profile for: {user_profile.name}")
    
    # Create initial state
    initial_state = create_initial_state(
        user_profile=user_profile,
        food_preferences=food_preferences,
        goals=goals,
    )
    
    # Add optional inputs
    if wearable_data:
        initial_state["wearable_data"] = wearable_data
    if food_images:
        initial_state["food_images"] = food_images
    if video_frames:
        initial_state["video_frames"] = video_frames
    
    # Get compiled graph
    logger.info("Initializing fitness coach graph...")
    graph = get_compiled_graph()
    
    # Run the graph
    logger.info("Running fitness coach analysis...")
    final_state = graph.invoke(initial_state)
    
    logger.info("Analysis complete!")
    
    return final_state


def display_results(state: dict) -> None:
    """Display the coaching results to the user."""
    print("\n" + "=" * 60)
    print("🏋️ AI FITNESS COACH RESULTS")
    print("=" * 60 + "\n")
    
    # Coaching message
    coaching_message = state.get("coaching_message")
    if coaching_message:
        print("📣 TODAY'S COACHING MESSAGE:")
        print("-" * 40)
        print(coaching_message)
        print()
    
    # Daily tips
    tips = state.get("daily_tips", [])
    if tips:
        print("💡 DAILY TIPS:")
        for tip in tips:
            print(f"  • {tip}")
        print()
    
    # Nutrition analysis - DISPLAYED SEPARATELY with food items
    nutrition = state.get("nutrition_analysis")
    if nutrition and nutrition.daily_meals:
        print("🍎 NUTRITION ANALYSIS:")
        print("=" * 60)
        
        # Display each meal and its food items
        for meal in nutrition.daily_meals:
            meal_type = meal.meal_type.value.upper() if hasattr(meal.meal_type, 'value') else str(meal.meal_type).upper()
            print(f"\n📍 {meal_type}")
            print("-" * 40)
            
            if meal.food_items:
                # Header
                print(f"{'Food Item':<30} {'Protein':>8} {'Carbs':>8} {'Fats':>8} {'Cal':>8}")
                print("-" * 70)
                
                # Each food item
                for item in meal.food_items:
                    name = item.name[:28] + ".." if len(item.name) > 30 else item.name
                    print(f"{name:<30} {item.protein_g:>7.1f}g {item.carbs_g:>7.1f}g {item.fats_g:>7.1f}g {item.calories:>7.0f}")
                
                print("-" * 70)
                # Meal subtotal
                m = meal.total_macros
                print(f"{'MEAL TOTAL':<30} {m.protein_g:>7.1f}g {m.carbs_g:>7.1f}g {m.fats_g:>7.1f}g {m.calories:>7.0f}")
            
            # Suggestions
            if meal.suggestions:
                print(f"\n  💡 Suggestions: {', '.join(meal.suggestions[:2])}")
            
            # Health score
            print(f"  ⭐ Health Score: {meal.health_score:.1f}/10")
        
        # Daily totals
        print("\n" + "=" * 60)
        print("📊 DAILY TOTALS:")
        macros = nutrition.daily_totals
        print(f"  🥩 Protein: {macros.protein_g:.1f}g")
        print(f"  🍞 Carbs:   {macros.carbs_g:.1f}g")
        print(f"  🥑 Fats:    {macros.fats_g:.1f}g")
        print(f"  🔥 Calories: {macros.calories:.0f}")
        print("=" * 60)
        print()
    
    # Program summary
    program = state.get("program")
    if program:
        print("📋 TRAINING PROGRAM:")
        print("-" * 40)
        print(f"  Program: {program.program_name}")
        print(f"  Duration: {program.program_length_weeks} weeks")
        print(f"  Split: {program.weekly_split}")
        print()
    
    print("=" * 60)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI-Driven Virtual Fitness Coach",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main --profile user.json
  python -m src.main --profile user.json --wearable wearable_data.json
  python -m src.main --profile user.json --food-images meal1.jpg meal2.jpg
        """
    )
    
    parser.add_argument(
        "--profile", "-p",
        required=True,
        help="Path to user profile JSON file"
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
        result = run_fitness_coach(
            profile_path=args.profile,
            food_prefs_path=args.food_prefs,
            goals_path=args.goals,
            wearable_path=args.wearable,
            food_images=args.food_images,
            video_frames=args.video_frames,
        )
        
        display_results(result)
        
        if args.output:
            # Serialize relevant parts of result
            output_data = {
                "coaching_message": result.get("coaching_message"),
                "daily_tips": result.get("daily_tips"),
            }
            
            if result.get("nutrition_analysis"):
                output_data["nutrition"] = {
                    "protein_g": result["nutrition_analysis"].daily_totals.protein_g,
                    "carbs_g": result["nutrition_analysis"].daily_totals.carbs_g,
                    "fats_g": result["nutrition_analysis"].daily_totals.fats_g,
                    "calories": result["nutrition_analysis"].daily_totals.calories,
                }
            
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
