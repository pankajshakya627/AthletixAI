"""
In-memory session cache for short-term workout data.
"""
from typing import Any, Optional
from datetime import datetime
import uuid


class SessionCache:
    """In-memory cache for current workout session."""
    
    def __init__(self, user_id: Optional[str] = None):
        """Initialize session cache."""
        self.cache: dict[str, Any] = {}
        self.session_id: str = str(uuid.uuid4())
        self.user_id: Optional[str] = user_id
        self.created_at: datetime = datetime.now()
    
    def set(self, key: str, value: Any) -> None:
        """Store value in session cache."""
        self.cache[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve value from session cache."""
        return self.cache.get(key, default)
    
    def update(self, data: dict[str, Any]) -> None:
        """Update multiple values at once."""
        self.cache.update(data)
    
    def clear(self) -> None:
        """Clear all session data."""
        self.cache.clear()
    
    def to_dict(self) -> dict:
        """Export session data as dict."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "data": self.cache,
        }
