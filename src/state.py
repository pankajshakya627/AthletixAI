"""Central state definition for the LangGraph fitness coach."""

from typing import Annotated, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

from src.models.user_profile import UserProfile, FoodPreferences, FitnessGoals
from src.models.assessment import MovementAssessment
from src.models.wearables import WearableMetrics
from src.models.nutrition import NutritionAnalysis
from src.models.program import TrainingProgram
from src.models.feedback import WeeklyFeedback
from src.models.research import ResearchResults


class FitnessState(TypedDict, total=False):
    """
    Central state object for the AI Fitness Coach LangGraph.
    
    This state is passed between all agents and accumulates
    information as the graph progresses.
    """
    
    # User Information
    user_profile: UserProfile
    food_preferences: FoodPreferences
    goals: FitnessGoals
    
    # Assessment Results
    movement_assessment: Optional[MovementAssessment]
    wearable_metrics: Optional[WearableMetrics]
    nutrition_analysis: Optional[NutritionAnalysis]
    
    # NEW: Exercise research results from Tavily
    exercise_resources: Optional[ResearchResults]
    
    # Generated Program
    program: Optional[TrainingProgram]
    
    # Feedback & Adaptation
    weekly_feedback: Optional[WeeklyFeedback]
    needs_replan: bool
    replan_count: int  # Number of replan cycles already executed (loop guard)
    
    # Messages for conversational context
    messages: Annotated[list[BaseMessage], add_messages]
    
    # Current workflow state
    current_agent: str
    
    # Input data (for agent processing)
    video_frames: Optional[list[str]]  # Base64 encoded frames or URLs
    food_images: Optional[list[str]]   # Base64 encoded food images or URLs
    wearable_data: Optional[dict]      # Raw wearable data
    
    # Coaching output
    coaching_message: Optional[str]
    daily_tips: Optional[list[str]]
    
    # NEW: Session and memory management
    session_id: Optional[str]        # Current session ID
    user_history: Optional[list[dict]]  # Previous workout history for personalization
    thread_id: Optional[str]         # LangGraph thread ID for checkpoint persistence


def create_initial_state(
    user_profile: UserProfile,
    food_preferences: Optional[FoodPreferences] = None,
    goals: Optional[FitnessGoals] = None,
) -> FitnessState:
    """
    Create initial state for a new fitness coach session.
    
    Args:
        user_profile: The user's profile information
        food_preferences: Optional food preferences
        goals: Optional fitness goals
    
    Returns:
        Initialized FitnessState
    """
    return FitnessState(
        user_profile=user_profile,
        food_preferences=food_preferences or FoodPreferences(),
        goals=goals or FitnessGoals(),
        movement_assessment=None,
        wearable_metrics=None,
        nutrition_analysis=None,
        program=None,
        weekly_feedback=None,
        needs_replan=False,
        replan_count=0,
        messages=[],
        current_agent="orchestrator",
        video_frames=None,
        food_images=None,
        wearable_data=None,
        coaching_message=None,
        daily_tips=None,
    )
