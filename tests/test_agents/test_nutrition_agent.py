"""Tests for the Nutrition Agent."""

import pytest
from unittest.mock import patch, MagicMock

from src.agents.nutrition_agent import nutrition_agent_node, _parse_meal_analysis
from src.models.nutrition import MealType, DailyMacros
from src.models.user_profile import UserProfile, FoodPreferences, Gender, DietaryRestriction


class TestNutritionAgent:
    """Tests for the Nutrition Agent."""
    
    @pytest.fixture
    def sample_state(self):
        """Create a sample state for testing."""
        return {
            "user_profile": UserProfile(
                user_id="test",
                name="Test",
                age=30,
                gender=Gender.MALE,
                height_cm=180,
                weight_kg=80,
            ),
            "food_preferences": FoodPreferences(
                calorie_target=2500,
                protein_target_g=150,
            ),
            "food_images": [],
        }
    
    def test_no_images_returns_empty_analysis(self, sample_state):
        """Test that no images returns empty nutrition analysis."""
        result = nutrition_agent_node(sample_state)
        
        assert "nutrition_analysis" in result
        assert result["current_agent"] == "nutrition_agent"
        assert len(result["nutrition_analysis"].daily_meals) == 0
    
    def test_parse_meal_analysis(self):
        """Test parsing of meal analysis response."""
        mock_response = {
            "meal_type": "lunch",
            "food_items": [
                {
                    "name": "Grilled Chicken",
                    "portion_size": "150g",
                    "protein_g": 31,
                    "carbs_g": 0,
                    "fats_g": 3.6,
                    "calories": 165,
                    "confidence": 0.9,
                }
            ],
            "total_macros": {
                "protein_g": 31,
                "carbs_g": 0,
                "fats_g": 3.6,
                "calories": 165,
            },
            "health_score": 8.5,
            "suggestions": ["Add vegetables for fiber"],
            "dietary_flags": [],
        }
        
        meal = _parse_meal_analysis(mock_response, "http://example.com/meal.jpg")
        
        assert meal.meal_type == MealType.LUNCH
        assert len(meal.food_items) == 1
        assert meal.food_items[0].name == "Grilled Chicken"
        assert meal.food_items[0].protein_g == 31
        assert meal.total_macros.protein_g == 31
        assert meal.health_score == 8.5
    
    @patch("src.agents.nutrition_agent.get_vision_response")
    def test_with_food_image(self, mock_vision, sample_state):
        """Test nutrition analysis with a food image."""
        mock_vision.return_value = '''
        {
            "meal_type": "dinner",
            "food_items": [
                {"name": "Salmon", "portion_size": "200g", "protein_g": 40, "carbs_g": 0, "fats_g": 20, "calories": 350}
            ],
            "total_macros": {"protein_g": 40, "carbs_g": 0, "fats_g": 20, "calories": 350},
            "health_score": 9.0,
            "suggestions": [],
            "dietary_flags": []
        }
        '''
        
        sample_state["food_images"] = ["http://example.com/salmon.jpg"]
        
        result = nutrition_agent_node(sample_state)
        
        assert len(result["nutrition_analysis"].daily_meals) == 1
        assert result["nutrition_analysis"].daily_meals[0].total_macros.protein_g == 40


class TestMacroCalculations:
    """Tests for macro calculations."""
    
    def test_daily_macros_add(self):
        """Test adding two DailyMacros together."""
        macros1 = DailyMacros(protein_g=30, carbs_g=50, fats_g=10, calories=400)
        macros2 = DailyMacros(protein_g=20, carbs_g=30, fats_g=15, calories=300)
        
        result = macros1.add(macros2)
        
        assert result.protein_g == 50
        assert result.carbs_g == 80
        assert result.fats_g == 25
        assert result.calories == 700
