"""
User memory manager for Supabase long-term storage.
"""
import os
import logging
from typing import Optional
from supabase import create_client, Client
from src.models.user_profile import UserProfile
from src.models.program import TrainingProgram
from src.models.research import ExerciseResource
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class UserMemory:
    """Manage long-term user data in Supabase."""
    
    def __init__(self):
        """Initialize Supabase client."""
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            logger.warning("Supabase credentials not found. Long-term memory disabled.")
            self.supabase: Optional[Client] = None
        else:
            self.supabase = create_client(supabase_url, supabase_key)
            logger.info("✓ Supabase client initialized")
    
    def is_enabled(self) -> bool:
        """Check if Supabase is configured."""
        return self.supabase is not None
    
    # ========================================================================
    # USER PROFILE METHODS
    # ========================================================================
    
    def save_user_profile(self, profile: UserProfile) -> Optional[str]:
        """Save or update user profile in Supabase."""
        if not self.is_enabled():
            return None
        
        try:
            user_data = {
                "name": profile.name,
                "email": getattr(profile, "email", None),
                "age": profile.age,
                "gender": profile.gender.value if hasattr(profile.gender, "value") else profile.gender,
                "height_cm": profile.height_cm,
                "weight_kg": profile.weight_kg,
                "experience_level": profile.experience_level.value if hasattr(profile.experience_level, "value") else profile.experience_level,
                "injury_history": profile.injury_history,
                "current_injuries": profile.current_injuries,
                "equipment_available": profile.equipment_available,
            }
            
            # Upsert (insert or update)
            result = self.supabase.table("users").upsert(
                user_data,
                on_conflict="name" # Changed to name or ensure user_id exists
            ).execute()
            
            logger.info(f"✓ Saved user profile to Supabase")
            return user_data.get("name")

        
        except Exception as e:
            logger.error(f"Error saving user profile: {e}")
            return None
    
    def load_user_profile(self, name: str) -> Optional[UserProfile]:
        """Load user profile from Supabase by name."""
        if not self.is_enabled():
            return None
        
        try:
            result = self.supabase.table("users").select("*").eq("name", name).execute()
            
            if not result.data:
                logger.warning(f"User profile not found: {name}")
                return None
            
            user_data = result.data[0]
            
            # Standardize gender and experience_level
            if "gender" in user_data:
                user_data["gender"] = user_data["gender"].lower()
            if "experience_level" in user_data:
                user_data["experience_level"] = user_data["experience_level"].lower()
            
            # Map SQL columns to UserProfile fields if they differ
            # (Assuming SQL columns match UserProfile field names based on save_user_profile)
            
            profile = UserProfile(**user_data)
            logger.info(f"✓ Loaded user profile: {name}")
            return profile
        
        except Exception as e:
            logger.error(f"Error loading user profile: {e}")
            return None

    def list_all_profiles(self) -> list[dict]:
        """List all user profiles from Supabase."""
        if not self.is_enabled():
            return []
            
        try:
            result = self.supabase.table("users").select("name, experience_level, primary_goal").execute()
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Error listing profiles: {e}")
            return []
    
    # ========================================================================
    # TRAINING PROGRAM METHODS
    # ========================================================================
    
    def save_training_program(
        self,
        user_id: str,
        program: TrainingProgram
    ) -> Optional[str]:
        """Save training program to Supabase."""
        if not self.is_enabled():
            return None
        
        try:
            program_data = {
                "user_id": user_id,
                "program_name": program.program_name,
                "program_data": program.model_dump(),  # Store as JSON
                "start_date": datetime.now().isoformat(),
                "is_active": True,
            }
            
            result = self.supabase.table("training_programs").insert(program_data).execute()
            
            program_id = result.data[0]["program_id"] if result.data else None
            logger.info(f"✓ Saved training program: {program_id}")
            return program_id
        
        except Exception as e:
            logger.error(f"Error saving training program: {e}")
            return None
    
    def get_active_program(self, user_id: str) -> Optional[TrainingProgram]:
        """Get user's active training program."""
        if not self.is_enabled():
            return None
        
        try:
            result = self.supabase.table("training_programs")\
                .select("program_data")\
                .eq("user_id", user_id)\
                .eq("is_active", True)\
                .order("created_at", desc=True)\
                .limit(1)\
                .execute()
            
            if not result.data:
                return None
            
            program_dict = result.data[0]["program_data"]
            return TrainingProgram(**program_dict)
        
        except Exception as e:
            logger.error(f"Error fetching active program: {e}")
            return None
    
    # ========================================================================
    # EXERCISE RESOURCES CACHE
    # ========================================================================
    
    def get_cached_exercise_resource(
        self,
        exercise_name: str
    ) -> Optional[ExerciseResource]:
        """Get cached exercise resource if not expired."""
        if not self.is_enabled():
            return None
        
        try:
            result = self.supabase.table("exercise_resources")\
                .select("*")\
                .eq("exercise_name", exercise_name)\
                .gt("expires_at", datetime.now().isoformat())\
                .execute()
            
            if not result.data:
                return None
            
            resource_data = result.data[0]
            return ExerciseResource(
                exercise_name=resource_data["exercise_name"],
                tutorial_url=resource_data.get("tutorial_url"),
                gif_url=resource_data.get("gif_url"),
                video_url=resource_data.get("video_url"),
                image_urls=resource_data.get("image_urls", []),
                breathing_guide=resource_data.get("breathing_guide"),
                common_mistakes=resource_data.get("common_mistakes", []),
                source=resource_data.get("source", "tavily"),
                confidence_score=resource_data.get("confidence_score", 0.0),
                cached_at=datetime.fromisoformat(resource_data["cached_at"]),
            )
        
        except Exception as e:
            logger.error(f"Error fetching cached resource: {e}")
            return None
    
    def cache_exercise_resource(self, resource: ExerciseResource) -> None:
        """Cache exercise resource in Supabase."""
        if not self.is_enabled():
            return
        
        try:
            resource_data = {
                "exercise_name": resource.exercise_name,
                "tutorial_url": resource.tutorial_url,
                "gif_url": resource.gif_url,
                "video_url": resource.video_url,
                "image_urls": resource.image_urls,
                "breathing_guide": resource.breathing_guide,
                "common_mistakes": resource.common_mistakes,
                "source": resource.source,
                "confidence_score": resource.confidence_score,
                "cached_at": resource.cached_at.isoformat(),
                "expires_at": (resource.cached_at + timedelta(days=30)).isoformat(),
            }
            
            # Upsert to update if exists
            self.supabase.table("exercise_resources").upsert(
                resource_data,
                on_conflict="exercise_name"
            ).execute()
            
            logger.info(f"✓ Cached exercise resource: {resource.exercise_name}")
        
        except Exception as e:
            logger.error(f"Error caching resource: {e}")
    
    # ========================================================================
    # WORKOUT HISTORY
    # ========================================================================
    
    def get_workout_history(
        self,
        user_id: str,
        limit: int = 10
    ) -> list[dict]:
        """Get user's recent workout history."""
        if not self.is_enabled():
            return []
        
        try:
            result = self.supabase.table("workout_history")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("workout_date", desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data if result.data else []
        
        except Exception as e:
            logger.error(f"Error fetching workout history: {e}")
            return []

    # ========================================================================
    # SEMANTIC SEARCH METHODS
    # ========================================================================

    def semantic_search_exercises(
        self,
        query: str,
        threshold: float = 0.5,
        limit: int = 5
    ) -> list[dict]:
        """
        Perform semantic search for exercises using pgvector.
        
        Args:
            query: The search query (e.g., "leg exercises for beginners")
            threshold: Minimum similarity threshold
            limit: Maximum number of results
            
        Returns:
            List of matching exercises with similarity scores
        """
        if not self.is_enabled():
            logger.warning("Supabase memory disabled. Semantic search unavailable.")
            return []
            
        try:
            from src.utils.openai_client import get_embedding
            
            # 1. Generate embedding for query
            query_embedding = get_embedding(query)
            
            # 2. Call the 'match_exercises' RPC in Supabase
            result = self.supabase.rpc(
                "match_exercises",
                {
                    "query_embedding": query_embedding,
                    "match_threshold": threshold,
                    "match_count": limit
                }
            ).execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"Error performing semantic search: {e}")
            return []

