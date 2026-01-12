-- Supabase Database Schema for AthletixAI
-- Version: 1.0.0
-- Description: Long-term memory storage for user profiles, training programs, sessions, and exercise resources

-- ============================================================================
-- USERS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    age INTEGER CHECK (age >= 13 AND age <= 100),
    gender TEXT CHECK (gender IN ('male', 'female', 'other')),
    height_cm FLOAT CHECK (height_cm >= 100 AND height_cm <= 250),
    weight_kg FLOAT CHECK (weight_kg >= 30 AND weight_kg <= 300),
    experience_level TEXT CHECK (experience_level IN ('beginner', 'intermediate', 'advanced', 'elite')),
    injury_history JSONB DEFAULT '[]'::jsonb,
    current_injuries JSONB DEFAULT '[]'::jsonb,
    equipment_available JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- SESSIONS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    session_date TIMESTAMPTZ DEFAULT NOW(),
    session_data JSONB,
    completed BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- TRAINING PROGRAMS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS training_programs (
    program_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    program_name TEXT NOT NULL,
    program_data JSONB NOT NULL,
    start_date TIMESTAMPTZ,
    end_date TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- EXERCISE RESOURCES CACHE (from Tavily)
-- ============================================================================
CREATE TABLE IF NOT EXISTS exercise_resources (
    resource_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exercise_name TEXT UNIQUE NOT NULL,
    tutorial_url TEXT,
    gif_url TEXT,
    video_url TEXT,
    image_urls JSONB DEFAULT '[]'::jsonb,
    breathing_guide TEXT,
    common_mistakes JSONB DEFAULT '[]'::jsonb,
    source TEXT DEFAULT 'tavily',
    confidence_score FLOAT DEFAULT 0.0,
    cached_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '30 days')
);

-- ============================================================================
-- LANGGRAPH CHECKPOINTS
-- ============================================================================
CREATE TABLE IF NOT EXISTS checkpoints (
    thread_id TEXT NOT NULL,
    checkpoint_id TEXT NOT NULL,
    parent_id TEXT,
    checkpoint JSONB NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (thread_id, checkpoint_id)
);

-- ============================================================================
-- WORKOUT HISTORY
-- ============================================================================
CREATE TABLE IF NOT EXISTS workout_history (
    workout_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    session_id UUID REFERENCES sessions(session_id),
    workout_date TIMESTAMPTZ DEFAULT NOW(),
    exercises_completed JSONB,
    notes TEXT,
    fatigue_level INTEGER CHECK (fatigue_level >= 1 AND fatigue_level <= 10),
    performance_rating INTEGER CHECK (performance_rating >= 1 AND performance_rating <= 10),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- FOOD PREFERENCES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS food_preferences (
    preference_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE UNIQUE,
    dietary_restrictions JSONB DEFAULT '[]'::jsonb,
    allergies JSONB DEFAULT '[]'::jsonb,
    calorie_target INTEGER,
    protein_target_g FLOAT,
    carbs_target_g FLOAT,
    fats_target_g FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_date ON sessions(session_date DESC);
CREATE INDEX IF NOT EXISTS idx_programs_user_id ON training_programs(user_id);
CREATE INDEX IF NOT EXISTS idx_programs_active ON training_programs(user_id, is_active) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_exercise_resources_name ON exercise_resources(exercise_name);
CREATE INDEX IF NOT EXISTS idx_exercise_resources_expires ON exercise_resources(expires_at);  -- Removed WHERE clause
CREATE INDEX IF NOT EXISTS idx_checkpoints_thread ON checkpoints(thread_id);
CREATE INDEX IF NOT EXISTS idx_checkpoints_created ON checkpoints(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_workout_history_user ON workout_history(user_id);
CREATE INDEX IF NOT EXISTS idx_workout_history_date ON workout_history(workout_date DESC);

-- ============================================================================
-- TRIGGERS FOR UPDATED_AT
-- ============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_programs_updated_at
    BEFORE UPDATE ON training_programs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_food_preferences_updated_at
    BEFORE UPDATE ON food_preferences
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- SAMPLE DATA (optional - for testing)
-- ============================================================================
-- Uncomment to insert sample user
-- INSERT INTO users (name, email, age, gender, height_cm, weight_kg, experience_level, equipment_available)
-- VALUES ('Sample User', 'sample@example.com', 30, 'male', 180, 80, 'intermediate', '["dumbbells", "barbell", "pull_up_bar"]'::jsonb);

-- ============================================================================
-- CLEANUP FUNCTION FOR EXPIRED RESOURCES
-- ============================================================================
CREATE OR REPLACE FUNCTION cleanup_expired_resources()
RETURNS void AS $$
BEGIN
    DELETE FROM exercise_resources WHERE expires_at < NOW();
END;
$$ LANGUAGE plpgsql;

-- Schedule cleanup (requires pg_cron extension - optional)
-- SELECT cron.schedule('cleanup-resources', '0 2 * * *', 'SELECT cleanup_expired_resources()');
