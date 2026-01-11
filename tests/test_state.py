"""Tests for FitnessState and state management."""

import pytest
from src.state import FitnessState, create_initial_state
from src.models.user_profile import UserProfile, FoodPreferences, FitnessGoals, Gender, ExperienceLevel


class TestFitnessState:
    """Tests for FitnessState creation and management."""
    
    def test_create_initial_state(self):
        """Test creating initial state with user profile."""
        profile = UserProfile(
            user_id="test123",
            name="Test User",
            age=30,
            gender=Gender.MALE,
            height_cm=180,
            weight_kg=80,
        )
        
        state = create_initial_state(user_profile=profile)
        
        assert state["user_profile"] == profile
        assert state["current_agent"] == "orchestrator"
        assert state["needs_replan"] is False
        assert state["messages"] == []
    
    def test_create_initial_state_with_preferences(self):
        """Test creating state with food preferences."""
        profile = UserProfile(
            user_id="test123",
            name="Test User",
            age=25,
            gender=Gender.FEMALE,
            height_cm=165,
            weight_kg=60,
        )
        
        food_prefs = FoodPreferences(
            calorie_target=2000,
            protein_target_g=120,
        )
        
        goals = FitnessGoals(
            primary_goal="muscle_gain",
            weekly_workout_days=4,
        )
        
        state = create_initial_state(
            user_profile=profile,
            food_preferences=food_prefs,
            goals=goals,
        )
        
        assert state["food_preferences"].calorie_target == 2000
        assert state["goals"].primary_goal == "muscle_gain"
    
    def test_state_optional_fields(self):
        """Test that optional fields default to None."""
        profile = UserProfile(
            user_id="test123",
            name="Test User",
            age=30,
            gender=Gender.MALE,
            height_cm=180,
            weight_kg=80,
        )
        
        state = create_initial_state(user_profile=profile)
        
        assert state.get("movement_assessment") is None
        assert state.get("wearable_metrics") is None
        assert state.get("nutrition_analysis") is None
        assert state.get("program") is None


class TestUserProfile:
    """Tests for UserProfile model."""
    
    def test_bmi_calculation(self):
        """Test BMI property calculation."""
        profile = UserProfile(
            user_id="test",
            name="Test",
            age=30,
            gender=Gender.MALE,
            height_cm=180,
            weight_kg=80,
        )
        
        # BMI = 80 / (1.8^2) = 24.7
        assert profile.bmi == 24.7
    
    def test_profile_validation(self):
        """Test profile field validation."""
        with pytest.raises(ValueError):
            UserProfile(
                user_id="test",
                name="Test",
                age=5,  # Too young
                gender=Gender.MALE,
                height_cm=180,
                weight_kg=80,
            )
    
    def test_profile_with_injuries(self):
        """Test profile with injury history."""
        profile = UserProfile(
            user_id="test",
            name="Test",
            age=35,
            gender=Gender.FEMALE,
            height_cm=165,
            weight_kg=60,
            injury_history=["lower back", "right knee"],
            current_injuries=["left shoulder"],
        )
        
        assert len(profile.injury_history) == 2
        assert "lower back" in profile.injury_history
        assert len(profile.current_injuries) == 1
