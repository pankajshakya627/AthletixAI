-- Migration 004: Add UNIQUE constraint on users.name
-- Required for upsert(on_conflict="name") in UserMemory.save_user_profile.
-- Postgres rejects ON CONFLICT against columns without a unique constraint.

-- Remove duplicate rows first, keeping the oldest user_id per name.
DELETE FROM users a
USING users b
WHERE a.name = b.name
  AND a.user_id > b.user_id;

ALTER TABLE users ADD CONSTRAINT users_name_unique UNIQUE (name);
