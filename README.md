# AI-Driven Virtual Fitness Coach

A multi-agent AI fitness coaching system built with **LangGraph** and **OpenAI API**. The system orchestrates specialized agents for exercise form analysis, wearable data interpretation, nutrition analysis from food images, program planning, coaching communication, and adaptive optimization.

## 🏗️ Architecture

```
User Input → Orchestrator → CV Agent → Wearable Agent → Nutrition Agent
                                                              ↓
                    ←───── Adaptation Agent ← Coach Agent ← Planner Agent
                    ↓
            (needs_replan?) → Loop back to Planner or END
```

### Agents

| Agent                | Role                              | LLM           |
| -------------------- | --------------------------------- | ------------- |
| **Orchestrator**     | Entry point, validation, routing  | Deterministic |
| **CV Agent**         | Exercise form analysis from video | GPT-4o Vision |
| **Wearable Agent**   | HRV, sleep, recovery analysis     | GPT-4o        |
| **Nutrition Agent**  | Food image → macros (P/C/F)       | GPT-4o Vision |
| **Planner Agent**    | Training program generation       | GPT-4o        |
| **Coach Agent**      | Human-like coaching messages      | GPT-4o        |
| **Adaptation Agent** | Feedback loop decisions           | Deterministic |

## 🚀 Quick Start

### Installation

```bash
# Clone and navigate
cd /Volumes/CrucialX9_MAC/Fitness_coach

# Install in development mode
pip install -e ".[dev]"

# Set up environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Usage

```bash
# Basic run with user profile
python -m src.main --profile sample_user.json

# With wearable data
python -m src.main --profile user.json --wearable wearable_data.json

# With food images for nutrition analysis
python -m src.main --profile user.json --food-images breakfast.jpg lunch.jpg

# Full analysis with all inputs
python -m src.main \
  --profile user.json \
  --wearable wearable.json \
  --food-images meal.jpg \
  --video-frames squat1.jpg squat2.jpg \
  --output results.json
```

### Sample User Profile (user.json)

```json
{
  "user_id": "user123",
  "name": "Alex",
  "age": 30,
  "gender": "male",
  "height_cm": 180,
  "weight_kg": 80,
  "experience_level": "intermediate",
  "equipment_available": ["dumbbells", "barbell", "pull_up_bar"],
  "injury_history": ["lower back"],
  "current_injuries": []
}
```

### Sample Wearable Data (wearable.json)

```json
{
  "resting_heart_rate": 58,
  "hrv": 65,
  "sleep_hours": 7.5,
  "sleep_score": 82,
  "steps": 8500,
  "active_calories": 450
}
```

## 📁 Project Structure

```
fitness_coach/
├── pyproject.toml          # Dependencies
├── .env.example            # Environment template
├── src/
│   ├── main.py             # CLI entry point
│   ├── graph.py            # LangGraph topology
│   ├── state.py            # FitnessState definition
│   ├── models/             # Pydantic data models
│   ├── agents/             # Agent implementations
│   ├── memory/             # Session & persistence
│   ├── safety/             # Guardrails & validators
│   └── utils/              # OpenAI client & prompts
└── tests/                  # Test suite
```

## ⚙️ Features

- **Exercise Form Analysis**: Upload video frames for biomechanics assessment
- **Nutrition Tracking**: Photograph meals for automatic macro calculation
- **Recovery Monitoring**: Integrate wearable data for training readiness
- **Adaptive Programs**: Automatic adjustments based on feedback
- **Safety Guardrails**: Volume caps, injury-aware modifications, disclaimers

## 🔒 Safety

- No medical diagnosis generation
- Conservative progression rules (max 10% weekly increase)
- Injury-aware volume caps
- Automatic health disclaimers

## 📝 License

MIT License
