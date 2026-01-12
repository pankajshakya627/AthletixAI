# Supabase Setup Guide for AthletixAI

This guide walks you through setting up Supabase for long-term memory storage.

## Prerequisites

- Supabase account (sign up at https://supabase.com)
- Project created in Supabase

## Step 1: Create Supabase Project

1. Go to https://supabase.com/dashboard
2. Click "New Project"
3. Choose organization and provide:
   - **Project Name**: `athletix-ai` (or your preferred name)
   - **Database Password**: Choose a strong password (save this!)
   - **Region**: Choose closest to your location
4. Click "Create new project"
5. Wait for project to initialize (~2 minutes)

## Step 2: Get API Credentials

Once your project is ready:

1. Go to **Settings** (gear icon) → **API**
2. Copy the following values:

```
Project URL: https://xxxxx.supabase.co
anon/public key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
service_role key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (optional, for admin operations)
```

## Step 3: Configure Environment

Add these to your `.env` file:

```bash
# Supabase Configuration
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  # Use anon/public key
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  # Optional
```

## Step 4: Run Database Migration

### Option A: Using Supabase SQL Editor (Recommended)

1. In your Supabase dashboard, go to **SQL Editor**
2. Click "New query"
3. Copy the entire contents of `migrations/001_initial_schema.sql`
4. Paste into the SQL editor
5. Click "Run" (or press Cmd/Ctrl + Enter)
6. Wait for confirmation message

### Option B: Using Supabase CLI (Advanced)

```bash
# Install Supabase CLI
npm install -g supabase

# Login
supabase login

# Link to your project
supabase link --project-ref YOUR_PROJECT_REF

# Run migration
supabase db push
```

## Step 5: Verify Tables

In Supabase dashboard:

1. Go to **Table Editor**
2. You should see 8 tables:
   - `users`
   - `sessions`
   - `training_programs`
   - `exercise_resources`
   - `checkpoints`
   - `workout_history`
   - `food_preferences`

## Step 6: Set Row Level Security (Optional but Recommended)

For production use, enable RLS policies:

```sql
-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE training_programs ENABLE ROW LEVEL SECURITY;
ALTER TABLE exercise_resources ENABLE ROW LEVEL SECURITY;
ALTER TABLE workout_history ENABLE ROW LEVEL SECURITY;

-- Example policy: Users can only access their own data
CREATE POLICY "Users can view own data"
  ON users FOR SELECT
  USING (auth.uid() = user_id::text);

-- Add similar policies for other tables
```

**Note**: For development/testing, you can skip RLS. For production, implement proper policies.

## Step 7: Test Connection

Run the test script:

```bash
python tests/test_supabase_setup.py
```

Expected output:

```
🧪 Starting Supabase Tests...

============================================================
SUPABASE CONNECTION TEST
============================================================

1. Checking environment variables...
✓ SUPABASE_URL: https://xxxxx.supabase.co...
✓ SUPABASE_KEY: eyJhbGciOiJIUzI1NiIsInR5...

2. Testing connection...
✓ Supabase client created successfully

3. Testing table access...
✓ Table 'users' accessible (rows: 0)
✓ Table 'sessions' accessible (rows: 0)
✓ Table 'training_programs' accessible (rows: 0)
✓ Table 'exercise_resources' accessible (rows: 0)
✓ Table 'workout_history' accessible (rows: 0)
✓ Table 'checkpoints' accessible (rows: 0)

4. Testing insert/query operations...
✓ Insert test successful
✓ Query test successful
✓ Delete test successful

============================================================
✅ ALL TESTS PASSED!
============================================================
```

## Troubleshooting

### Error: "Table does not exist"

- **Solution**: Run the migration script in Step 4

### Error: "Invalid API key"

- **Solution**: Double-check your `SUPABASE_KEY` in `.env`
- Make sure you copied the **anon/public** key, not the service role key

### Error: "Connection refused"

- **Solution**: Check your `SUPABASE_URL` is correct
- Ensure your Supabase project is active (not paused)

### Error: "Permission denied"

- **Solution**: If RLS is enabled, you need to authenticate first
- For testing, disable RLS or use service role key

## Next Steps

Once all tests pass:

1. ✅ Supabase is ready
2. ✅ Proceed with graph integration
3. ✅ Test research agent with Tavily API

## Useful Supabase Resources

- [Documentation](https://supabase.com/docs)
- [Python Client](https://supabase.com/docs/reference/python/introduction)
- [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
- [Database Functions](https://supabase.com/docs/guides/database/functions)
