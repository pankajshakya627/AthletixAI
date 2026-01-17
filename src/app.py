
import streamlit as st
import json
import os
import sys
import glob
from dotenv import load_dotenv

# Add src to python path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import run_program_with_profile
from src.models.user_profile import UserProfile

# Page Config
st.set_page_config(
    page_title="AI Fitness Coach",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stButton button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    .workout-day-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 20px;
    }
    .exercise-link {
        text-decoration: none;
        color: #ff4b4b;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


def load_profiles():
    """Load all JSON profiles from the root directory."""
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    files = glob.glob(os.path.join(root_dir, "*.json"))
    profiles = {}
    for f in files:
        filename = os.path.basename(f)
        try:
            with open(f, 'r') as fp:
                data = json.load(fp)
                # Check if it looks like a profile (has name, age, etc.)
                if "name" in data and "age" in data:
                    profiles[filename] = data
        except Exception:
            continue
    return profiles


# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/weightlifting.png", width=80)
    st.title("FitAI Coach")
    st.markdown("---")
    
    st.header("👤 User Profile")
    
    profiles = load_profiles()
    if not profiles:
        st.error("No profile JSON files found in root directory!")
        st.stop()
        
    selected_filename = st.selectbox(
        "Select Profile",
        options=list(profiles.keys()),
        index=0
    )
    
    selected_profile_data = profiles[selected_filename]
    
    # Preview
    with st.expander("Profile Details", expanded=True):
        st.write(f"**Name:** {selected_profile_data.get('name')}")
        st.write(f"**Age:** {selected_profile_data.get('age')}")
        st.write(f"**Goal:** {selected_profile_data.get('primary_goal')}")
        st.write(f"**Level:** {selected_profile_data.get('experience_level')}")
        
    if st.button("🚀 Generate Program", type="primary"):
        with st.spinner("🤖 AI Agents are working... (Researching exercises, analyzing profile)"):
            try:
                # Convert dict to UserProfile object
                user_profile = UserProfile(**selected_profile_data)
                
                # Run the actual agent pipeline
                state = run_program_with_profile(user_profile)
                
                # Save to session state
                st.session_state["program_state"] = state
                st.session_state["generated_for"] = selected_filename
                st.success("Program Generated Successfully!")
                st.rerun() # Refresh to show results
                
            except Exception as e:
                st.error(f"Error generating program: {str(e)}")
                import traceback
                st.code(traceback.format_exc())


# --- MAIN CONTENT ---

if "program_state" not in st.session_state:
    # Landing State
    st.title("💪 Welcome to AI Fitness Coach")
    st.markdown("""
    Your personalized AI coach will create a fully customized workout plan based on your:
    
    *   **Experience Level** (Beginner to Advanced)
    *   **Goals** (Muscle Gain, Strength, Weight Loss)
    *   **Equipment Available**
    *   **Injuries & Constraints**
    
    👈 **Select a profile on the left and click 'Generate Program' to start!**
    """)
    
    st.info("💡 **Did you know?** The AI research agent searches the web for the best tutorials for every exercise in your plan.")

else:
    # Result State
    state = st.session_state["program_state"]
    program = state.get("program")
    coaching_message = state.get("coaching_message")
    daily_tips = state.get("daily_tips", [])
    
    # Header
    st.title(f"🏋️ {program.program_name}")
    st.caption(f"Generated for: {st.session_state['generated_for']} | {program.program_length_weeks} Weeks | {program.weekly_split}")
    
    # Tabs
    tab_overview, tab_workouts, tab_schedule = st.tabs(["📊 Overview & Tips", "📅 Workouts", "📆 Schedule"])
    
    # --- TAB 1: OVERVIEW ---
    with tab_overview:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📣 Coach's Message")
            st.info(coaching_message)
            
        with col2:
            st.subheader("💡 Daily Tips")
            for tip in daily_tips:
                st.markdown(f"✅ {tip}")
                
        st.subheader("Progression Rules")
        if program.progression_rules:
            for rule in program.progression_rules:
                st.markdown(f"- **{rule.rule_type.title()}**: {rule.condition}")
        else:
            st.write("Follow standard progressive overload.")

    # --- TAB 2: WORKOUTS ---
    with tab_workouts:
        if not program.weekly_schedules:
            st.warning("No workouts found in program.")
        else:
            week = program.weekly_schedules[0]
            
            # Create sub-tabs for each day
            day_names = [w.day_name for w in week.workouts]
            workout_tabs = st.tabs(day_names)
            
            for i, workout_tab in enumerate(workout_tabs):
                workout = week.workouts[i]
                with workout_tab:
                    st.markdown(f"### 🔥 Focus: {workout.focus}")
                    st.write(f"⏱️ **Duration:** ~{workout.estimated_duration_minutes} mins")
                    
                    # Prepare table data
                    table_data = []
                    for ex in workout.exercises:
                        # Format Resources Links
                        links = []
                        if hasattr(ex, 'tutorial_url') and ex.tutorial_url:
                            links.append(f"[📖 Tutorial]({ex.tutorial_url})")
                        if hasattr(ex, 'video_url') and ex.video_url:
                            links.append(f"[🎬 Video]({ex.video_url})")
                        
                        link_str = " | ".join(links) if links else "Searching..."
                        
                        table_data.append({
                            "Exercise": ex.name,
                            "Sets": ex.sets,
                            "Reps": ex.reps,
                            "Resources": link_str
                        })
                    
                    # Display as table
                    st.markdown("#### Exercises")
                    
                    # Custom HTML table for better link rendering than st.dataframe
                    # st.dataframe handles links poorly sometimes
                    
                    header = "| Exercise | Sets | Reps | Resources |\n|---|---|---|---|\n"
                    rows = ""
                    for row in table_data:
                        rows += f"| **{row['Exercise']}** | {row['Sets']} | {row['Reps']} | {row['Resources']} |\n"
                    
                    st.markdown(header + rows)

    # --- TAB 3: SCHEDULE ---
    with tab_schedule:
        st.write("### Weekly Schedule")
        schedule_cols = st.columns(len(program.weekly_schedules[0].workouts))
        for i, col in enumerate(schedule_cols):
            w = program.weekly_schedules[0].workouts[i]
            with col:
                st.markdown(f"**{w.day_name}**")
                st.caption(w.focus)
