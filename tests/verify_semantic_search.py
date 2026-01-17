"""
Verification script for Semantic Search.
Usage: python tests/verify_semantic_search.py "leg exercises for seniors"
"""
import sys
import os
import logging
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.memory.user_memory import UserMemory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_search(query: str):
    load_dotenv()
    memory = UserMemory()
    
    if not memory.is_enabled():
        print("❌ Supabase not enabled.")
        return

    print(f"\n🔍 Searching for: '{query}'...")
    results = memory.semantic_search_exercises(query, limit=5)
    
    if not results:
        print("❓ No results found. Did you run the seeding script?")
        return

    print("\n✅ Top Results:")
    print("-" * 50)
    for i, res in enumerate(results, 1):
        print(f"{i}. {res['name'].title()} (Similarity: {res['similarity']:.4f})")
        print(f"   Muscles: {', '.join(res['muscles'])}")
        print(f"   Level: {', '.join(res['difficulty'])}")
        print("-" * 50)

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "core stability exercises"
    test_search(query)
