# AthletixAI - AI-Driven Virtual Fitness Coach

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A multi-agent AI fitness coaching system using LangGraph for orchestration and OpenAI for intelligence.**

[Features](#-features) • [Architecture](#-architecture) • [Installation](#-installation) • [Documentation](#-documentation)

</div>

---

## 🎯 Overview

AthletixAI is an intelligent fitness coaching platform that combines:

- **Computer Vision** for exercise form analysis
- **Nutrition AI** for food image macro calculation
- **Wearable Integration** for recovery monitoring
- **Adaptive Training** for personalized workout programs

## ✨ Features

| Feature                      | Description                                                       |
| ---------------------------- | ----------------------------------------------------------------- |
| 🍎 **Nutrition Analysis**    | Photograph meals → Get protein, carbs, fats, fiber, calories      |
| 🏋️ **5-Day Programs**        | Comprehensive Push/Pull/Legs split with 13-15 exercises/day       |
| 🧘 **Warmup & Stretching**   | Built-in dynamic warmups and static cooldowns                     |
| 📊 **Recovery Tracking**     | HRV, sleep, and activity analysis for training readiness          |
| 🎯 **Form Analysis**         | Video frame analysis for movement quality                         |
| 🔄 **Adaptive Optimization** | Automatic program adjustments based on feedback                   |
| 🔍 **Exercise Research**     | Auto-search for tutorials, videos, GIFs for every exercise        |
| 🗄️ **Long-term Memory**      | Supabase storage for user profiles, programs, workout history     |
| 📚 **Educational Resources** | Each exercise includes tutorial URLs, breathing guides, form tips |

---

## 🏗️ Architecture

### System Overview

```mermaid
flowchart TB
    subgraph Input["📥 User Inputs"]
        UP[User Profile]
        VF[Video Frames]
        FI[Food Images]
        WD[Wearable Data]
    end

    subgraph Orchestration["🔄 LangGraph Orchestration"]
        direction LR
        ORC[Orchestrator]
        CV[CV Agent]
        WA[Wearable Agent]
        NA[Nutrition Agent]
        RA[Research Agent]
        PA[Planner Agent]
        CA[Coach Agent]
        AA[Adaptation Agent]
    end

    subgraph Memory["🗄️ Memory System"]
        CACHE[(Supabase Cache)]
        HIST[(Workout History)]
    end

    subgraph Output["📤 Outputs"]
        TP[Training Program]
        CM[Coaching Message]
        NM[Nutrition Macros]
    end

    UP --> ORC
    VF --> CV
    FI --> NA
    WD --> WA

    ORC --> CV --> WA --> NA --> RA --> PA --> CA --> AA
    RA -.->|Cache| CACHE
    RA -.->|Retrieve| CACHE
    PA -.->|Save| HIST
    AA -->|needs_replan| PA
    AA -->|complete| Output

    PA --> TP
    CA --> CM
    NA --> NM
```

### Agent Pipeline

```mermaid
sequenceDiagram
    participant User
    participant Orchestrator
    participant Research
    participant Planner
    participant Supabase

    User->>Orchestrator: Profile + Goals
    Orchestrator->>Research: Find exercise resources
    Research->>Supabase: Check cache
    alt Cache miss
        Research->>Tavily: Search tutorials/videos/GIFs
        Research->>Supabase: Cache results (30 days)
    end
    Research->>Planner: Exercise resources
    Planner->>Planner: Generate 5-day program
    Planner->>Planner: Enrich with URLs
    Planner->>User: Program with tutorials
```

### Agent Pipeline

```mermaid
sequenceDiagram
    participant U as User
    participant O as Orchestrator
    participant CV as CV Agent
    participant W as Wearable Agent
    participant N as Nutrition Agent
    participant P as Planner Agent
    participant C as Coach Agent
    participant A as Adaptation Agent

    U->>O: Profile + Images + Data
    O->>CV: Validate & Route
    CV->>W: Movement Assessment
    W->>N: Recovery Metrics
    N->>P: Nutrition Analysis
    P->>C: Training Program
    C->>A: Coaching Message
    A-->>P: Replan (if needed)
    A->>U: Final Results
```

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

# Configure environment
cp .env.example .env
# Edit .env and add your API keys:
# - OPENAI_API_KEY (required)
# - TAVILY_API_KEY (optional, for exercise research)
# - SUPABASE_URL and SUPABASE_KEY (optional, for memory)
```

### Supabase Setup (Optional)

For long-term memory and exercise caching:

1. Create account at [supabase.com](https://supabase.com)
2. Create new project
3. Run migration: Copy `migrations/001_initial_schema.sql` to SQL Editor
4. Get credentials from **Settings → API**
5. Add to `.env`:
   ```bash
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

See [docs/SUPABASE_SETUP.md](docs/SUPABASE_SETUP.md) for detailed instructions.

## 📖 Usage

### Interactive Mode (Recommended)

```bash
python -m src.main --program-only
# Choose: 1=Sample, 2=Create new profile, 3=Specify file
```

### Nutrition Analysis Only

```bash
python -m src.main --nutrition-only --food-images meal.jpg
```

### Full Mode

```bash
python -m src.main --profile user.json --food-images meal.jpg
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

| Document                                    | Description                                             |
| ------------------------------------------- | ------------------------------------------------------- |
| [HLD.md](docs/HLD.md)                       | High-Level Design - Architecture, components, data flow |
| [LLD.md](docs/LLD.md)                       | Low-Level Design - Classes, methods, algorithms, APIs   |
| [SUPABASE_SETUP.md](docs/SUPABASE_SETUP.md) | Supabase database setup and configuration guide         |

## 🔒 Safety

- Input validation (age, weight, height ranges)
- Weekly volume caps per muscle group
- Injury-aware exercise modifications
- Conservative progression (max 10%/week)
- Automatic health disclaimers

## 🛠️ Tech Stack

| Category        | Technology                    |
| --------------- | ----------------------------- |
| Orchestration   | LangGraph (StateGraph)        |
| AI              | OpenAI GPT-4o, GPT-4o Vision  |
| Data Validation | Pydantic v2                   |
| Database        | Supabase (PostgreSQL)         |
| Search          | Tavily API                    |
| Memory          | LangGraph Checkpoints, SQLite |
| Persistence     | SQLite                        |
| Testing         | pytest                        |

## 📝 License

MIT License

---

<div align="center">
Made with 💪 by AthletixAI Team
</div>
