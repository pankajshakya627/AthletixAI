"""Long-term persistence for user data and progress."""

import os
import json
import sqlite3
from typing import Any, Optional
from datetime import datetime
from pathlib import Path


class PersistenceManager:
    """
    Manages long-term storage of user data.
    
    Stores:
    - User profiles
    - Training history
    - Strength progression
    - Injury records
    - Adherence patterns
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the persistence manager.
        
        Args:
            db_path: Path to SQLite database. Defaults to ./fitness_coach.db
        """
        self.db_path = db_path or os.getenv("DATABASE_URL", "fitness_coach.db")
        if self.db_path.startswith("sqlite:///"):
            self.db_path = self.db_path.replace("sqlite:///", "")
        
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize database tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # User profiles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id TEXT PRIMARY KEY,
                    profile_data TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            # Training history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS training_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    workout_date TEXT NOT NULL,
                    workout_data TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
                )
            """)
            
            # Progress tracking table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS progress_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    exercise_name TEXT NOT NULL,
                    metric_type TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    recorded_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
                )
            """)
            
            # Programs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS programs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    program_data TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
                )
            """)
            
            conn.commit()
    
    # User Profile Methods
    def save_user_profile(self, user_id: str, profile_data: dict) -> None:
        """Save or update a user profile."""
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_profiles (user_id, profile_data, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    profile_data = excluded.profile_data,
                    updated_at = excluded.updated_at
            """, (user_id, json.dumps(profile_data), now, now))
            conn.commit()
    
    def get_user_profile(self, user_id: str) -> Optional[dict]:
        """Get a user profile by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT profile_data FROM user_profiles WHERE user_id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            return json.loads(row[0]) if row else None
    
    # Training History Methods
    def log_workout(self, user_id: str, workout_data: dict) -> None:
        """Log a completed workout."""
        now = datetime.now().isoformat()
        workout_date = workout_data.get("date", now.split("T")[0])
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO training_history (user_id, workout_date, workout_data, created_at)
                VALUES (?, ?, ?, ?)
            """, (user_id, workout_date, json.dumps(workout_data), now))
            conn.commit()
    
    def get_recent_workouts(self, user_id: str, limit: int = 10) -> list[dict]:
        """Get recent workouts for a user."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT workout_data FROM training_history
                WHERE user_id = ?
                ORDER BY workout_date DESC
                LIMIT ?
            """, (user_id, limit))
            return [json.loads(row[0]) for row in cursor.fetchall()]
    
    # Progress Tracking Methods
    def log_progress(
        self,
        user_id: str,
        exercise: str,
        metric_type: str,
        value: float,
    ) -> None:
        """Log progress for an exercise."""
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO progress_tracking 
                (user_id, exercise_name, metric_type, metric_value, recorded_at)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, exercise, metric_type, value, now))
            conn.commit()
    
    def get_exercise_progress(
        self,
        user_id: str,
        exercise: str,
        metric_type: str = "weight",
        limit: int = 20,
    ) -> list[dict]:
        """Get progress history for an exercise."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT metric_value, recorded_at FROM progress_tracking
                WHERE user_id = ? AND exercise_name = ? AND metric_type = ?
                ORDER BY recorded_at DESC
                LIMIT ?
            """, (user_id, exercise, metric_type, limit))
            return [
                {"value": row[0], "date": row[1]}
                for row in cursor.fetchall()
            ]
    
    # Program Methods
    def save_program(self, user_id: str, program_data: dict) -> int:
        """Save a training program and return its ID."""
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Deactivate previous programs
            cursor.execute(
                "UPDATE programs SET is_active = 0 WHERE user_id = ?",
                (user_id,)
            )
            
            # Insert new program
            cursor.execute("""
                INSERT INTO programs (user_id, program_data, is_active, created_at)
                VALUES (?, ?, 1, ?)
            """, (user_id, json.dumps(program_data), now))
            
            conn.commit()
            return cursor.lastrowid
    
    def get_active_program(self, user_id: str) -> Optional[dict]:
        """Get the user's active program."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT program_data FROM programs
                WHERE user_id = ? AND is_active = 1
                ORDER BY created_at DESC
                LIMIT 1
            """, (user_id,))
            row = cursor.fetchone()
            return json.loads(row[0]) if row else None
