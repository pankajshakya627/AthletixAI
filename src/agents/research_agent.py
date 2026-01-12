"""
Research agent that searches for exercise tutorials and resources using Tavily API.
"""
import os
import logging
from typing import Any, Optional
from tavily import TavilyClient
from src.state import FitnessState
from src.models.research import ExerciseResource, ResearchResults
from src.memory.user_memory import UserMemory
from datetime import datetime

logger = logging.getLogger(__name__)


# Fallback URLs for common exercises (in case Tavily is unavailable)
FALLBACK_URLS = {
    "squat": "https://www.youtube.com/watch?v=ultWZbUMPL8",
    "deadlift": "https://www.youtube.com/watch?v=XxWcirHIwVo",
    "bench press": "https://www.youtube.com/watch?v=gRVjAtPip0Y",
    "overhead press": "https://www.youtube.com/watch?v=2yjwXTZQDDI",
    "barbell row": "https://www.youtube.com/watch?v=FWJR5Ve8bnQ",
    "pull-up": "https://www.youtube.com/watch?v=eGo4IYlbE5g",
    "push-up": "https://www.youtube.com/watch?v=IODxDxX7oi4",
    "plank": "https://www.youtube.com/watch?v=ASdvN_XEl_c",
}


def research_agent_node(state: FitnessState) -> dict[str, Any]:
    """
    Research agent that finds exercise tutorials and resources.
    
    Flow:
    1. Extract exercise names from state (or use common exercises)
    2. Check cache in Supabase for existing resources
    3. For uncached exercises, search Tavily API
    4. Store results in Supabase and return in state
    """
    logger.info("🔍 Research Agent: Searching for exercise resources...")
    
    # Skip if no Tavily API key
    if not os.getenv("TAVILY_API_KEY"):
        logger.warning("TAVILY_API_KEY not configured. Skipping research agent.")
        return {}
    
    # Extract exercise names
    exercises = _extract_exercise_names(state)
    
    if not exercises:
        logger.info("No exercises identified yet. Using common exercises for demo.")
        exercises = list(FALLBACK_URLS.keys())[:5]  # First 5 common exercises
    
    logger.info(f"Researching {len(exercises)} exercises...")
    
    # Initialize clients
    try:
        tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    except Exception as e:
        logger.error(f"Failed to initialize Tavily client: {e}")
        return {}
    
    user_memory = UserMemory()
    research_results = {}
    
    for exercise_name in exercises[:10]:  # Limit to 10 exercises to avoid excessive API calls
        # Check cache first
        if user_memory.is_enabled():
            cached = user_memory.get_cached_exercise_resource(exercise_name)
            if cached:
                logger.info(f"✓ Using cached resources for: {exercise_name}")
                research_results[exercise_name] = cached
                continue
        
        # Search Tavily
        logger.info(f"🔎 Searching Tavily for: {exercise_name}")
        resource = search_exercise_resources(exercise_name, tavily_client)
        
        # Cache in Supabase
        if user_memory.is_enabled() and resource:
            user_memory.cache_exercise_resource(resource)
        
        if resource:
            research_results[exercise_name] = resource
    
    logger.info(f"✓ Research complete. Found resources for {len(research_results)} exercises.")
    
    return {
        "exercise_resources": ResearchResults(
            exercises=research_results,
            search_timestamp=datetime.now()
        )
    }


