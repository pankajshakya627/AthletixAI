"""
Test script to verify Supabase setup and connection.

Run this script to ensure Supabase is properly configured before using the memory system.
"""
import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def test_supabase_connection():
    """Test basic Supabase connection."""
    print("=" * 60)
    print("SUPABASE CONNECTION TEST")
    print("=" * 60)
    
    # Check environment variables
    print("\n1. Checking environment variables...")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url:
        print("❌ SUPABASE_URL not found in environment")
        return False
    
    if not supabase_key:
        print("❌ SUPABASE_KEY not found in environment")
        return False
    
    print(f"✓ SUPABASE_URL: {supabase_url[:30]}...")
    print(f"✓ SUPABASE_KEY: {supabase_key[:20]}...")
    
    # Test connection
    print("\n2. Testing connection...")
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✓ Supabase client created successfully")
    except Exception as e:
        print(f"❌ Failed to create Supabase client: {e}")
        return False
    
    # Test table access
    print("\n3. Testing table access...")
    tables_to_test = [
        "users",
        "sessions",
        "training_programs",
        "exercise_resources",
        "workout_history",
        "checkpoints"
    ]
    
    for table in tables_to_test:
        try:
            result = supabase.table(table).select("*").limit(1).execute()
            print(f"✓ Table '{table}' accessible (rows: {len(result.data)})")
        except Exception as e:
            print(f"❌ Table '{table}' not accessible: {e}")
            print(f"   → Have you run the migration script?")
            return False
    
    print("\n4. Testing insert/query operations...")
    # Test inserting a sample exercise resource
    try:
        test_resource = {
            "exercise_name": "test_exercise_delete_me",
            "tutorial_url": "https://example.com/test",
            "source": "test",
            "confidence_score": 1.0,
        }
        
        # Insert
        insert_result = supabase.table("exercise_resources").insert(test_resource).execute()
        print(f"✓ Insert test successful")
        
        # Query
        query_result = supabase.table("exercise_resources")\
            .select("*")\
            .eq("exercise_name", "test_exercise_delete_me")\
            .execute()
        
        if query_result.data:
            print(f"✓ Query test successful")
            
            # Cleanup
            supabase.table("exercise_resources")\
                .delete()\
                .eq("exercise_name", "test_exercise_delete_me")\
                .execute()
            print(f"✓ Delete test successful")
        else:
            print(f"❌ Query returned no data")
            return False
            
    except Exception as e:
        print(f"❌ Insert/Query test failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nYour Supabase setup is ready to use.")
    return True


def test_user_memory():
    """Test UserMemory class."""
    print("\n" + "=" * 60)
    print("USER MEMORY CLASS TEST")
    print("=" * 60)
    
    try:
        from src.memory.user_memory import UserMemory
        
        print("\n1. Creating UserMemory instance...")
        user_memory = UserMemory()
        
        if not user_memory.is_enabled():
            print("❌ UserMemory not enabled (check Supabase credentials)")
            return False
        
        print("✓ UserMemory instance created")
        
        # Test caching exercise resource
        print("\n2. Testing exercise resource caching...")
        from src.models.research import ExerciseResource
        from datetime import datetime
        
        test_resource = ExerciseResource(
            exercise_name="test_squat",
            tutorial_url="https://youtube.com/test",
            source="test",
            confidence_score=0.9,
            cached_at=datetime.now()
        )
        
        user_memory.cache_exercise_resource(test_resource)
        print("✓ Resource cached")
        
        # Retrieve cached resource
        cached = user_memory.get_cached_exercise_resource("test_squat")
        if cached:
            print(f"✓ Resource retrieved: {cached.exercise_name}")
            
            # Cleanup
            if user_memory.supabase:
                user_memory.supabase.table("exercise_resources")\
                    .delete()\
                    .eq("exercise_name", "test_squat")\
                    .execute()
                print("✓ Cleanup completed")
        else:
            print("❌ Failed to retrieve cached resource")
            return False
        
        print("\n✅ UserMemory tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ UserMemory test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🧪 Starting Supabase Tests...\n")
    
    # Run connection tests
    connection_ok = test_supabase_connection()
    
    if connection_ok:
        # Run UserMemory tests
        memory_ok = test_user_memory()
        
        if memory_ok:
            print("\n🎉 All tests passed! Supabase is ready.\n")
            sys.exit(0)
    
    print("\n⚠️  Some tests failed. Please check the errors above.\n")
    sys.exit(1)
