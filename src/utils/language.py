"""
Language instruction templates for multilingual support.
"""

LANGUAGE_INSTRUCTIONS = {
    "english": "",  # Default, no special instruction needed
    
    "hindi": """
IMPORTANT: Respond in Hindi (हिंदी) using Devanagari script.
- Use proper Hindi fitness terminology
- Keep technical terms in Hindi where appropriate
- Use natural, conversational Hindi
""",
    
    "hinglish": """
IMPORTANT: Respond in Hinglish (Hindi-English mix).
- Mix Hindi and English naturally as Indians speak
- Use English for technical fitness terms
- Use Hindi for common words and instructions
- Example: "Aap ko daily 3 sets of squats karne hain with proper form"
"""
}


def get_language_instruction(preferred_language: str) -> str:
    """Get language instruction for prompts based on user preference."""
    return LANGUAGE_INSTRUCTIONS.get(preferred_language.lower(), "")
