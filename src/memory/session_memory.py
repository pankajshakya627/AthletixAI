"""Short-term session memory for the fitness coach."""

from typing import Any, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class SessionMemory:
    """
    Short-term memory for a single coaching session.
    
    Stores:
    - Recent workout data
    - Session-specific feedback
    - Current fatigue indicators
    - Conversation context
    """
    
    session_id: str
    started_at: datetime = field(default_factory=datetime.now)
    
    # Workout tracking
    recent_workouts: list[dict] = field(default_factory=list)
    current_workout_progress: dict = field(default_factory=dict)
    
    # Session feedback
    form_feedback: list[str] = field(default_factory=list)
    exercise_notes: dict[str, list[str]] = field(default_factory=dict)
    
    # Fatigue tracking
    session_rpe: Optional[int] = None
    energy_at_start: Optional[int] = None
    energy_at_end: Optional[int] = None
    
    # Conversation context
    conversation_history: list[dict] = field(default_factory=list)
    
    def add_workout_log(self, workout: dict) -> None:
        """Add a completed workout to the session history."""
        self.recent_workouts.append({
            **workout,
            "timestamp": datetime.now().isoformat(),
        })
    
    def add_form_feedback(self, feedback: str) -> None:
        """Add form feedback received during session."""
        self.form_feedback.append(feedback)
    
    def add_exercise_note(self, exercise: str, note: str) -> None:
        """Add a note for a specific exercise."""
        if exercise not in self.exercise_notes:
            self.exercise_notes[exercise] = []
        self.exercise_notes[exercise].append(note)
    
    def log_exercise_set(
        self,
        exercise: str,
        set_number: int,
        reps: int,
        weight: Optional[float] = None,
    ) -> None:
        """Log a completed exercise set."""
        if exercise not in self.current_workout_progress:
            self.current_workout_progress[exercise] = []
        
        self.current_workout_progress[exercise].append({
            "set": set_number,
            "reps": reps,
            "weight": weight,
            "timestamp": datetime.now().isoformat(),
        })
    
    def add_conversation_turn(self, role: str, content: str) -> None:
        """Add a conversation turn to history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })
    
    def get_session_summary(self) -> dict:
        """Get a summary of the session."""
        return {
            "session_id": self.session_id,
            "duration_minutes": (datetime.now() - self.started_at).total_seconds() / 60,
            "workouts_completed": len(self.recent_workouts),
            "exercises_logged": len(self.current_workout_progress),
            "feedback_received": len(self.form_feedback),
            "session_rpe": self.session_rpe,
        }
    
    def to_dict(self) -> dict:
        """Serialize session memory to dictionary."""
        return {
            "session_id": self.session_id,
            "started_at": self.started_at.isoformat(),
            "recent_workouts": self.recent_workouts,
            "current_workout_progress": self.current_workout_progress,
            "form_feedback": self.form_feedback,
            "exercise_notes": self.exercise_notes,
            "session_rpe": self.session_rpe,
            "energy_at_start": self.energy_at_start,
            "energy_at_end": self.energy_at_end,
            "conversation_history": self.conversation_history,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SessionMemory":
        """Deserialize session memory from dictionary."""
        return cls(
            session_id=data["session_id"],
            started_at=datetime.fromisoformat(data["started_at"]),
            recent_workouts=data.get("recent_workouts", []),
            current_workout_progress=data.get("current_workout_progress", {}),
            form_feedback=data.get("form_feedback", []),
            exercise_notes=data.get("exercise_notes", {}),
            session_rpe=data.get("session_rpe"),
            energy_at_start=data.get("energy_at_start"),
            energy_at_end=data.get("energy_at_end"),
            conversation_history=data.get("conversation_history", []),
        )
