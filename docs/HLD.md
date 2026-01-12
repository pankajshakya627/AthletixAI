# High-Level Design (HLD) - AthletixAI

## 1. Executive Summary

**AthletixAI** is a multi-agent AI fitness coaching system that provides personalized training programs, nutrition analysis, and adaptive coaching using LangGraph orchestration and OpenAI GPT-4o.

| Attribute          | Value                                    |
| ------------------ | ---------------------------------------- |
| Architecture Style | Event-driven Multi-Agent System          |
| Orchestration      | LangGraph StateGraph                     |
| AI Provider        | OpenAI (GPT-4o, GPT-4o Vision), Tavily   |
| Data Store         | Supabase (PostgreSQL), SQLite (Fallback) |

---

## 2. System Context Diagram

```mermaid
C4Context
    title System Context - AthletixAI

    Person(user, "Fitness User", "Tracks nutrition, follows training programs")

    System(athletix, "AthletixAI", "Multi-agent AI fitness coaching platform")

    System_Ext(openai, "OpenAI API", "GPT-4o and Vision models")
    System_Ext(wearables, "Wearable APIs", "Fitbit, Garmin, Apple Health")
    System_Ext(storage, "Cloud Storage", "Image and video storage")

    Rel(user, athletix, "Uses", "CLI/API")
    Rel(athletix, openai, "Calls", "HTTPS/REST")
    Rel(athletix, wearables, "Fetches data", "OAuth/REST")
    Rel(athletix, storage, "Stores media", "S3/GCS")
```

---

## 3. High-Level Architecture

```mermaid
flowchart TB
    subgraph Presentation["Presentation Layer"]
        CLI[CLI - main.py]
        API[REST API - Future]
        UI[Streamlit UI - Future]
    end

    subgraph Orchestration["Orchestration Layer - LangGraph"]
        GR[StateGraph Engine]
        SM[State Manager]
        CR[Conditional Router]
    end

    subgraph Agents["Agent Layer"]
        direction LR
        ORC[Orchestrator]
        CVA[CV Agent]
        WAA[Wearable Agent]
        NUA[Nutrition Agent]
        PLA[Planner Agent]
        COA[Coach Agent]
        ADA[Adaptation Agent]
    end

    subgraph Domain["Domain Layer"]
        MOD[Pydantic Models]
        SAF[Safety Guardrails]
        VAL[Validators]
    end

    subgraph Data["Data Layer"]
        SES[Session Memory]
        PER[SQLite Persistence]
        CAC[Response Cache - Future]
    end

    subgraph External["External Services"]
        OAI[OpenAI API]
        WRB[Wearable APIs]
    end

    Presentation --> Orchestration
    Orchestration --> Agents
    Agents --> Domain
    Agents --> Data
    Agents --> External
```

---

## 4. Agent Architecture

### 4.1 Agent Flow Diagram

```mermaid
stateDiagram-v2
    [*] --> Orchestrator: User Input

    Orchestrator --> CVAgent: Video Frames
    Orchestrator --> WearableAgent: Device Data

    CVAgent --> WearableAgent: Movement Assessment
    WearableAgent --> NutritionAgent: Recovery Metrics
    NutritionAgent --> PlannerAgent: Nutrition Analysis
    PlannerAgent --> CoachAgent: Training Program
    CoachAgent --> AdaptationAgent: Coaching Message

    AdaptationAgent --> PlannerAgent: needs_replan = true
    AdaptationAgent --> [*]: needs_replan = false
```

### 4.2 Agent Specifications

| Agent              | Type          | LLM            | Responsibility                              |
| ------------------ | ------------- | -------------- | ------------------------------------------- |
| Orchestrator       | Deterministic | None           | Input validation, routing                   |
| CV Agent           | AI            | GPT-4o Vision  | Exercise form analysis                      |
| Wearable Agent     | AI            | GPT-4o         | Recovery metrics interpretation             |
| Nutrition Agent    | AI            | GPT-4o Vision  | Food → macro calculation                    |
| **Research Agent** | **AI**        | **Tavily API** | **Exercise tutorials, GIFs, videos search** |
| Planner Agent      | AI            | GPT-4o         | Training program generation                 |
| Coach Agent        | AI            | GPT-4o         | Human-like coaching messages                |
| Adaptation Agent   | Deterministic | None           | Feedback analysis, replan decision          |

---

## 5. Data Flow

### 5.1 Nutrition Analysis Pipeline

```mermaid
flowchart LR
    subgraph Input
        IMG[Food Image]
        PREF[Dietary Preferences]
    end

    subgraph Processing
        ENC[Base64 Encode]
        API[GPT-4o Vision API]
        PAR[JSON Parser]
        VAL[Validator]
    end

    subgraph Output
        MEAL[MealAnalysis]
        MAC[DailyMacros]
        SUG[Suggestions]
    end

    IMG --> ENC --> API
    PREF --> API
    API --> PAR --> VAL
    VAL --> MEAL --> MAC
    VAL --> SUG
```

