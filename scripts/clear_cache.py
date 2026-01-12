"""
Utility to clear exercise resource cache from Supabase.
"""
import os
from dotenv import load_dotenv
from src.memory.user_memory import UserMemory

load_dotenv()

def clear_exercise_cache(exercise_names: list[str] = None):
    """Clear exercise resource cache."""
    user_memory = UserMemory()
    
    if not user_memory.is_enabled():
        print("❌ Supabase not configured")
        return
    
    if exercise_names:
        # Clear specific exercises
        for name in exercise_names:
            user_memory.supabase.table("exercise_resources")\
                .delete()\
                .eq("exercise_name", name)\
                .execute()
            print(f"✓ Cleared cache for: {name}")
    else:
        # Clear all
        user_memory.supabase.table("exercise_resources").delete().neq("exercise_name", "").execute()
        print("✓ Cleared all exercise resource cache")

if __name__ == "__main__":
    # Clear cache for test exercises
    test_exercises = ["squat", "deadlift", "bench press", "overhead press", "barbell row"]
    print("Clearing cache for test exercises...")
    clear_exercise_cache(test_exercises)
    print("\n✅ Cache cleared. Run the test again to get fresh searches.")
