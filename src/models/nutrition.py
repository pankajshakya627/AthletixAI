"""Nutrition analysis models for food image processing."""

from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class MealType(str, Enum):
    """Type of meal."""
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    PRE_WORKOUT = "pre_workout"
    POST_WORKOUT = "post_workout"


class DailyMacros(BaseModel):
    """Daily macronutrient totals."""
    
    protein_g: float = Field(default=0, ge=0, description="Total protein in grams")
    carbs_g: float = Field(default=0, ge=0, description="Total carbs in grams")
    fats_g: float = Field(default=0, ge=0, description="Total fats in grams")
    calories: float = Field(default=0, ge=0, description="Total calories")
    fiber_g: float = Field(default=0, ge=0, description="Total fiber in grams")
    sugar_g: float = Field(default=0, ge=0, description="Total sugar in grams")
    
    def add(self, other: "DailyMacros") -> "DailyMacros":
        """Add another DailyMacros to this one."""
        return DailyMacros(
            protein_g=self.protein_g + other.protein_g,
            carbs_g=self.carbs_g + other.carbs_g,
            fats_g=self.fats_g + other.fats_g,
            calories=self.calories + other.calories,
            fiber_g=self.fiber_g + other.fiber_g,
            sugar_g=self.sugar_g + other.sugar_g,
        )


class FoodItem(BaseModel):
    """Individual food item identified in image."""
    
    name: str = Field(description="Name of the food item")
    portion_size: str = Field(description="Estimated portion size (e.g., '150g', '1 cup')")
    protein_g: float = Field(ge=0, description="Protein content in grams")
    carbs_g: float = Field(ge=0, description="Carbohydrate content in grams")
    fats_g: float = Field(ge=0, description="Fat content in grams")
    calories: float = Field(ge=0, description="Calorie content")
    fiber_g: float = Field(default=0, ge=0, description="Fiber content in grams")
    sugar_g: float = Field(default=0, ge=0, description="Sugar content in grams")
    confidence: float = Field(
        default=0.8,
        ge=0,
        le=1,
        description="Confidence in identification (0-1)"
    )
    
    @property
    def macros(self) -> DailyMacros:
        """Get macros as DailyMacros object."""
        return DailyMacros(
            protein_g=self.protein_g,
            carbs_g=self.carbs_g,
            fats_g=self.fats_g,
            calories=self.calories,
            fiber_g=self.fiber_g,
            sugar_g=self.sugar_g,
        )


class MealAnalysis(BaseModel):
    """Analysis of a complete meal from image."""
    
    meal_type: MealType = Field(description="Type of meal")
    food_items: list[FoodItem] = Field(
        default_factory=list,
        description="List of identified food items"
    )
    total_macros: DailyMacros = Field(
        default_factory=DailyMacros,
        description="Total macros for the meal"
    )
    health_score: float = Field(
        default=5.0,
        ge=0,
        le=10,
        description="Overall health score for the meal (0-10)"
    )
    suggestions: list[str] = Field(
        default_factory=list,
        description="Nutritional improvement suggestions"
    )
    dietary_flags: list[str] = Field(
        default_factory=list,
        description="Flags for dietary restrictions violated"
    )
    image_url: Optional[str] = Field(
        default=None,
        description="URL or path to the analyzed image"
    )
    analyzed_at: datetime = Field(
        default_factory=datetime.now,
        description="When the analysis was performed"
    )
    
    def calculate_totals(self) -> None:
        """Calculate total macros from food items."""
        total = DailyMacros()
        for item in self.food_items:
            total = total.add(item.macros)
        self.total_macros = total


class NutritionAnalysis(BaseModel):
    """Complete nutrition analysis for a user's day or period."""
    
    daily_meals: list[MealAnalysis] = Field(
        default_factory=list,
        description="List of meals analyzed"
    )
    daily_totals: DailyMacros = Field(
        default_factory=DailyMacros,
        description="Total daily macros"
    )
    protein_target_met: bool = Field(
        default=False,
        description="Whether protein target was met"
    )
    carbs_target_met: bool = Field(
        default=False,
        description="Whether carbs target was met"
    )
    fats_target_met: bool = Field(
        default=False,
        description="Whether fats target was met"
    )
    calorie_target_met: bool = Field(
        default=False,
        description="Whether calorie target was met"
    )
    recommendations: list[str] = Field(
        default_factory=list,
        description="Daily nutrition recommendations"
    )
    analysis_date: datetime = Field(
        default_factory=datetime.now,
        description="Date of analysis"
    )
    
    def calculate_daily_totals(self) -> None:
        """Calculate daily totals from all meals."""
        total = DailyMacros()
        for meal in self.daily_meals:
            total = total.add(meal.total_macros)
        self.daily_totals = total
    
    def check_targets(
        self,
        protein_target: Optional[float] = None,
        carbs_target: Optional[float] = None,
        fats_target: Optional[float] = None,
        calorie_target: Optional[float] = None,
    ) -> None:
        """Check if macro targets are met (within 90% is considered met)."""
        if protein_target:
            self.protein_target_met = self.daily_totals.protein_g >= (protein_target * 0.9)
        if carbs_target:
            self.carbs_target_met = self.daily_totals.carbs_g >= (carbs_target * 0.9)
        if fats_target:
            self.fats_target_met = self.daily_totals.fats_g >= (fats_target * 0.9)
        if calorie_target:
            # Calories within 10% of target
            self.calorie_target_met = abs(
                self.daily_totals.calories - calorie_target
            ) <= (calorie_target * 0.1)
