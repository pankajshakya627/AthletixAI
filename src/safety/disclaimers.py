"""Health disclaimers for the fitness coach."""

from typing import Any

from src.state import FitnessState


# Standard health disclaimers
HEALTH_DISCLAIMERS = {
    "general": "This is not medical advice. Consult a physician before beginning any exercise program.",
    
    "pain": "Stop immediately if you experience sharp pain. Consult a healthcare provider if pain persists.",
    
    "new_exercise": "Learn proper form from a qualified instructor before attempting new exercises.",
    
    "intensity": "Progress gradually. Sudden increases in intensity can lead to injury.",
    
    "medical_condition": "If you have any medical conditions, get clearance from your doctor before exercising.",
    
    "nutrition": "Nutrition recommendations are general guidelines. Consult a registered dietitian for personalized advice.",
    
    "supplement": "Always consult a healthcare provider before taking any supplements.",
    
    "pregnancy": "If pregnant or nursing, consult your healthcare provider before exercising.",
    
    "heart_condition": "If you have heart conditions, consult your cardiologist before high-intensity exercise.",
    
    "diabetes": "If you have diabetes, monitor blood sugar levels and consult your doctor about exercise.",
}


def get_relevant_disclaimers(state: FitnessState) -> list[str]:
    """
    Get relevant disclaimers based on user profile and program.
    
    Args:
        state: Current fitness state
    
    Returns:
        List of relevant disclaimer strings
    """
    disclaimers = []
    
    # Always include general disclaimer
    disclaimers.append(HEALTH_DISCLAIMERS["general"])
    
    user_profile = state.get("user_profile")
    if not user_profile:
        return disclaimers
    
    # Check for medical conditions
    medical_conditions = getattr(user_profile, "medical_conditions", [])
    if medical_conditions:
        disclaimers.append(HEALTH_DISCLAIMERS["medical_condition"])
        
        # Specific conditions
        conditions_lower = [c.lower() for c in medical_conditions]
        for condition in conditions_lower:
            if "heart" in condition or "cardiac" in condition:
                disclaimers.append(HEALTH_DISCLAIMERS["heart_condition"])
            if "diabetes" in condition:
                disclaimers.append(HEALTH_DISCLAIMERS["diabetes"])
    
    # Check for current injuries
    current_injuries = getattr(user_profile, "current_injuries", [])
    if current_injuries:
        disclaimers.append(HEALTH_DISCLAIMERS["pain"])
    
    # Check experience level for new exercise disclaimer
    experience = getattr(user_profile, "experience_level", "beginner")
    if hasattr(experience, "value"):
        experience = experience.value
    
    if experience in ["beginner", "novice"]:
        disclaimers.append(HEALTH_DISCLAIMERS["new_exercise"])
    
    return list(set(disclaimers))  # Remove duplicates


def get_session_disclaimers(workout: Any, wearable_metrics: Any) -> list[str]:
    """
    Get disclaimers specific to a workout session.
    
    Args:
        workout: Today's workout
        wearable_metrics: Current wearable metrics
    
    Returns:
        List of session-specific disclaimers
    """
    disclaimers = []
    
    # Check intensity
    if wearable_metrics:
        intensity_mod = getattr(wearable_metrics, "recommended_intensity_modifier", 0)
        if intensity_mod < -20:
            disclaimers.append(
                "Your recovery indicators suggest taking it easy today. "
                "Listen to your body and reduce intensity if needed."
            )
    
    # Check workout intensity
    if workout:
        intensity = getattr(workout, "intensity_level", "moderate")
        if intensity in ["high", "very high"]:
            disclaimers.append(HEALTH_DISCLAIMERS["intensity"])
    
    return disclaimers


def format_disclaimer_block(disclaimers: list[str]) -> str:
    """Format disclaimers as a readable block."""
    if not disclaimers:
        return ""
    
    lines = ["⚠️ **Important Health Information:**"]
    for disclaimer in disclaimers:
        lines.append(f"• {disclaimer}")
    
    return "\n".join(lines)
