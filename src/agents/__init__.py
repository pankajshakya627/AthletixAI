"""Agent implementations for the fitness coach."""

from src.agents.orchestrator import orchestrator_node
from src.agents.cv_agent import cv_agent_node
from src.agents.wearable_agent import wearable_agent_node
from src.agents.nutrition_agent import nutrition_agent_node
from src.agents.planner_agent import planner_agent_node
from src.agents.coach_agent import coach_agent_node
from src.agents.adaptation_agent import adaptation_agent_node

__all__ = [
    "orchestrator_node",
    "cv_agent_node",
    "wearable_agent_node",
    "nutrition_agent_node",
    "planner_agent_node",
    "coach_agent_node",
    "adaptation_agent_node",
]
