"""Assessment Orchestrator - Entry point and router for the fitness coach."""

import logging
from typing import Any
from src.state import FitnessState

logger = logging.getLogger(__name__)


def orchestrator_node(state: FitnessState) -> dict[str, Any]:
    """
    Orchestrator node - Entry point for the fitness coach graph.
    
    Responsibilities:
    - Validate user inputs
    - Initialize missing state fields
    - Route to appropriate assessment agents
    - Maintain workflow state
    
    This is a deterministic controller with minimal LLM usage.
    
    Args:
        state: Current fitness state
    
    Returns:
        State updates with validated and initialized fields
    """
    logger.info("Orchestrator: Processing incoming state")
    
    updates: dict[str, Any] = {
        "current_agent": "orchestrator",
    }
    
    # Validate user profile exists
    user_profile = state.get("user_profile")
    if not user_profile:
        logger.error("No user profile provided")
        raise ValueError("User profile is required to start the fitness coach")
    
    # Initialize food preferences if not present
    if not state.get("food_preferences"):
        from src.models.user_profile import FoodPreferences
        updates["food_preferences"] = FoodPreferences()
        logger.info("Initialized default food preferences")
    
    # Initialize goals if not present
    if not state.get("goals"):
        from src.models.user_profile import FitnessGoals
        updates["goals"] = FitnessGoals()
        logger.info("Initialized default fitness goals")
    
    # Set needs_replan to False initially
    if state.get("needs_replan") is None:
        updates["needs_replan"] = False
    
    # Log assessment inputs available
    has_video = bool(state.get("video_frames"))
    has_food_images = bool(state.get("food_images"))
    has_wearable = bool(state.get("wearable_data"))
    
    logger.info(
        f"Orchestrator: Inputs available - "
        f"video_frames={has_video}, food_images={has_food_images}, wearable_data={has_wearable}"
    )
    
    return updates


def validate_user_profile(profile: Any) -> bool:
    """Validate that the user profile has required fields."""
    required_fields = ["user_id", "name", "age", "height_cm", "weight_kg"]
    
    if not hasattr(profile, "__dict__"):
        return False
    
    for field in required_fields:
        if not hasattr(profile, field) or getattr(profile, field) is None:
            return False
    
    return True
