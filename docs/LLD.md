# Low-Level Design (LLD) - AthletixAI

## 1. Overview

This document provides detailed technical specifications including class diagrams, sequence diagrams, API contracts, and implementation algorithms.

---

## 2. Class Diagrams

### 2.1 Domain Models

```mermaid
classDiagram
    class UserProfile {
        +str user_id
        +str name
        +int age
        +Gender gender
        +float height_cm
        +float weight_kg
        +ExperienceLevel experience_level
        +List~str~ injury_history
        +List~str~ equipment_available
        +bmi() float
    }

    class FoodPreferences {
        +List~DietaryRestriction~ dietary_restrictions
        +List~str~ allergies
        +int calorie_target
        +float protein_target_g
        +float carbs_target_g
        +float fats_target_g
    }

    class FitnessGoals {
        +str primary_goal
        +List~str~ secondary_goals
        +float target_weight_kg
        +int weekly_workout_days
        +int session_duration_minutes
    }

    UserProfile "1" --> "0..1" FoodPreferences
    UserProfile "1" --> "0..1" FitnessGoals
```

### 2.2 Nutrition Models

```mermaid
classDiagram
    class FoodItem {
        +str name
        +str portion_size
        +float protein_g
        +float carbs_g
        +float fats_g
        +float fiber_g
        +float calories
        +float confidence
    }

    class DailyMacros {
        +float protein_g
        +float carbs_g
        +float fats_g
        +float calories
        +float fiber_g
        +add(other) DailyMacros
    }

    class MealAnalysis {
        +MealType meal_type
        +List~FoodItem~ food_items
        +DailyMacros total_macros
        +float health_score
        +List~str~ suggestions
    }

    class NutritionAnalysis {
        +List~MealAnalysis~ daily_meals
        +DailyMacros daily_totals
        +calculate_daily_totals() void
        +check_targets() void
    }

    NutritionAnalysis "1" *-- "*" MealAnalysis
    MealAnalysis "1" *-- "*" FoodItem
    MealAnalysis "1" *-- "1" DailyMacros
    NutritionAnalysis "1" *-- "1" DailyMacros
```

### 2.3 Training Program Models

```mermaid
classDiagram
    class Exercise {
        +str name
        +int sets
        +str reps
        +int rest_seconds
        +str weight_suggestion
        +List~str~ technique_cues
    }

    class DailyWorkout {
        +int day_number
        +str day_name
        +str focus
        +List~Exercise~ exercises
        +int estimated_duration_minutes
        +bool is_rest_day
    }

    class WeeklySchedule {
        +int week_number
        +List~DailyWorkout~ workouts
    }

    class TrainingProgram {
        +str program_name
        +int program_length_weeks
        +str weekly_split
        +List~WeeklySchedule~ weekly_schedules
        +List~ProgressionRule~ progression_rules
        +str difficulty_level
    }

    TrainingProgram "1" *-- "*" WeeklySchedule
    WeeklySchedule "1" *-- "5+" DailyWorkout
    DailyWorkout "1" *-- "10-15" Exercise
```

### 2.4 Research Models

```mermaid
classDiagram
    class ExerciseResource {
        +str exercise_name
        +Optional~str~ tutorial_url
        +Optional~str~ gif_url
        +Optional~str~ video_url
        +List~str~ image_urls
        +Optional~str~ breathing_guide
        +List~str~ common_mistakes
        +str source
        +float confidence_score
        +datetime cached_at
    }

    class ResearchResults {
        +dict~str,ExerciseResource~ exercises
        +datetime search_timestamp
        +get_resource(name) Optional~ExerciseResource~
    }

    ResearchResults "1" *-- "*" ExerciseResource
```

### 2.5 Memory Models

```mermaid
classDiagram
    class UserMemory {
        +Client supabase
        +is_enabled() bool
        +save_user_profile(profile) str
        +load_user_profile(user_id) UserProfile
        +save_training_program(user_id, program) str
        +get_active_program(user_id) TrainingProgram
        +cache_exercise_resource(resource) void
        +get_cached_exercise_resource(name) ExerciseResource
        +get_workout_history(user_id, limit) list
    }

    class SessionCache {
        +dict cache
        +str session_id
        +Optional~str~ user_id
        +datetime created_at
        +set(key, value) void
        +get(key, default) Any
        +update(data) void
        +clear() void
        +to_dict() dict
    }

    UserMemory --> "uses" Supabase
    SessionCache --> "stores" State
```

