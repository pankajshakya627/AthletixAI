"""
Seed Supabase exercises table with vector embeddings for semantic search.
"""
import os
import sys
import logging
import json
from tqdm import tqdm
from dotenv import load_dotenv

# Add src to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.exercise_library import EXERCISE_LIBRARY
from src.utils.openai_client import get_embedding
from supabase import create_client, Client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_exercises():
    load_dotenv()
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        logger.error("Supabase credentials not found in .env")
        return

    supabase: Client = create_client(supabase_url, supabase_key)
    
    logger.info(f"Seeding {len(EXERCISE_LIBRARY)} exercises...")
    
    for name, data in tqdm(EXERCISE_LIBRARY.items()):
        try:
            # Create a rich text description for the embedding
            # This helps the embedding capture the context (muscles, type, equipment)
            description = f"Exercise: {name}. Type: {data['type']}. Muscles: {', '.join(data['muscles'])}. Equipment: {', '.join(data['equipment'])}."
            
            embedding = get_embedding(description)
            
            payload = {
                "name": name,
                "muscles": data["muscles"],
                "difficulty": data["difficulty"],
                "equipment": data["equipment"],
                "exercise_type": data["type"],
                "embedding": embedding
            }
            
            # Upsert into 'exercises' table
            supabase.table("exercises").upsert(payload, on_conflict="name").execute()
            
        except Exception as e:
            logger.error(f"Error seeding {name}: {e}")
            continue

    logger.info("✓ Seeding complete!")

if __name__ == "__main__":
    seed_exercises()