### 5.2 Program Generation Pipeline

```mermaid
flowchart LR
    subgraph Context
        PRO[User Profile]
        ASS[Assessments]
        WEA[Wearable Metrics]
        GOA[Goals]
    end

    subgraph Generation
        PRM[Prompt Builder]
        LLM[GPT-4o]
        PRS[JSON Parser]
        DEF[Default Fallback]
    end

    subgraph Output
        PGM[TrainingProgram]
        WKT[5 DailyWorkouts]
        EXE[13-15 Exercises/Day]
    end

    Context --> PRM --> LLM --> PRS --> PGM --> WKT --> EXE
    PRS -.->|On Error| DEF --> PGM
```

### 5.3 Exercise Research Pipeline

```mermaid
flowchart TB
    subgraph Input
        EXERCISES[Exercise Names]
    end

    subgraph Cache["Supabase Cache"]
        CHECK{Check Cache}
        CACHED[(30-day TTL)]
    end

    subgraph Search["Tavily Search"]
        Q1[Tutorial Query]
        Q2[Video Query]
        Q3[GIF Query]
        TAVILY[Tavily API]
    end

    subgraph Processing
        FILTER[Filter Results]
        PARSE[Parse URLs]
    end

    subgraph Output
        RESOURCE[ExerciseResource]
        TUTORIAL[tutorial_url]
        VIDEO[video_url]
        GIF[gif_url]
        IMAGES[image_urls]
    end

    EXERCISES --> CHECK
    CHECK -->|Hit| CACHED --> RESOURCE
    CHECK -->|Miss| Q1
    Q1 --> TAVILY
    Q2 --> TAVILY
    Q3 --> TAVILY
    TAVILY --> FILTER --> PARSE
    PARSE --> RESOURCE
    RESOURCE --> TUTORIAL
    RESOURCE --> VIDEO
    RESOURCE --> GIF
    RESOURCE --> IMAGES
    RESOURCE -.->|Cache 30d| CACHED
```

---

## 6. Technology Stack

```mermaid
mindmap
  root((AthletixAI))
    Orchestration
      LangGraph
      StateGraph
      Conditional Edges
      Checkpoints
    AI/ML
      OpenAI GPT-4o
      GPT-4o Vision
      Tavily Search
      Structured Output
    Data
      Pydantic v2
      TypedDict
      Supabase PostgreSQL
      SQLite Fallback
    Memory
      Long-term Supabase
      Short-term Cache
      Exercise Resources
      Workout History
    Safety
      Input Validators
      Volume Caps
      Injury Guards
    Interface
      CLI argparse
      Future REST API
      Future Streamlit
```

---

## 7. Deployment Architecture

### 7.1 Current (MVP)

```mermaid
flowchart LR
    subgraph Local["Local Machine"]
        CLI[Python CLI]
        APP[AthletixAI App]
        DB[(SQLite)]
    end

    subgraph Cloud["External"]
        OAI[OpenAI API]
    end

    CLI --> APP --> DB
    APP <--> OAI
```

### 7.2 Future (Production)

```mermaid
flowchart TB
    subgraph Client["Client Layer"]
        WEB[Web App]
        MOB[Mobile App]
        CLI[CLI]
    end

    subgraph API["API Gateway"]
        GW[API Gateway]
        AUTH[Auth Service]
    end

    subgraph Services["Service Layer"]
        ORG[Orchestrator Service]
        AGT[Agent Workers]
        CAC[Redis Cache]
    end

    subgraph Data["Data Layer"]
        PG[(PostgreSQL)]
        S3[(S3 Storage)]
    end

    Client --> GW --> AUTH --> ORG
    ORG --> AGT --> CAC
    AGT --> PG
    AGT --> S3
```

---

## 8. Security Considerations

| Concern          | Mitigation                        |
| ---------------- | --------------------------------- |
| API Key Exposure | Environment variables, .gitignore |
| PII Protection   | Local storage, no cloud logging   |
| Input Validation | Pydantic models, range checks     |
| Training Safety  | Volume caps, progression limits   |

---

## 9. Quality Attributes

| Attribute           | Approach                                    |
| ------------------- | ------------------------------------------- |
| **Reliability**     | Fallback to default programs on LLM failure |
| **Maintainability** | Modular agent architecture, type hints      |
| **Extensibility**   | New agents via add_node()                   |
| **Testability**     | Pure functions, dependency injection        |

---

## 10. References

- [LLD.md](LLD.md) - Low-Level Design
- [README.md](../README.md) - User Guide
