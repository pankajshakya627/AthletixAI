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
                on_conflict="user_id"
            ).execute()
            
            user_id = result.data[0]["user_id"] if result.data else None
            logger.info(f"✓ Saved user profile: {user_id}")
            return user_id

        
        except Exception as e:
            logger.error(f"Error saving user profile: {e}")
            return None
    
    def load_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Load user profile from Supabase."""
        if not self.is_enabled():
            return None
        
        try:
            result = self.supabase.table("users").select("*").eq("user_id", user_id).execute()
            
            if not result.data:
                logger.warning(f"User profile not found: {user_id}")
                return None
            
            user_data = result.data[0]
            # Convert to UserProfile (simplified - adjust based on your UserProfile model)
            logger.info(f"✓ Loaded user profile: {user_id}")
            return None  # TODO: Convert dict to UserProfile model
        
        except Exception as e:
            logger.error(f"Error loading user profile: {e}")
            return None
    
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
