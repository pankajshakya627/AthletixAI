"""
Test script to generate a full program and verify tutorial URLs are included.
"""
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def test_full_program_with_urls():
    """Generate a complete program and verify URLs are present."""
    print("\n" + "=" * 70)
    print("FULL PROGRAM GENERATION TEST - Verify Tutorial URLs")
    print("=" * 70)
    
    # Import required modules
    from src.models.user_profile import UserProfile, Gender, ExperienceLevel, FitnessGoals
    from src.agents.planner_agent import planner_agent_node, _create_default_program
    from src.agents.research_agent import research_agent_node
    from src.state import FitnessState
    
    # Create test user
    print("\n1. Creating test user profile...")
    user_profile = UserProfile(
        user_id="test_user_123",
        name="Test User",
        age=30,
        gender=Gender.MALE,
        height_cm=180,
        weight_kg=80,
        experience_level=ExperienceLevel.INTERMEDIATE,
        equipment_available=["dumbbells", "barbell", "pull_up_bar"],
        injury_history=[],
        current_injuries=[]
    )
    
    goals = FitnessGoals(
        primary_goal="muscle_building",
        weekly_workout_days=5
    )
    
    print(f"✓ User: {user_profile.name}, {user_profile.experience_level.value}")
    
    # Create state
    state = FitnessState(
        user_profile=user_profile,
        goals=goals,
        current_agent="test"
    )
    
    # Step 1: Run research agent
    print("\n2. Running Research Agent...")
    if os.getenv("TAVILY_API_KEY"):
        research_result = research_agent_node(state)
        if "exercise_resources" in research_result:
            state["exercise_resources"] = research_result["exercise_resources"]
            print(f"✓ Found resources for {len(research_result['exercise_resources'].exercises)} exercises")
        else:
            print("⚠️  Research agent returned no results")
    else:
        print("⚠️  TAVILY_API_KEY not set, skipping research")
    
    # Step 2: Generate program
    print("\n3. Generating training program...")
    planner_result = planner_agent_node(state)
    program = planner_result.get("program")
    
    if not program:
        print("❌ No program generated!")
        return False
    
    print(f"✓ Program: {program.program_name}")
    print(f"✓ Weeks: {program.program_length_weeks}")
    print(f"✓ Days per week: {len(program.weekly_schedules[0].workouts)}")
    
    # Step 3: Check for tutorial URLs
    print("\n4. Checking for tutorial URLs in exercises...")
    
    total_exercises = 0
    exercises_with_urls = 0
    
    for week in program.weekly_schedules:
        for workout in week.workouts:
            for exercise in workout.exercises:
                total_exercises += 1
                has_url = (
                    exercise.tutorial_url or 
                    exercise.video_url or 
                    exercise.gif_url
                )
                if has_url:
                    exercises_with_urls += 1
    
    print(f"\nTotal exercises: {total_exercises}")
    print(f"Exercises with URLs: {exercises_with_urls}")
    print(f"Coverage: {(exercises_with_urls/total_exercises*100):.1f}%")
    
    # Show sample
    if exercises_with_urls > 0:
        print("\n5. Sample exercises with URLs:")
        count = 0
        for week in program.weekly_schedules:
            for workout in week.workouts:
                for exercise in workout.exercises:
                    if exercise.tutorial_url or exercise.video_url:
                        print(f"\n   • {exercise.name}:")
                        if exercise.tutorial_url:
                            print(f"     Tutorial: {exercise.tutorial_url[:60]}...")
                        if exercise.video_url:
                            print(f"     Video: {exercise.video_url[:60]}...")
                        if exercise.gif_url:
                            print(f"     GIF: {exercise.gif_url[:60]}...")
                        count += 1
                        if count >= 3:
                            break
                if count >= 3:
                    break
            if count >= 3:
                break
    else:
        print("\n❌ NO TUTORIAL URLs FOUND IN PROGRAM!")
        print("\nPossible reasons:")
        print("  1. TAVILY_API_KEY not configured")
        print("  2. Research agent not running in graph")
        print("  3. Planner not enriching exercises with URLs")
        print("  4. Check that research_agent is in the graph flow")
    
    print("\n" + "=" * 70)
    return exercises_with_urls > 0


if __name__ == "__main__":
    try:
        success = test_full_program_with_urls()
        if success:
            print("✅ TEST PASSED - Tutorial URLs are present!")
        else:
            print("❌ TEST FAILED - Tutorial URLs missing!")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
