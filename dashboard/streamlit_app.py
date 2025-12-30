import streamlit as st
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.profile_agent import ProfileAgent
from agents.market_agent import MarketAgent
from agents.planner_agent import PlanningAgent # Check class name in file
# Assuming class in planner_agent.py is PlanningAgent
from utils.visualization import plot_readiness_radar, plot_market_trends, plot_growth_trajectory
from utils.style_manager import apply_custom_styles

def main():
    st.set_page_config(page_title="PathPilot AI", layout="wide", initial_sidebar_state="expanded")
    apply_custom_styles()

    st.title("PathPilot AI 🚀")
    st.markdown("### Your Autonomous Career Companion")

    # Sidebar: User Profile Input
    with st.sidebar:
        st.header("Profile Setup")
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])
        user_goal = st.text_input("Career Goal", "AI Engineer")
        if st.button("Analyze Profile"):
            st.session_state['analyzing'] = True

    # Main Content Area
    col1, col2 = st.columns([2, 1])

    if 'analyzing' in st.session_state:
        # Placeholder for agent orchestration
        with st.spinner("Agents are collaborating..."):
            # In a real app, agents would run here
            profile_data = {"skills": ["Python", "TensorFlow"], "readiness_score": 65}
            market_data = {"skill_demand": {"Python": 90, "R": 40, "SQL": 80}}
            
        with col1:
            st.subheader("Career Readiness")
            st.plotly_chart(plot_readiness_radar(profile_data), use_container_width=True)
            
            st.subheader("Market Demand Analysis")
            st.plotly_chart(plot_market_trends(market_data), use_container_width=True)

        with col2:
            st.subheader("Action Plan")
            st.markdown("#### Week 1: Foundation")
            st.info("- Master PyTorch basics\n- Complete 'Deep Learning Specialization'")
            
            st.subheader("Projected Growth")
            st.plotly_chart(plot_growth_trajectory(), use_container_width=True)

    else:
        st.info("Please upload your resume and set a goal to start.")

if __name__ == "__main__":
    main()
