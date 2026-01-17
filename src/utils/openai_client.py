"""OpenAI API client utilities."""

import os
import base64
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_openai_client() -> OpenAI:
    """Get configured OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)


def encode_image_to_base64(image_path: str) -> str:
    """Encode a local image file to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_vision_response(
    prompt: str,
    images: list[str],
    model: Optional[str] = None,
    max_tokens: int = 1500,
) -> str:
    """
    Get a response from OpenAI Vision model.
    
    Args:
        prompt: Text prompt for the model
        images: List of image URLs or base64 encoded images
        model: Model to use (defaults to OPENAI_VISION_MODEL env var)
        max_tokens: Maximum tokens in response
    
    Returns:
        Model response text
    """
    client = get_openai_client()
    model = model or os.getenv("OPENAI_VISION_MODEL", "gpt-4o")
    
    # Build content with images
    content = [{"type": "text", "text": prompt}]
    
    for image in images:
        if image.startswith("http"):
            # URL image
            content.append({
                "type": "image_url",
                "image_url": {"url": image}
            })
        elif image.startswith("data:image"):
            # Already formatted base64
            content.append({
                "type": "image_url",
                "image_url": {"url": image}
            })
        elif os.path.exists(image):
            # Local file path
            base64_image = encode_image_to_base64(image)
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            })
        else:
            # Assume raw base64
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image}"}
            })
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": content}],
        max_tokens=max_tokens,
    )
    
    return response.choices[0].message.content or ""


def get_chat_response(
    system_prompt: str,
    user_message: str,
    model: Optional[str] = None,
    max_tokens: int = 2000,
    temperature: float = 0.7,
    response_format: Optional[dict] = None,
) -> str:
    """
    Get a response from OpenAI chat model.
    
    Args:
        system_prompt: System prompt for the model
        user_message: User message/query
        model: Model to use (defaults to OPENAI_CHAT_MODEL env var)
        max_tokens: Maximum tokens in response
        temperature: Sampling temperature
        response_format: Optional response format (e.g., {"type": "json_object"})
    
    Returns:
        Model response text
    """
    client = get_openai_client()
    model = model or os.getenv("OPENAI_CHAT_MODEL", "gpt-4o")
    
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    
    if response_format:
        kwargs["response_format"] = response_format
    
    response = client.chat.completions.create(**kwargs)
    
    return response.choices[0].message.content or ""


def get_structured_response(
    system_prompt: str,
    user_message: str,
    model: Optional[str] = None,
    max_tokens: int = 2000,
) -> str:
    """
    Get a JSON-structured response from OpenAI.
    
    Args:
        system_prompt: System prompt (should request JSON output)
        user_message: User message/query
        model: Model to use
        max_tokens: Maximum tokens
    
    Returns:
        JSON string response
    """
    return get_chat_response(
        system_prompt=system_prompt,
        user_message=user_message,
        model=model,
        max_tokens=max_tokens,
        temperature=0.3,  # Lower temperature for structured output
        response_format={"type": "json_object"},
    )


def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """
    Generate embedding for a given text using OpenAI.
    
    Args:
        text: The text to embed
        model: Embedding model to use
        
    Returns:
        List of floats representing the embedding
    """
    client = get_openai_client()
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

