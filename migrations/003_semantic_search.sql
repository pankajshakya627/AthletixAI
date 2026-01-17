-- Enable the pgvector extension to work with embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Create exercises table with vector support
CREATE TABLE IF NOT EXISTS exercises (
    exercise_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE NOT NULL,
    muscles JSONB DEFAULT '[]'::jsonb,
    difficulty JSONB DEFAULT '[]'::jsonb,
    equipment JSONB DEFAULT '[]'::jsonb,
    exercise_type TEXT,
    embedding VECTOR(1536), -- Dimension for text-embedding-3-small
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create an HNSW index for faster similarity search
-- Note: m and ef_construction are parameters for the HNSW algorithm
CREATE INDEX IF NOT EXISTS idx_exercises_embedding ON exercises 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- RPC Function for semantic search
CREATE OR REPLACE FUNCTION match_exercises (
  query_embedding VECTOR(1536),
  match_threshold FLOAT,
  match_count INT
)
RETURNS TABLE (
  exercise_id UUID,
  name TEXT,
  muscles JSONB,
  difficulty JSONB,
  equipment JSONB,
  exercise_type TEXT,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    exercises.exercise_id,
    exercises.name,
    exercises.muscles,
    exercises.difficulty,
    exercises.equipment,
    exercises.exercise_type,
    1 - (exercises.embedding <=> query_embedding) AS similarity
  FROM exercises
  WHERE 1 - (exercises.embedding <=> query_embedding) > match_threshold
  ORDER BY exercises.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
