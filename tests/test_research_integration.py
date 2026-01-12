"""
Test the integrated research agent + program enrichment.

This script tests the full flow:
1. Research agent searches for exercise resources
2. Planner agent generates program
3. Program is enriched with tutorial URLs
"""
import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_research_and_enrichment():
    """Test research agent and program enrichment."""
    print("\n" + "=" * 70)
    print("RESEARCH AGENT + PROGRAM ENRICHMENT TEST")
    print("=" * 70)
    
    # Check Tavily API key
    print("\n1. Checking Tavily API configuration...")
    if not os.getenv("TAVILY_API_KEY"):
        print("⚠️  TAVILY_API_KEY not set - research agent will be skipped")
        print("   Set it in .env to enable exercise research")
        tavily_configured = False
    else:
        print(f"✓ TAVILY_API_KEY configured")
        tavily_configured = True
    
    # Load sample user profile
    print("\n2. Loading sample user profile...")
    from src.models.user_profile import UserProfile, Gender, ExperienceLevel
    
    sample_profile = UserProfile(
        user_id="test_user",
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
    print(f"✓ Loaded profile: {sample_profile.name}")
    
    # Test research agent (if Tavily is configured)
    if tavily_configured:
        print("\n3. Testing research agent...")
        from src.agents.research_agent import research_agent_node
        from src.state import FitnessState
        
        # Create minimal state
        state = FitnessState(
            user_profile=sample_profile,
            current_agent="research_agent"
        )
        
        print("   Searching for exercise resources (this may take 10-20 seconds)...")
        result = research_agent_node(state)
        
        if result and "exercise_resources" in result:
            resources = result["exercise_resources"]
            print(f"✓ Found resources for {len(resources.exercises)} exercises")
            
            # Show first few
            for i, (name, resource) in enumerate(list(resources.exercises.items())[:3]):
                print(f"   • {name}:")
                if resource.video_url:
                    print(f"     Video: {resource.video_url[:50]}...")
                if resource.tutorial_url:
                    print(f"     Tutorial: {resource.tutorial_url[:50]}...")
        else:
            print("❌ Research agent returned no results")
            return False
    else:
        print("\n3. Skipping research agent test (Tavily not configured)")
    
    # Test program generation with enrichment
    print("\n4. Testing program generation + enrichment...")
    from src.agents.planner_agent import planner_agent_node, _enrich_program_with_resources
    from src.models.program import TrainingProgram, WeeklySchedule, DailyWorkout, Exercise
    
    # Create a simple test program
    test_exercise = Exercise(
        name="squat",
        sets=4,
        reps="8-10",
        rest_seconds=90,
        technique_cues=["Keep chest up"]
    )
    
    test_workout = DailyWorkout(
        day_number=1,
        day_name="Test Day",
        focus="Lower Body",
        exercises=[test_exercise]
    )
    
    test_program = TrainingProgram(
        program_name="Test Program",
        program_length_weeks=1,
        weekly_split="Test",
        weekly_schedules=[WeeklySchedule(week_number=1, workouts=[test_workout])]
    )
    
    print(f"✓ Created test program with {len(test_workout.exercises)} exercise")
    
    # Enrich if we have resources
    if tavily_configured and 'resources' in locals():
        print("\n5. Enriching program with research URLs...")
        enriched = _enrich_program_with_resources(test_program, resources)
        
        # Check if enrichment worked
        exercise = enriched.weekly_schedules[0].workouts[0].exercises[0]
        if exercise.tutorial_url or exercise.video_url:
            print(f"✓ Exercise enriched successfully!")
            print(f"   Tutorial URL: {exercise.tutorial_url or 'N/A'}")
            print(f"   Video URL: {exercise.video_url or 'N/A'}")
            print(f"   GIF URL: {exercise.gif_url or 'N/A'}")
        else:
            print("⚠️  Exercise not enriched (no matching resource)")
    else:
        print("\n5. Skipping enrichment test")
    
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Set TAVILY_API_KEY in .env to enable research")
    print("2. Run: python -m src.main --program-only")
    print("3. Check generated program for tutorial URLs")
    return True


if __name__ == "__main__":
    try:
        success = test_research_and_enrichment()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