---

## 3. State Management

### 3.1 FitnessState Structure

```mermaid
classDiagram
    class FitnessState {
        <<TypedDict>>
        +UserProfile user_profile
        +FoodPreferences food_preferences
        +FitnessGoals goals
        +List~str~ video_frames
        +List~str~ food_images
        +dict wearable_data
        +MovementAssessment movement_assessment
        +WearableMetrics wearable_metrics
        +NutritionAnalysis nutrition_analysis
        +TrainingProgram program
        +WeeklyFeedback weekly_feedback
        +str coaching_message
        +List~str~ daily_tips
        +str current_agent
        +bool needs_replan
        +List~dict~ messages
    }
```

---

## 4. Agent Implementations

### 4.1 Agent Interface Pattern

````mermaid
classDiagram
    class AgentNode {
        <<interface>>
        +__call__(state: FitnessState) dict
    }

    class OrchestratorNode {
        +__call__(state) dict
        -validate_inputs()
        -log_summary()
    }

    class NutritionAgentNode {
        +__call__(state) dict
        -analyze_image(image)
        -parse_response(json)
        -calculate_totals()
    }

    class PlannerAgentNode {
        +__call__(state) dict
        -build_prompt()
        -parse_program(json)
        -create_default_program()
    }

    AgentNode <|.. OrchestratorNode
    AgentNode <|.. NutritionAgentNode
    AgentNode <|.. PlannerAgentNode
```mermaid
classDiagram
    class FitnessState {
        <<TypedDict>>
        +UserProfile user_profile
        +FoodPreferences food_preferences
        +FitnessGoals goals
        +List~str~ video_frames
        +List~str~ food_images
        +dict wearable_data
        +MovementAssessment movement_assessment
        +WearableMetrics wearable_metrics
        +NutritionAnalysis nutrition_analysis
        +ResearchResults exercise_resources
        +TrainingProgram program
        +WeeklyFeedback weekly_feedback
        +str coaching_message
        +List~str~ daily_tips
        +str current_agent
        +bool needs_replan
        +List~dict~ messages
        +str session_id
        +List~dict~ user_history
        +str thread_id
    }
````

---

## 4. Agent Implementations

### 4.1 Agent Interface Pattern

```mermaid
classDiagram
    class AgentNode {
        <<interface>>
        +__call__(state: FitnessState) dict
    }

    class OrchestratorNode {
        +__call__(state) dict
        -validate_inputs()
        -log_summary()
    }

    class ResearchAgentNode {
        +__call__(state) dict
        -extract_exercise_names()
        -search_exercise_resources(name)
        -check_cache()
        -parse_results()
    }

    class NutritionAgentNode {
        +__call__(state) dict
        -analyze_image(image)
        -parse_response(json)
        -calculate_totals()
    }

    class PlannerAgentNode {
        +__call__(state) dict
        -build_prompt()
        -parse_program(json)
        -enrich_program_with_resources()
        -create_default_program()
    }

    AgentNode <|.. OrchestratorNode
    AgentNode <|.. ResearchAgentNode
    AgentNode <|.. NutritionAgentNode
    AgentNode <|.. PlannerAgentNode
```

### 4.2 Research Agent Sequence

```mermaid
sequenceDiagram
    participant P as Planner
    participant R as ResearchAgent
    participant C as Supabase Cache
    participant T as Tavily API

    P->>R: Exercise names
    loop For each exercise
        R->>C: Check cache
        alt Cache hit (< 30 days)
            C-->>R: ExerciseResource
        else Cache miss
            R->>T: Search tutorial
            R->>T: Search video
            R->>T: Search GIF
            T-->>R: Results
            R->>R: Parse & filter URLs
            R->>C: Cache resource (30d TTL)
        end
    end
    R-->>P: ResearchResults
    P->>P: Enrich program with URLs
