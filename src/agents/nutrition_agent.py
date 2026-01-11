"""Nutrition Agent - Food image analysis and macro calculation."""

import json
import logging
import re
from typing import Any

from src.state import FitnessState
from src.models.nutrition import (
    NutritionAnalysis,
    MealAnalysis,
    FoodItem,
    DailyMacros,
    MealType,
)
from src.models.user_profile import DietaryRestriction
from src.utils.openai_client import get_vision_response
from src.utils.prompts import get_prompt

logger = logging.getLogger(__name__)


def _extract_json(text: str) -> str:
    """Extract JSON from markdown code blocks or raw text."""
    # Try to find JSON in markdown code blocks
    patterns = [
        r'```json\s*([\s\S]*?)\s*```',  # ```json ... ```
        r'```\s*([\s\S]*?)\s*```',       # ``` ... ```
        r'\{[\s\S]*\}',                   # Raw JSON object
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            json_str = match.group(1) if '```' in pattern else match.group(0)
            # Validate it's parseable
            try:
                json.loads(json_str)
                return json_str
            except json.JSONDecodeError:
                continue
    
    # Return original if no pattern matched
    return text


def nutrition_agent_node(state: FitnessState) -> dict[str, Any]:
    """
    Nutrition Agent node - Analyzes food images for macro calculation.
    
    Uses OpenAI Vision API to:
    - Identify foods from images
    - Estimate portion sizes
    - Calculate protein, carbs, fats per item
    - Provide health scores and suggestions
    - Flag dietary restriction violations
    
    Args:
        state: Current fitness state with food_images
    
    Returns:
        State updates with nutrition_analysis
    """
    logger.info("Nutrition Agent: Starting food analysis")
    
    updates: dict[str, Any] = {
        "current_agent": "nutrition_agent",
    }
    
    food_images = state.get("food_images", [])
    
    if not food_images:
        logger.info("Nutrition Agent: No food images provided, skipping analysis")
        updates["nutrition_analysis"] = NutritionAnalysis()
        return updates
    
    # Get user food preferences
    food_preferences = state.get("food_preferences")
    dietary_restrictions = []
    if food_preferences:
        dietary_restrictions = [
            r.value for r in getattr(food_preferences, "dietary_restrictions", [])
            if r != DietaryRestriction.NONE
        ]
        allergies = getattr(food_preferences, "allergies", [])
        calorie_target = getattr(food_preferences, "calorie_target", None)
        protein_target = getattr(food_preferences, "protein_target_g", None)
    else:
        allergies = []
        calorie_target = None
        protein_target = None
    
    # Analyze each food image
    all_meals = []
    
    for idx, image in enumerate(food_images):
        try:
            logger.info(f"Nutrition Agent: Analyzing image {idx + 1}/{len(food_images)}")
            
            prompt = get_prompt(
                "nutrition_agent",
                dietary_restrictions=", ".join(dietary_restrictions) if dietary_restrictions else "None",
                allergies=", ".join(allergies) if allergies else "None",
                calorie_target=calorie_target or "Not specified",
                protein_target=protein_target or "Not specified",
            )
            
            response = get_vision_response(
                prompt=prompt,
                images=[image],
                max_tokens=1200,
            )
            
            # Extract JSON from potentially markdown-wrapped response
            json_str = _extract_json(response)
            meal_data = json.loads(json_str)
            meal = _parse_meal_analysis(meal_data, image)
            all_meals.append(meal)
            
            logger.info(
                f"Nutrition Agent: Meal analyzed - "
                f"items={len(meal.food_items)}, "
                f"calories={meal.total_macros.calories}"
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Nutrition Agent: Failed to parse response for image {idx}: {e}")
        except Exception as e:
            logger.error(f"Nutrition Agent: Error analyzing image {idx}: {e}")
    
    # Create nutrition analysis with all meals
    nutrition_analysis = NutritionAnalysis(daily_meals=all_meals)
    nutrition_analysis.calculate_daily_totals()
    
    # Check macro targets if specified
    if food_preferences:
        nutrition_analysis.check_targets(
            protein_target=protein_target,
            carbs_target=getattr(food_preferences, "carbs_target_g", None),
            fats_target=getattr(food_preferences, "fats_target_g", None),
            calorie_target=calorie_target,
        )
    
    updates["nutrition_analysis"] = nutrition_analysis
    
    logger.info(
        f"Nutrition Agent: Analysis complete - "
        f"meals={len(all_meals)}, "
        f"daily_protein={nutrition_analysis.daily_totals.protein_g}g"
    )
    
    return updates


def _parse_meal_analysis(data: dict, image_url: str) -> MealAnalysis:
    """Parse API response into MealAnalysis model."""
    
    # Parse meal type
    meal_type_str = data.get("meal_type", "snack").lower()
    meal_type_map = {
        "breakfast": MealType.BREAKFAST,
        "lunch": MealType.LUNCH,
        "dinner": MealType.DINNER,
        "snack": MealType.SNACK,
        "pre_workout": MealType.PRE_WORKOUT,
        "post_workout": MealType.POST_WORKOUT,
    }
    meal_type = meal_type_map.get(meal_type_str, MealType.SNACK)
    
    # Parse food items
    food_items = []
    for item_data in data.get("food_items", []):
        food_items.append(FoodItem(
            name=item_data.get("name", "Unknown food"),
            portion_size=item_data.get("portion_size", "1 serving"),
            protein_g=item_data.get("protein_g", 0),
            carbs_g=item_data.get("carbs_g", 0),
            fats_g=item_data.get("fats_g", 0),
            calories=item_data.get("calories", 0),
            fiber_g=item_data.get("fiber_g", 0),
            sugar_g=item_data.get("sugar_g", 0),
            confidence=item_data.get("confidence", 0.8),
        ))
    
    # Parse total macros
    total_data = data.get("total_macros", {})
    total_macros = DailyMacros(
        protein_g=total_data.get("protein_g", 0),
        carbs_g=total_data.get("carbs_g", 0),
        fats_g=total_data.get("fats_g", 0),
        calories=total_data.get("calories", 0),
    )
    
    return MealAnalysis(
        meal_type=meal_type,
        food_items=food_items,
        total_macros=total_macros,
        health_score=data.get("health_score", 5.0),
        suggestions=data.get("suggestions", []),
        dietary_flags=data.get("dietary_flags", []),
        image_url=image_url if image_url.startswith("http") else None,
    )
