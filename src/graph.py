"""LangGraph topology for the AI Fitness Coach."""

from langgraph.graph import StateGraph, END

from src.state import FitnessState
from src.agents.orchestrator import orchestrator_node
from src.agents.cv_agent import cv_agent_node
from src.agents.wearable_agent import wearable_agent_node
from src.agents.nutrition_agent import nutrition_agent_node
from src.agents.research_agent import research_agent_node  # NEW
from src.agents.planner_agent import planner_agent_node
from src.agents.coach_agent import coach_agent_node
from src.agents.adaptation_agent import adaptation_agent_node, should_replan


def create_fitness_graph() -> StateGraph:
    """
    Create the LangGraph StateGraph for the fitness coach.
    
    Graph Topology:
        orchestrator → cv_agent → wearable_agent → nutrition_agent 
        → research_agent → planner_agent → coach_agent → adaptation_agent
        → (conditional: back to planner_agent if needs_replan, else END)
    
    Returns:
        Compiled StateGraph ready for invocation
    """
    # Create the graph with our state type
    graph = StateGraph(FitnessState)
    
    # Add all agent nodes
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("cv_agent", cv_agent_node)
    graph.add_node("wearable_agent", wearable_agent_node)
    graph.add_node("nutrition_agent", nutrition_agent_node)
    graph.add_node("research_agent", research_agent_node)  # NEW
    graph.add_node("planner_agent", planner_agent_node)
    graph.add_node("coach_agent", coach_agent_node)
    graph.add_node("adaptation_agent", adaptation_agent_node)
    
    # Set entry point
    graph.set_entry_point("orchestrator")
    
    # Add linear edges through the assessment pipeline
    graph.add_edge("orchestrator", "cv_agent")
    graph.add_edge("cv_agent", "wearable_agent")
    graph.add_edge("wearable_agent", "nutrition_agent")
    graph.add_edge("nutrition_agent", "planner_agent")      # planner comes first now
    graph.add_edge("planner_agent", "research_agent")       # research AFTER planner
    graph.add_edge("research_agent", "coach_agent")         # then coach
    graph.add_edge("coach_agent", "adaptation_agent")
    
    # Add conditional edge for feedback loop
    graph.add_conditional_edges(
        "adaptation_agent",
        should_replan,
        {
            True: "planner_agent",  # Loop back if needs replanning
            False: END,             # End if no replanning needed
        }
    )
    
    return graph


def compile_fitness_graph():
    """
    Create and compile the fitness graph for execution.
    
    Returns:
        Compiled graph ready for invocation
    """
    graph = create_fitness_graph()
    return graph.compile()


# Pre-compiled graph for import
fitness_graph = None


def get_compiled_graph():
    """Get the compiled graph (lazy initialization)."""
    global fitness_graph
    if fitness_graph is None:
        fitness_graph = compile_fitness_graph()
    return fitness_graph
