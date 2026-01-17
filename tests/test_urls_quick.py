"""
Quick test to demonstrate exercise URL enrichment is working.
Runs through the actual graph to verify URLs are attached.
"""
import os
from dotenv import load_dotenv

load_dotenv()

def quick_test():
    print("\n" + "="*70)
    print("QUICK URL ENRICHMENT TEST")
    print("="*70)
    
    from src.graph import get_compiled_graph
    from src.models.user_profile import UserProfile, Gender, ExperienceLevel, FitnessGoals
    
    # Create simple user
    user = UserProfile(
        user_id="test_123",
        name="Quick Test",
        age=30,
        gender=Gender.MALE,
        height_cm=175,
        weight_kg=75,
        experience_level=ExperienceLevel.INTERMEDIATE,
        equipment_available=["dumbbells", "barbell"],
        injury_history=[],
        current_injuries=[]
    )
    
    goals = FitnessGoals(
        primary_goal="muscle_building",
        weekly_workout_days=5
    )
    
    # Create initial state
    initial_state = {
        "user_profile": user,
        "goals": goals,
        "current_agent": "orchestrator"
    }
    
    print("\n1. Running full graph (this will take ~30 seconds)...")
    print("   - Orchestrator → CV → Wearable → Nutrition → Research → Planner → Coach → Adaptation")
    
    # Run graph
    graph = get_compiled_graph()
    final_state = graph.invoke(initial_state)
    
    print("\n2. Checking program for URLs...")
    program = final_state.get("program")
    
    if not program:
        print("❌ No program in final state!")
        return False
    
    # Count enriched exercises
    total = 0
    enriched = 0
    sample_urls = []
    
    for week in program.weekly_schedules:
        for workout in week.workouts:
            for exercise in workout.exercises:
                total += 1
                if exercise.tutorial_url or exercise.video_url or exercise.gif_url:
                    enriched += 1
                    if len(sample_urls) < 3:
                        sample_urls.append({
                            "name": exercise.name,
                            "tutorial": exercise.tutorial_url,
                            "video": exercise.video_url
                        })
    
    print(f"\nTotal exercises: {total}")
    print(f"Enriched with URLs: {enriched}")
    print(f"Coverage: {(enriched/total*100):.1f}%")
    
    if sample_urls:
        print("\n3. Sample enriched exercises:")
        for ex in sample_urls:
            print(f"\n   • {ex['name']}")
            if ex['tutorial']:
                print(f"     Tutorial: {ex['tutorial'][:60]}...")
            if ex['video']:
                print(f"     Video: {ex['video'][:60]}...")
        print("\n✅ SUCCESS! URLs are being attached!")
    else:
        print("\n❌ No URLs found!")
        print("\nCheck:")
        print("  - Is TAVILY_API_KEY set in .env?")
        print("  - Run: echo $TAVILY_API_KEY")
    
    print("\n" + "="*70)
    return enriched > 0


if __name__ == "__main__":
    import sys
    try:
        success = quick_test()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
