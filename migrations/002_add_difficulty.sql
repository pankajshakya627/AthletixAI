-- ============================================================================
-- MIGRATION 002: Add difficulty levels to exercise_resources
-- ============================================================================
-- This migration adds a difficulty_levels column to tag exercises by level
-- Values: 'beginner', 'intermediate', 'advanced'
-- An exercise can have multiple levels (e.g., squats work for all levels)
-- ============================================================================

-- Add difficulty_levels column as array of text
ALTER TABLE exercise_resources 
ADD COLUMN IF NOT EXISTS difficulty_levels TEXT[] DEFAULT ARRAY['beginner', 'intermediate', 'advanced'];

-- Add muscle_groups column for categorization
ALTER TABLE exercise_resources 
ADD COLUMN IF NOT EXISTS muscle_groups TEXT[] DEFAULT ARRAY[]::TEXT[];

-- Add equipment_required column
ALTER TABLE exercise_resources 
ADD COLUMN IF NOT EXISTS equipment_required TEXT[] DEFAULT ARRAY[]::TEXT[];

-- Add exercise_type column (compound, isolation, cardio, stretch)
ALTER TABLE exercise_resources 
ADD COLUMN IF NOT EXISTS exercise_type TEXT DEFAULT 'compound';

-- Create index for filtering by difficulty
CREATE INDEX IF NOT EXISTS idx_exercise_difficulty 
ON exercise_resources USING GIN (difficulty_levels);

-- Create index for filtering by muscle group
CREATE INDEX IF NOT EXISTS idx_exercise_muscles 
ON exercise_resources USING GIN (muscle_groups);

-- Update existing records to have default difficulty (universal exercises)
UPDATE exercise_resources 
SET difficulty_levels = ARRAY['beginner', 'intermediate', 'advanced']
WHERE difficulty_levels IS NULL;

-- ============================================================================
-- Sample updates for specific exercises (run after initial data exists)
-- ============================================================================
-- UPDATE exercise_resources SET difficulty_levels = ARRAY['beginner'] 
-- WHERE exercise_name IN ('wall push-up', 'knee push-up', 'assisted squat');

-- UPDATE exercise_resources SET difficulty_levels = ARRAY['advanced'] 
-- WHERE exercise_name IN ('muscle up', 'pistol squat', 'planche');
