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

| Feature                      | Description                                                  |
| ---------------------------- | ------------------------------------------------------------ |
| 🍎 **Nutrition Analysis**    | Photograph meals → Get protein, carbs, fats, fiber, calories |
| 🏋️ **5-Day Programs**        | Comprehensive Push/Pull/Legs split with 13-15 exercises/day  |
| 🧘 **Warmup & Stretching**   | Built-in dynamic warmups and static cooldowns                |
| 📊 **Recovery Tracking**     | HRV, sleep, and activity analysis for training readiness     |
| 🎯 **Form Analysis**         | Video frame analysis for movement quality                    |
| 🔄 **Adaptive Optimization** | Automatic program adjustments based on feedback              |

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
        PA[Planner Agent]
        CA[Coach Agent]
        AA[Adaptation Agent]
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

    ORC --> CV --> WA --> NA --> PA --> CA --> AA
    AA -->|needs_replan| PA
    AA -->|complete| Output

    PA --> TP
    CA --> CM
    NA --> NM
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

# Install dependencies
pip install -e ".[dev]"

# Configure environment
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

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
│   ├── HLD.md              # High-Level Design
│   └── LLD.md              # Low-Level Design
├── src/
│   ├── main.py             # CLI entry point
│   ├── graph.py            # LangGraph topology
│   ├── state.py            # FitnessState TypedDict
│   ├── agents/             # 7 specialized agents
│   ├── models/             # Pydantic data models
│   ├── memory/             # Session & persistence
│   ├── safety/             # Guardrails & validators
│   └── utils/              # OpenAI client & prompts
├── tests/
├── pyproject.toml
└── sample_user.json
```

## 📚 Documentation

| Document              | Description                                                    |
| --------------------- | -------------------------------------------------------------- |
| [HLD.md](docs/HLD.md) | High-Level Design - System architecture, components, data flow |
| [LLD.md](docs/LLD.md) | Low-Level Design - Classes, methods, algorithms, APIs          |

## 🔒 Safety

- Input validation (age, weight, height ranges)
- Weekly volume caps per muscle group
- Injury-aware exercise modifications
- Conservative progression (max 10%/week)
- Automatic health disclaimers

## 🛠️ Tech Stack

| Category        | Technology                   |
| --------------- | ---------------------------- |
| Orchestration   | LangGraph (StateGraph)       |
| AI              | OpenAI GPT-4o, GPT-4o Vision |
| Data Validation | Pydantic v2                  |
| Persistence     | SQLite                       |
| Testing         | pytest                       |

## 📝 License

MIT License

---

<div align="center">
Made with 💪 by AthletixAI Team
</div>
