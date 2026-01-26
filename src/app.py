
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
from src.memory.user_memory import UserMemory

# Initialize Memory
memory = UserMemory()

# Page Config
st.set_page_config(
    page_title="AI Fitness Coach",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Modern Design System
st.markdown("""
<style>
    /* ==========================================================================
       ROOT VARIABLES
       ========================================================================== */
    :root {
        --primary: #6366f1;       /* Indigo */
        --primary-dark: #4f46e5;
        --secondary: #22d3ee;     /* Cyan accent */
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --border-color: #334155;
        --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        --gradient-header: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* ==========================================================================
       GLOBAL STYLES
       ========================================================================== */
    .stApp {
        background: var(--bg-dark);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--text-primary) !important;
    }
    
    /* ==========================================================================
       BUTTONS
       ========================================================================== */
    .stButton > button {
        width: 100%;
        background: var(--gradient-primary) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
    }
    
    /* ==========================================================================
       CARDS & CONTAINERS
       ========================================================================== */
    .modern-card {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid var(--border-color);
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    
    .gradient-header {
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    }
    
    /* ==========================================================================
       METRICS & STATS
       ========================================================================== */
    .metric-card {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        border: 1px solid var(--border-color);
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* ==========================================================================
       TABLES
       ========================================================================== */
    .styled-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        background: var(--bg-card);
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border-color);
    }
    
    .styled-table th {
        background: linear-gradient(135deg, #334155 0%, #1e293b 100%);
        color: var(--text-primary);
        font-weight: 600;
        padding: 1rem;
        text-align: left;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
    }
    
    .styled-table td {
        padding: 0.875rem 1rem;
        border-bottom: 1px solid var(--border-color);
        color: var(--text-primary);
    }
    
    .styled-table tr:last-child td {
        border-bottom: none;
    }
    
    .styled-table tr:hover td {
        background: rgba(99, 102, 241, 0.1);
    }
    
    /* ==========================================================================
       LINKS
       ========================================================================== */
    .styled-table a {
        color: var(--secondary) !important;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s ease;
    }
    
    .styled-table a:hover {
        color: var(--primary) !important;
        text-decoration: underline;
    }
    
    /* ==========================================================================
       TABS
       ========================================================================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--bg-card);
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid var(--border-color);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 8px;
        color: var(--text-secondary);
        font-weight: 500;
        background: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--gradient-primary) !important;
        color: white !important;
    }
    
    /* ==========================================================================
       EXPANDERS
       ========================================================================== */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border-color) !important;
    }
    
    /* ==========================================================================
       STATUS BADGES
       ========================================================================== */
    .badge-success {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: rgba(16, 185, 129, 0.2);
        color: var(--success);
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .badge-warning {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: rgba(245, 158, 11, 0.2);
        color: var(--warning);
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    /* ==========================================================================
       ANIMATIONS
       ========================================================================== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease-out forwards;
    }
    
    /* ==========================================================================
       SCROLLBAR
       ========================================================================== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary);
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
    
    # Connection Status
    if memory.is_enabled():
        st.success("☁️ Cloud Sync Active")
    else:
        st.warning("⚠️ Local Storage Only")
        
    st.markdown("---")
    
    # Create New Profile Section
    with st.expander("➕ Create New Profile"):
        with st.form("create_profile_form"):
            new_name = st.text_input("Name")
            new_age = st.number_input("Age", min_value=10, max_value=100, value=30)
            new_weight = st.number_input("Weight (kg)", min_value=30.0, value=70.0)
            new_height = st.number_input("Height (cm)", min_value=100.0, value=175.0)
            new_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            new_exp = st.selectbox("Experience", ["Beginner", "Intermediate", "Advanced"])
            new_goal = st.selectbox("Goal", ["Muscle Building", "Weight Loss", "Strength", "General Fitness"])
            
            submitted = st.form_submit_button("Save Profile")
            if submitted and new_name:
                filename = f"user_{new_name.lower().replace(' ', '_')}.json"
                file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), filename)
                
                new_profile_data = {
                    "user_id": f"u_{new_name.lower().replace(' ', '_')}",  # changed from id
                    "name": new_name,
                    "age": new_age,
                    "weight_kg": new_weight,  # changed from weight
                    "height_cm": new_height,  # changed from height
                    "gender": new_gender.lower(),  # lowercase
                    "experience_level": new_exp.lower(),  # lowercase
                    "primary_goal": new_goal,
                    "medical_conditions": [],
                    "injuries": [],
                    "equipment_access": ["Gym"]
                }
                
                with open(file_path, 'w') as f:
                    json.dump(new_profile_data, f, indent=4)
                
                # Cloud Sync
                if memory.is_enabled():
                    profile_obj = UserProfile(**new_profile_data)
                    memory.save_user_profile(profile_obj)
                    st.success(f"Profile synced to Cloud!")
                
                st.success(f"Created {filename}!")
                st.rerun()

    st.markdown("---")
    st.header("👤 Select Profile")
    
    profiles = load_profiles()
    if not profiles:
        st.error("No profile JSON files found in root directory!")
        st.stop()
        
    selected_filename = st.selectbox(
        "Choose User",
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
                
                # Auto-save to Supabase
                if memory.is_enabled() and state.get("program"):
                    user_name = selected_profile_data.get("name")
                    memory.save_training_program(user_name, state["program"])
                    st.toast("💾 Program saved to Cloud history!")
                
                st.success("Program Generated Successfully!")
                st.rerun() # Refresh to show results
                
            except Exception as e:
                st.error(f"Error generating program: {str(e)}")
                import traceback
                st.code(traceback.format_exc())


# --- MAIN CONTENT ---

if "program_state" not in st.session_state:
    # Landing State
    st.markdown('<h1 class="gradient-header">💪 Welcome to AI Fitness Coach</h1>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="modern-card animate-fade-in">
        <p style="color: #94a3b8; font-size: 1.1rem; line-height: 1.8;">
            Your personalized AI coach will create a fully customized workout plan based on your:
        </p>
        <ul style="color: #f1f5f9; list-style: none; padding-left: 0;">
            <li style="margin: 0.5rem 0;">✨ <strong>Experience Level</strong> – Beginner to Elite</li>
            <li style="margin: 0.5rem 0;">🎯 <strong>Goals</strong> – Muscle Gain, Strength, Weight Loss</li>
            <li style="margin: 0.5rem 0;">🏋️ <strong>Equipment Access</strong> – Home, Gym, or Bodyweight</li>
            <li style="margin: 0.5rem 0;">🩹 <strong>Injuries & Constraints</strong> – Personalized modifications</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="modern-card" style="border-left: 4px solid #6366f1;">
        <p style="color: #f1f5f9; margin: 0;">
            👈 <strong>Select a profile on the left and click "Generate Program"</strong> to start!
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="modern-card" style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(34, 211, 238, 0.1) 100%);">
        <p style="color: #22d3ee; margin: 0;">
            💡 <strong>Did you know?</strong> The AI research agent searches the web for the best tutorials for every exercise in your plan.
        </p>
    </div>
    ''', unsafe_allow_html=True)

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
                    st.markdown(f'''
                    <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                        <div class="metric-card" style="flex: 1;">
                            <div class="metric-value">🔥</div>
                            <div class="metric-label">{workout.focus}</div>
                        </div>
                        <div class="metric-card" style="flex: 1;">
                            <div class="metric-value">{workout.estimated_duration_minutes}</div>
                            <div class="metric-label">Minutes</div>
                        </div>
                        <div class="metric-card" style="flex: 1;">
                            <div class="metric-value">{len(workout.exercises)}</div>
                            <div class="metric-label">Exercises</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    
                    # =================================================================
                    # WORKOUT EXERCISES - NATIVE STREAMLIT CARDS
                    # Displays exercises with expandable detailed instructions
                    # =================================================================
                    
                    for idx, ex in enumerate(workout.exercises, 1):
                        # Exercise header with name, sets, reps
                        col_name, col_sets, col_reps = st.columns([3, 1, 1])
                        with col_name:
                            st.markdown(f"### {idx}. {ex.name}")
                        with col_sets:
                            st.metric("Sets", ex.sets)
                        with col_reps:
                            st.metric("Reps", ex.reps)
                        
                        # Expandable details section
                        with st.expander("📖 View Instructions & Details"):
                            # Description (show placeholder if missing)
                            if hasattr(ex, 'description') and ex.description:
                                st.markdown(f"**About this exercise:** {ex.description}")
                            else:
                                st.caption("_No description available. Generate a new program to see detailed instructions._")
                            
                            st.markdown("")
                            
                            # Step-by-step instructions (show placeholder if missing)
                            st.markdown("**📋 How to Perform:**")
                            if hasattr(ex, 'steps') and ex.steps:
                                for step_idx, step in enumerate(ex.steps, 1):
                                    st.markdown(f"{step_idx}. {step}")
                            else:
                                st.caption("_Step-by-step instructions will appear here when a new program is generated._")
                            
                            st.markdown("")
                            
                            # Breathing guide (show placeholder if missing)
                            st.markdown("**💨 Breathing:**")
                            if hasattr(ex, 'breathing_guide') and ex.breathing_guide:
                                st.markdown(f"{ex.breathing_guide}")
                            else:
                                st.caption("_Breathing guide will appear here when a new program is generated._")
                            
                            st.markdown("")
                            
                            # Technique cues - ALWAYS show if available
                            if ex.technique_cues:
                                st.markdown("**✅ Key Technique Cues:**")
                                for cue in ex.technique_cues:
                                    st.markdown(f"• {cue}")
                                st.markdown("")
                            
                            # Common mistakes (from research agent)
                            if hasattr(ex, 'common_mistakes') and ex.common_mistakes:
                                st.markdown("**⚠️ Common Mistakes to Avoid:**")
                                for mistake in ex.common_mistakes:
                                    st.markdown(f"• {mistake}")
                                st.markdown("")
                            
                            # Resource links
                            st.markdown("**🔗 External Resources:**")
                            link_cols = st.columns(3)
                            has_links = False
                            
                            if hasattr(ex, 'tutorial_url') and ex.tutorial_url:
                                with link_cols[0]:
                                    st.markdown(f"[📚 Tutorial Article]({ex.tutorial_url})")
                                has_links = True
                            if hasattr(ex, 'video_url') and ex.video_url:
                                with link_cols[1]:
                                    st.markdown(f"[🎬 Video Demo]({ex.video_url})")
                                has_links = True
                            if hasattr(ex, 'gif_url') and ex.gif_url:
                                with link_cols[2]:
                                    st.markdown(f"[🖼️ GIF Animation]({ex.gif_url})")
                                has_links = True
                            
                            if not has_links:
                                st.caption("_No external resources available for this exercise._")
                        
                        # Visual separator between exercises
                        if idx < len(workout.exercises):
                            st.divider()


    # --- TAB 3: SCHEDULE ---
    with tab_schedule:
        st.write("### Weekly Schedule")
        schedule_cols = st.columns(len(program.weekly_schedules[0].workouts))
        for i, col in enumerate(schedule_cols):
            w = program.weekly_schedules[0].workouts[i]
            with col:
                st.markdown(f"**{w.day_name}**")
                st.caption(w.focus)