```

### 4.3 Nutrition Agent Sequence

```mermaid
sequenceDiagram
    participant C as Client
    participant NA as NutritionAgent
    participant OAI as OpenAI API
    participant P as Parser

    C->>NA: food_images[]
    loop For each image
        NA->>NA: Build prompt with dietary context
        NA->>OAI: Vision API call
        OAI-->>NA: JSON response (may be markdown-wrapped)
        NA->>P: _extract_json()
        P-->>NA: Clean JSON
        NA->>NA: Parse to MealAnalysis
    end
    NA->>NA: calculate_daily_totals()
    NA-->>C: NutritionAnalysis
```

### 4.3 Planner Agent Algorithm

```mermaid
flowchart TD
    START([Start]) --> CHECK{needs_replan?}

    CHECK -->|Yes| ADAPT[Adapt Existing Program]
    CHECK -->|No| NEW[Generate New Program]

    NEW --> BUILD[Build LLM Prompt]
    BUILD --> CALL[Call GPT-4o]
    CALL --> PARSE{Parse JSON}

    PARSE -->|Success| VALID[Validate Program]
    PARSE -->|Error| DEFAULT[Use Default 5-Day Program]

    ADAPT --> MODIFY[Apply Feedback Modifications]
    MODIFY --> VALID

    VALID --> RETURN([Return TrainingProgram])
    DEFAULT --> RETURN
```

---

## 5. Graph Topology

### 5.1 LangGraph Structure

```mermaid
flowchart LR
    subgraph Graph["StateGraph~FitnessState~"]
        direction LR
        E([Entry]) --> O[orchestrator]
        O --> CV[cv_agent]
        CV --> W[wearable_agent]
        W --> N[nutrition_agent]
        N --> R[research_agent]
        R --> P[planner_agent]
        P --> C[coach_agent]
        C --> A[adaptation_agent]
        A --> D{should_replan?}
        D -->|True| P
        D -->|False| END([END])
    end
```

### 5.2 Graph Construction Code

```python
def create_fitness_graph() -> StateGraph:
    graph = StateGraph(FitnessState)

    # Add nodes
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("cv_agent", cv_agent_node)
    graph.add_node("wearable_agent", wearable_agent_node)
    graph.add_node("nutrition_agent", nutrition_agent_node)
    graph.add_node("research_agent", research_agent_node)  # NEW
    graph.add_node("planner_agent", planner_agent_node)
    graph.add_node("coach_agent", coach_agent_node)
    graph.add_node("adaptation_agent", adaptation_agent_node)

    # Linear edges
    graph.add_edge("orchestrator", "cv_agent")
    graph.add_edge("cv_agent", "wearable_agent")
    graph.add_edge("wearable_agent", "nutrition_agent")
    graph.add_edge("nutrition_agent", "research_agent")  # NEW
    graph.add_edge("research_agent", "planner_agent")    # NEW
    graph.add_edge("planner_agent", "coach_agent")
    graph.add_edge("coach_agent", "adaptation_agent")

    # Conditional edge (feedback loop)
    graph.add_conditional_edges(
        "adaptation_agent",
        should_replan,
        {True: "planner_agent", False: END}
    )

    graph.set_entry_point("orchestrator")
    return graph
```

---

## 6. API Specifications

### 6.1 OpenAI Client Interface

```mermaid
classDiagram
    class OpenAIClient {
        <<module>>
        +get_vision_response(prompt, images, max_tokens) str
        +get_structured_response(system, user, max_tokens) str
        +get_chat_model() str
        +get_vision_model() str
        -encode_image_base64(path) str
    }
```

### 6.2 Request/Response Flow

```mermaid
sequenceDiagram
    participant A as Agent
    participant C as OpenAI Client
    participant API as OpenAI API

    A->>C: get_vision_response(prompt, [images])
    C->>C: Encode images to base64
    C->>C: Build messages array
    C->>API: POST /chat/completions
    API-->>C: Response with content
    C->>C: Extract text content
    C-->>A: Raw response string
    A->>A: _extract_json()
    A->>A: Parse to Pydantic model
```

---

## 7. Safety Module

### 7.1 Validation Flow

```mermaid
flowchart TD
    INPUT[User Input] --> VAL{Validate Profile}

    VAL -->|Invalid| ERR[Return Errors]
    VAL -->|Valid| RANGE{Check Ranges}

    RANGE -->|Age 13-100| OK1[✓]
    RANGE -->|Weight 30-300kg| OK2[✓]
    RANGE -->|Height 100-250cm| OK3[✓]

    OK1 & OK2 & OK3 --> GUARD[Apply Guardrails]

    GUARD --> VOL[Volume Caps]
    GUARD --> INJ[Injury Modifications]
    GUARD --> PRO[Progression Limits]

    VOL & INJ & PRO --> DISCLAIM[Add Disclaimers]
    DISCLAIM --> OUTPUT[Safe Output]