def search_exercise_resources(
    exercise_name: str,
    tavily_client: TavilyClient
) -> Optional[ExerciseResource]:
    """
    Search Tavily for exercise resources with multiple targeted queries.
    
    Makes separate searches for:
    1. Tutorial articles with diagrams
    2. Video demonstrations
    3. GIF demonstrations
    """
    try:
        tutorial_url = None
        video_url = None
        gif_url = None
        image_urls = []
        
        # Search 1: Tutorial articles with diagrams
        logger.info(f"   Searching for tutorial article: {exercise_name}")
        tutorial_query = f"{exercise_name} exercise tutorial guide form diagram"
        tutorial_results = tavily_client.search(
            query=tutorial_query,
            search_depth="basic",
            max_results=5,
            include_domains=["exrx.net", "bodybuilding.com", "verywellfit.com", "acefitness.org", "stronglifts.com"]
        )
        
        # Extract tutorial URL (prefer non-video sites)
        if tutorial_results.get("results"):
            for result in tutorial_results["results"]:
                url = result.get("url", "")
                # Avoid video sites for tutorial
                if not any(vid in url for vid in ["youtube.com", "vimeo.com", "tiktok.com"]):
                    tutorial_url = url
                    break
        
        # Search 2: Video demonstrations
        logger.info(f"   Searching for video: {exercise_name}")
        video_query = f"{exercise_name} exercise proper form demonstration video"
        video_results = tavily_client.search(
            query=video_query,
            search_depth="basic",
            max_results=5,
            include_domains=["youtube.com", "vimeo.com"]
        )
        
        # Extract video URL
        if video_results.get("results"):
            for result in video_results["results"]:
                url = result.get("url", "")
                if "youtube.com" in url or "vimeo.com" in url:
                    video_url = url
                    break
        
        # Search 3: GIF demonstrations
        logger.info(f"   Searching for GIF: {exercise_name}")
        gif_query = f"{exercise_name} exercise animated gif demonstration"
        gif_results = tavily_client.search(
            query=gif_query,
            search_depth="basic",
            max_results=5,
            include_images=True
        )
        
        # Extract GIF and images
        if gif_results.get("images"):
            for img_url in gif_results["images"][:5]:
                if img_url.lower().endswith('.gif'):
                    if not gif_url:  # Only set first GIF
                        gif_url = img_url
                elif len(image_urls) < 3:  # Collect up to 3 images
                    image_urls.append(img_url)
        
        # Also check for images in tutorial results
        if tutorial_results.get("images") and len(image_urls) < 3:
            for img_url in tutorial_results["images"][:3]:
                if not img_url.lower().endswith('.gif') and img_url not in image_urls:
                    image_urls.append(img_url)
                if len(image_urls) >= 3:
                    break
        
        # Log what we found
        logger.info(f"   ✓ Tutorial: {'Yes' if tutorial_url else 'No'}")
        logger.info(f"   ✓ Video: {'Yes' if video_url else 'No'}")
        logger.info(f"   ✓ GIF: {'Yes' if gif_url else 'No'}")
        logger.info(f"   ✓ Images: {len(image_urls)}")
        
        # If we found nothing, use fallback
        if not tutorial_url and not video_url and not gif_url:
            logger.warning(f"   No results found, using fallback")
            return _get_fallback_resource(exercise_name)
        
        return ExerciseResource(
            exercise_name=exercise_name,
            tutorial_url=tutorial_url,
            video_url=video_url,
            gif_url=gif_url,
            image_urls=image_urls,
            source="tavily",
            confidence_score=0.8 if (tutorial_url and video_url) else 0.6,
            cached_at=datetime.now()
        )
    
    except Exception as e:
        logger.error(f"Error searching for {exercise_name}: {e}")
        # Return fallback if available
        return _get_fallback_resource(exercise_name)


def _get_fallback_resource(exercise_name: str) -> Optional[ExerciseResource]:
    """Get fallback resource for common exercises."""
    fallback_url = FALLBACK_URLS.get(exercise_name.lower())
    
    if not fallback_url:
        return None
    
    return ExerciseResource(
        exercise_name=exercise_name,
        tutorial_url=fallback_url,
        video_url=fallback_url,
        source="fallback",
        confidence_score=0.9,
        cached_at=datetime.now()
    )


def _extract_exercise_names(state: FitnessState) -> list[str]:
    """Extract unique exercise names from state."""
    exercises = set()
    
    # If program exists in state, extract from there
    program = state.get("program")
    if program and hasattr(program, "weekly_schedules"):
        for week in program.weekly_schedules:
            for workout in week.workouts:
                for exercise in workout.exercises:
                    exercises.add(exercise.name)
    
    return list(exercises)
