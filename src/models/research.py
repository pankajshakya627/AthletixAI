"""
Research models for exercise resources from Tavily API.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ExerciseResource(BaseModel):
    """Resource information for a single exercise."""
    
    exercise_name: str
    tutorial_url: Optional[str] = None
    gif_url: Optional[str] = None
    video_url: Optional[str] = None
    image_urls: list[str] = Field(default_factory=list)
    breathing_guide: Optional[str] = None
    common_mistakes: list[str] = Field(default_factory=list)
    source: str = "tavily"
    confidence_score: float = 0.0
    cached_at: datetime = Field(default_factory=datetime.now)


class ResearchResults(BaseModel):
    """Collection of exercise resources from research."""
    
    exercises: dict[str, ExerciseResource]
    search_timestamp: datetime = Field(default_factory=datetime.now)
    
    def get_resource(self, exercise_name: str) -> Optional[ExerciseResource]:
        """Get resource for specific exercise (case-insensitive)."""
        # Try exact match first
        if exercise_name in self.exercises:
            return self.exercises[exercise_name]
        
        # Try case-insensitive match
        exercise_lower = exercise_name.lower()
        for key, value in self.exercises.items():
            if key.lower() == exercise_lower:
                return value
        
        return None
    
    def add_resource(self, resource: ExerciseResource) -> None:
        """Add or update exercise resource."""
        self.exercises[resource.exercise_name] = resource