```

### 7.2 Guardrails Implementation

```python
class SafetyGuardrails:
    MAX_WEEKLY_SETS_PER_MUSCLE = 25
    MIN_REST_DAYS = 2
    MAX_PROGRESSION_PERCENT = 10

    INJURY_MODIFICATIONS = {
        "lower back": ["deadlift", "good morning"],
        "shoulder": ["overhead press", "upright row"],
        "knee": ["deep squat", "jumping"]
    }

    @staticmethod
    def apply_volume_cap(program: TrainingProgram) -> TrainingProgram:
        # Limit total sets per muscle group

    @staticmethod
    def apply_injury_modifications(
        program: TrainingProgram,
        injuries: list[str]
    ) -> TrainingProgram:
        # Substitute or remove risky exercises
```

---

## 8. Error Handling

```mermaid
flowchart TD
    subgraph Errors["Error Categories"]
        API[API Errors]
        PARSE[Parse Errors]
        VAL[Validation Errors]
        IO[I/O Errors]
    end

    subgraph Handlers["Handling Strategies"]
        RETRY[Retry with Backoff]
        EXTRACT[JSON Extraction Fallback]
        DEFAULT[Default Values]
        LOG[Log & Continue]
    end

    API --> RETRY
    PARSE --> EXTRACT
    VAL --> DEFAULT
    IO --> LOG
```

| Error              | Strategy                          | Fallback               |
| ------------------ | --------------------------------- | ---------------------- |
| OpenAI API timeout | Retry 3x with exponential backoff | Use default program    |
| JSON parse error   | Try markdown extraction patterns  | Log warning, skip item |
| Invalid profile    | Return validation errors          | Block execution        |
| Image not found    | Log warning                       | Skip image             |

---

## 9. Testing Strategy

```mermaid
flowchart LR
    subgraph Unit["Unit Tests"]
        UM[Model Validation]
        UA[Agent Logic]
        UP[Parser Functions]
    end

    subgraph Integration["Integration Tests"]
        IG[Graph Flow]
        IA[API Mocking]
    end

    subgraph E2E["End-to-End"]
        EC[CLI Commands]
        EO[Output Validation]
    end

    Unit --> Integration --> E2E
```

---

## 10. File Structure

```
src/
├── main.py                 # CLI entry, interactive mode
├── graph.py                # LangGraph StateGraph construction
├── state.py                # FitnessState TypedDict
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py     # Input validation, routing
│   ├── cv_agent.py         # Video frame analysis
│   ├── wearable_agent.py   # Device data interpretation
│   ├── nutrition_agent.py  # Food image → macros
│   ├── research_agent.py   # Exercise resource search (Tavily)
│   ├── planner_agent.py    # 5-day program generation
│   ├── coach_agent.py      # Motivational messaging
│   └── adaptation_agent.py # Feedback loop logic
├── models/
│   ├── user_profile.py     # UserProfile, Goals, Preferences
│   ├── assessment.py       # MovementAssessment
│   ├── wearables.py        # WearableMetrics
│   ├── nutrition.py        # FoodItem, MealAnalysis
│   ├── program.py          # TrainingProgram, Exercise
│   ├── research.py         # ExerciseResource, ResearchResults
│   ├── session.py          # WorkoutSession, SessionSummary
│   └── feedback.py         # WeeklyFeedback
├── memory/
│   ├── user_memory.py      # Supabase integration
│   ├── session_cache.py    # In-memory session state
│   └── persistence.py      # SQLite storage
├── safety/
│   ├── validators.py       # Input validation functions
│   ├── guardrails.py       # Training safety limits
│   └── disclaimers.py      # Health warning generation
└── utils/
    ├── openai_client.py    # API wrapper functions
    └── prompts.py          # Agent prompt templates
```

---

## 11. References

- [HLD.md](HLD.md) - High-Level Design
- [README.md](../README.md) - User Guide
