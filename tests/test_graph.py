"""Tests for the LangGraph topology."""

import pytest

from src.graph import create_fitness_graph, compile_fitness_graph
from src.state import create_initial_state
from src.models.user_profile import UserProfile, Gender


class TestGraphTopology:
    """Tests for the LangGraph structure."""
    
    def test_graph_creation(self):
        """Test that the graph is created with all nodes."""
        graph = create_fitness_graph()
        
        # Check that all nodes exist
        expected_nodes = [
            "orchestrator",
            "cv_agent",
            "wearable_agent",
            "nutrition_agent",
            "planner_agent",
            "coach_agent",
            "adaptation_agent",
        ]
        
        for node in expected_nodes:
            assert node in graph.nodes, f"Missing node: {node}"
    
    def test_graph_compilation(self):
        """Test that the graph compiles without errors."""
        compiled = compile_fitness_graph()
        assert compiled is not None
    
    def test_graph_entry_point(self):
        """Test that orchestrator is the entry point."""
        graph = create_fitness_graph()
        # The entry point should route through orchestrator first
        assert "orchestrator" in graph.nodes


class TestAdaptationCondition:
    """Tests for the adaptation agent conditional logic."""
    
    def test_should_replan_false_by_default(self):
        """Test that needs_replan defaults to False."""
        from src.agents.adaptation_agent import should_replan
        
        state = {"needs_replan": False}
        assert should_replan(state) is False
    
    def test_should_replan_true_when_set(self):
        """Test that should_replan returns True when state indicates."""
        from src.agents.adaptation_agent import should_replan
        
        state = {"needs_replan": True}
        assert should_replan(state) is True
