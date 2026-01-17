# AthletixAI - AI-Driven Virtual Fitness Coach

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green.svg)
![Supabase](https://img.shields.io/badge/Supabase-Database-blueviolet.svg)
![pgvector](https://img.shields.io/badge/pgvector-Semantic%20Search-orange.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange.svg)

**A multi-agent AI fitness coaching system using LangGraph for orchestration and Supabase for long-term memory.**

[Features](#-features) • [Architecture](#-architecture) • [Installation](#-installation) • [Database Setup](#-database-setup) • [Documentation](#-documentation)

</div>

---

## 🎯 Overview

AthletixAI is an intelligent fitness coaching platform that combines:

- **Computer Vision** for exercise form analysis
- **Nutrition AI** for food image macro calculation
- **Long-Term Memory** for cross-session personalized training
- **Semantic Search** for intelligent exercise discovery and substitution

## ✨ Features

| Feature                    | Description                                                                                   |
| -------------------------- | --------------------------------------------------------------------------------------------- |
| 🗄️ **Long-term Memory**    | Supabase storage for user profiles, programs, workout history, and cross-session learning.    |
| 🔍 **Semantic Search**     | Intelligence exercise discovery using **pgvector**. Find "leg exercises" or "core stability". |
| 🍎 **Nutrition Analysis**  | Photograph meals → Get protein, carbs, fats, fiber, calories.                                 |
| 🏋️ **Adaptive Programs**   | Programs adjust based on your history and experience level (Beginner/Intermediate/Advanced).  |
| 🧘 **Warmup & Stretching** | Built-in dynamic warmups and static cooldowns tailored to your daily plan.                    |
| 📊 **Recovery Tracking**   | HRV, sleep, and activity analysis for training readiness.                                     |
| 🖥️ **Interactive Web UI**  | Streamlit dashboard with **Cloud Sync Active** indicators and profile management.             |
| 📚 **Rich Resources**      | Clickable Tutorial, Video, and GIF links for every exercise.                                  |

---

## 🏗️ Architecture

### System Overview

```mermaid
flowchart TB
    subgraph UI["🖥️ User Interface"]
        ST[Streamlit App]
        CLI[Command Line]
    end

    subgraph Orchestration["🔄 LangGraph Orchestration"]
        ORC[Orchestrator]
        CV[CV Agent]
        WA[Wearable Agent]
        PA[Planner Agent]
        RA[Research Agent]
        CA[Coach Agent]
    end

    subgraph Memory["🗄️ Cloud Memory (Supabase)"]
        PROF[(User Profiles)]
        PROG[(Training Programs)]
        HIST[(Workout History)]
        VEC[(Exercise Vector DB)]
    end

    ST & CLI --> ORC
    ORC --> CV & WA --> PA
    PA --> RA
    RA --> CA
    PA -.->|Grounding| HIST
    RA -.->|Search| VEC
    CA -.->|Persistence| PROG
```

### Agent Pipeline

1.  **User Profile**: Inputs from UI or JSON.
2.  **Planner**: Generates 5-6 day workout program based on experience (Intermediate/Advanced).
3.  **Research**: Searches web (Tavily) for tutorial videos/articles for every exercise.
4.  **Coach**: Adds personalized advice and motivation.
5.  **Output**: Interactive table with clickable video links.

---

## 📸 Screenshots

<div align="center">

![AthletixAI Dashboard - Profile creation sidebar and welcome screen](docs/images/dashboard.png)

_AI Fitness Coach dashboard showing profile selection and welcome screen._

</div>

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/pankajshakya627/AthletixAI.git
cd AthletixAI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
pip install streamlit supabase tqdm

# Configure environment
cp .env.example .env
# Edit .env and add your API keys:
# - OPENAI_API_KEY (required)
# - TAVILY_API_KEY (optional, for exercise research)
# - SUPABASE_URL/KEY (optional, for caching)
```

## 🗄️ Database Setup (Supabase)

AthletixAI requires **Supabase** for its core intelligence and long-term memory.

### 1. Configure Environment

Add your credentials to `.env`:

```env
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_service_role_key
OPENAI_API_KEY=your_key
```

### 2. Apply Migrations

Run these SQL scripts in order in your **Supabase SQL Editor**:

1.  [001_initial_schema.sql](migrations/001_initial_schema.sql) - Core tables.
2.  [002_add_difficulty.sql](migrations/002_add_difficulty.sql) - Exercise metadata.
3.  [003_semantic_search.sql](migrations/003_semantic_search.sql) - **CRITICAL**: Enables `pgvector` and semantic search.

### 3. Seed Vector Database

Once migrations are complete and API keys are set, populate the exercise library:

```bash
python scripts/seed_exercises_vector.py
```

_This generates OpenAI embeddings for 100+ exercises and saves them to your cloud database._

---

## 🧩 Component Guide

AthletixAI is built as a modular system where each agent handles a specific domain. Here is how to use each component:

### 🥗 Nutrition AI

**Goal**: Analyze caloric and macronutrient content from food images.

- **How to use**: In the Streamlit UI, navigate to the "Nutrition" section and upload a photo of your meal.
- **Output**: The system returns a breakdown of Protein (g), Carbs (g), Fats (g), and Total Calories, optimized based on your profile's goal (e.g., "Muscle Gain" vs "Weight Loss").

### 🏋️ Training Planner

**Goal**: Generate high-volume, personalized workout programs.

- **How to use**: Select your profile from the sidebar and click **"🚀 Generate Program"**.
- **Intelligence**: The planner automatically detects your **experience level** (Beginner, Intermediate, Advanced) and selects appropriate exercises from the 100+ exercise library. It prioritizes compound movements (Squats, Bench) for efficiency.

### 🔍 Exercise Research

**Goal**: Provide visual and educational resources for every exercise in your plan.

- **How to use**: View your generated program in the dashboard. Click on any exercise name or the links in the **Tutorial**, **Video**, or **GIF** columns.
- **Tech**: Powered by **Tavily**, it fetches live URLs to ensure you always have the best form guidance.

### 🗄️ Long-Term Memory

**Goal**: Cross-device persistence and historical progress tracking.

- **How to use**: Look for the **"☁️ Cloud Sync Active"** message in the sidebar. Any profile you create or program you generate is automatically saved to Supabase.
- **Grounding**: When generating a new program, the AI automatically fetches your **last 5 workouts** to adjust volume or substitute exercises you struggled with.

### 🧠 Semantic Search

**Goal**: Find exercises based on natural language intent.

- **How to use**: Use the dedicated testing script to explore the library:
  ```bash
  python tests/verify_semantic_search.py "leg exercises for seniors"
  ```
- **Fuzzy Matching**: You don't need exact names. You can search for concepts like "core stability", "injury prevention", or "explosive power".

### ⌚ Wearable Integration (Beta)

**Goal**: Adjust training intensity based on recovery data.

- **How to use**: (Simulation mode) Provide a `wearable_data.json` file.
- **Output**: The agent analyzes HRV and Sleep scores to suggest whether it's a "Push Day" or a "Rest Day".

---

## 📖 Usage

### 🖥️ Interactive Web UI (Recommended)

The easiest way to use the coach is via the Streamlit app:

```bash
streamlit run src/app.py
```

**Features:**

- **Cloud Sync Active**: Real-time indicator of Supabase connectivity.
- **Historical Grounding**: Automatically adjusts your new program based on your last 5 workouts.
- **Rich Dashboard**: View weekly schedules with embedded exercise tutorials.

### 💻 Command Line Interface

```bash
# Run program generation for a specific profile
python -m src.main --program-only --profile sample_user.json
```

---

## 📁 Project Structure

```
AthletixAI/
├── docs/
│   ├── HLD.md                  # High-Level Design
│   ├── LLD.md                  # Low-Level Design
│   └── SUPABASE_SETUP.md       # Database setup guide
├── migrations/
│   └── 001_initial_schema.sql  # Supabase database schema
├── src/
│   ├── app.py                  # Streamlit Web UI
│   ├── main.py                 # CLI entry point
│   ├── graph.py                # LangGraph topology
│   ├── state.py                # FitnessState TypedDict
│   ├── agents/                 # 8 specialized agents
│   │   ├── research_agent.py   # Exercise resource search
│   │   └── ...                 # Other agents
│   ├── models/                 # Pydantic data models
│   │   ├── research.py         # Exercise resources
│   │   ├── session.py          # Session tracking
│   │   └── ...
│   ├── memory/                 # Memory system
│   │   ├── user_memory.py      # Supabase integration
│   │   └── session_cache.py    # In-memory cache
│   ├── safety/                 # Guardrails & validators
│   └── utils/                  # OpenAI client & prompts
├── tests/
│   ├── test_supabase_setup.py
│   └── test_research_integration.py
├── pyproject.toml
└── sample_user.json
```

## 📚 Documentation

| Document                                           | Description                                           |
| -------------------------------------------------- | ----------------------------------------------------- |
| [Enterprise_HLD.md](docs/Enterprise_HLD.md)        | **New** Enterprise Design Thinking Framework HLD      |
| [SUPABASE_SETUP.md](docs/SUPABASE_SETUP.md)        | Detailed database configuration guide                 |
| [Interview_Preparation.md](docs/Enterprise_HLD.md) | Structured Q&A for the Enterprise Design architecture |

## 🔒 Safety

- **Validation**: Strict input checks for age, weight, and height.
- **Volume Caps**: Maximum weekly set limits per muscle group to prevent overtraining.
- **Injury Aware**: Automatically modifies programs based on the injuries listed in your profile.

## 🛠️ Tech Stack

| Category      | Technology                       |
| ------------- | -------------------------------- |
| Orchestration | LangGraph (StateGraph)           |
| AI            | OpenAI GPT-4o, text-embedding-3  |
| Database      | Supabase (PostgreSQL + pgvector) |
| Vector Store  | HNSW Index on Supabase           |
| Frontend      | Streamlit                        |
| Search        | Tavily API                       |

## 📝 License

MIT License

---

<div align="center">
Made with 💪 by AthletixAI Team
</div>
