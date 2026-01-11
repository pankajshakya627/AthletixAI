"""Input validation for the fitness coach."""

from typing import Any, Optional
from pydantic import ValidationError

from src.models.user_profile import UserProfile


def validate_input(data: dict, model_class: type) -> tuple[bool, Optional[str]]:
    """
    Validate input data against a Pydantic model.
    
    Args:
        data: Dictionary of input data
        model_class: Pydantic model class to validate against
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        model_class(**data)
        return True, None
    except ValidationError as e:
        errors = []
        for error in e.errors():
            field = ".".join(str(f) for f in error["loc"])
            msg = error["msg"]
            errors.append(f"{field}: {msg}")
        return False, "; ".join(errors)
    except Exception as e:
        return False, str(e)


def validate_user_profile(profile: Any) -> tuple[bool, list[str]]:
    """
    Validate a user profile has all required fields and safe values.
    
    Args:
        profile: UserProfile instance or dict
    
    Returns:
        Tuple of (is_valid, list of validation errors)
    """
    errors = []
    
    # Check required fields
    required = ["user_id", "name", "age", "height_cm", "weight_kg"]
    
    for field in required:
        value = getattr(profile, field, None) if hasattr(profile, field) else profile.get(field)
        if value is None:
            errors.append(f"Missing required field: {field}")
    
    # Validate age
    age = getattr(profile, "age", None) if hasattr(profile, "age") else profile.get("age")
    if age is not None:
        if age < 13:
            errors.append("User must be at least 13 years old")
        if age > 100:
            errors.append("Please verify age is correct")
    
    # Validate height
    height = getattr(profile, "height_cm", None) if hasattr(profile, "height_cm") else profile.get("height_cm")
    if height is not None:
        if height < 100 or height > 250:
            errors.append("Height must be between 100cm and 250cm")
    
    # Validate weight
    weight = getattr(profile, "weight_kg", None) if hasattr(profile, "weight_kg") else profile.get("weight_kg")
    if weight is not None:
        if weight < 30 or weight > 300:
            errors.append("Weight must be between 30kg and 300kg")
    
    return len(errors) == 0, errors


def validate_wearable_data(data: dict) -> tuple[bool, list[str]]:
    """Validate wearable data values are within safe ranges."""
    errors = []
    
    # Heart rate validation
    hr = data.get("resting_heart_rate")
    if hr is not None and (hr < 30 or hr > 120):
        errors.append("Resting heart rate should be between 30-120 BPM")
    
    # HRV validation
    hrv = data.get("hrv") or data.get("heart_rate_variability")
    if hrv is not None and (hrv < 0 or hrv > 200):
        errors.append("HRV should be between 0-200ms")
    
    # Sleep validation
    sleep = data.get("sleep_hours") or data.get("sleep_duration")
    if sleep is not None and (sleep < 0 or sleep > 24):
        errors.append("Sleep duration should be between 0-24 hours")
    
    return len(errors) == 0, errors
