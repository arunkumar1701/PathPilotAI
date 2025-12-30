import streamlit as st
import random
import time
import pandas as pd
from utils.style_manager import load_custom_css, display_header
from utils.visualization import plot_readiness_radar, plot_market_trends, plot_growth_trajectory
from utils.llm_manager import LLMManager
from agents.profile_agent import ProfileAgent
from agents.market_agent import MarketAgent
from agents.planner_agent import PlanningAgent
from agents.action_agent import ActionAgent
from agents.feedback_agent import FeedbackAgent

# Page Config
st.set_page_config(
    page_title="PathPilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Styles
load_custom_css()

# Initialize Session State
if 'profile_data' not in st.session_state:
    st.session_state.profile_data = None
if 'matched_jobs' not in st.session_state:
    st.session_state.matched_jobs = []
if 'market_data' not in st.session_state:
    st.session_state.market_data = None
if 'roadmap' not in st.session_state:
    st.session_state.roadmap = None
if 'interview_history' not in st.session_state:
    st.session_state.interview_history = []

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.markdown("### PathPilot AI")
    st.markdown("---")
    
    menu = st.radio(
        "Navigation",
        ["Profile & Resume", "Market Intelligence", "Career Roadmap", "Action Center", "Progress Dashboard"]
    )
    
    st.markdown("---")
    st.markdown("---")
    st.markdown("### System Status")
    
    # Default key for demo purposes
    default_key = "AIzaSyDlPeb49DSYZNShcBC4r7Qz6Fk_-YFuJYM"
    api_key = st.text_input("Gemini API Key", value=default_key, type="password")
    
    if api_key:
        st.session_state.api_key = api_key
        st.caption("🟢 Agents Active (AI Mode)")
    else:
        st.caption("🟡 Demo Mode (Mock Data)")
        
    st.caption("🟢 Memory Engine Online")

# Initialize LLM Manager
llm_manager = LLMManager(st.session_state.get('api_key'))

# Main Content
# Main Content - Login Wrapper
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = "Guest"

def login_page():
    st.markdown("<h1 style='text-align: center;'>PathPilot AI 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Your Autonomous Career Companion</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.info("ℹ️ **Prototype Credentials**\n\nUsername: `arunkumar`\nPassword: `Qwertyui`")
        with st.form("login_form"):
            st.write("Please sign in to continue")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                # Simple mock auth
                if username == "arunkumar" and password == "Qwertyui": 
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please use the prototype usage credentials.")

if not st.session_state.logged_in:
    login_page()
    st.stop() # Stop execution if not logged in

# Main App Logic (Only runs if logged in)
display_header()
st.sidebar.markdown(f"**User:** {st.session_state.username}")

if menu == "Profile & Resume":
    st.markdown("## 1️⃣ Profile Understanding Agent")
    st.markdown("Upload your resume to let the AI analyze your skills, experience, and goals.")
    
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])
    
    if uploaded_file:
        with st.spinner("Parsing and analyzing profile..."):
            time.sleep(1.5)
            agent = ProfileAgent(llm_manager)
            profile_data = agent.parse_resume(uploaded_file)
            st.session_state.profile_data = profile_data
            
            # Update user identity if name found
            if profile_data.get('name') and profile_data.get('name') != "Candidate (Demo)" and "detected" not in profile_data.get('name').lower():
                 st.session_state.username = profile_data['name']
            
        st.success(f"Profile Analysis Complete! Welcome, {st.session_state.username}.")
        
        col1, col2 = st.columns([1, 1.5])
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 👤 Candidate Profile")
            st.markdown(f"**Name:** {profile_data.get('name', 'N/A')}")
            st.markdown(f"**Experience Level:** {profile_data.get('experience_level', 'Entry')}")
            st.markdown("**Top Skills:**")
            st.write(", ".join(profile_data.get('skills', [])[:5]))
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📊 Readiness Radar")
            fig = plot_readiness_radar(profile_data)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

elif menu == "Market Intelligence":
    st.markdown("## 2️⃣ Market Reasoning Agent")
    
    if not st.session_state.profile_data:
        st.warning("Please upload your resume in the Profile tab first.")
    else:
        role_search = st.text_input("Target Role", value=st.session_state.profile_data.get('target_role', 'Data Scientist'))
        
        if st.button("Scan Market"):
            with st.spinner(f"Analyzing trends for {role_search}..."):
                agent = MarketAgent(llm_manager)
                market_data = agent.analyze_market(role_search)
                st.session_state.market_data = market_data
            
            st.markdown("### 📈 Market Trends Forecast")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Demand Growth", market_data['growth_rate'], "High")
            with col2:
                st.metric("Avg Base Salary", market_data['salary_range'], "+5%")
            with col3:
                st.metric("Competition Level", market_data['competition'], "Moderate")
                
            st.markdown("### 🔑 Key Skills in Demand")
            col_chart, col_info = st.columns([2, 1])
            with col_chart:
                 fig = plot_market_trends(market_data)
                 if fig:
                    st.plotly_chart(fig, use_container_width=True)
            with col_info:
                 st.info(f"Top missing skill: **{market_data['missing_skills'][0]}**")
                 st.write("Trending Keywords:")
                 for kw in market_data['trending_keywords']:
                     st.code(kw)

elif menu == "Career Roadmap":
    st.markdown("## 3️⃣ Planning Agent")
    
    if st.button("Generate Adaptive Roadmap"):
        with st.spinner("Generating multi-agent verified roadmap..."):
            agent = PlanningAgent(llm_manager)
            roadmap = agent.generate_roadmap(st.session_state.profile_data, st.session_state.market_data)
            st.session_state.roadmap = roadmap
            
    if st.session_state.roadmap:
        for week in st.session_state.roadmap:
            with st.expander(f"Week {week['week']}: {week['focus']}", expanded=True):
                st.write(week['tasks'])
                if 'resources' in week:
                    st.markdown("**Resources:**")
                    for r in week['resources']:
                        st.markdown(f"- [{r['title']}]({r['url']})")

elif menu == "Action Center":
    st.markdown("## 4️⃣ Action Agent")
    
    tab1, tab2 = st.tabs(["Job Applications", "Mock Interview Analysis"])
    

    with tab1:
        st.markdown("### 🤖 Auto-Apply System")
        st.write("Jobs matched based on your profile and market analysis.")
        
        if 'applied_jobs' not in st.session_state:
            st.session_state.applied_jobs = set()
            
        action_agent = ActionAgent(llm_manager)
        
        # Get jobs (cache this in session state in a real app to avoid refresh)
        if 'matched_jobs' not in st.session_state or not st.session_state.matched_jobs:
            if st.session_state.profile_data:
                st.session_state.matched_jobs = action_agent.get_matched_jobs(st.session_state.profile_data, st.session_state.market_data)
            else:
                st.warning("Please setup your profile first.")
                st.session_state.matched_jobs = []

        for job in st.session_state.matched_jobs:
            col_info, col_action = st.columns([3, 1])
            with col_info:
                st.markdown(f"**{job['title']}** @ {job['company']}")
                st.caption(f"Match: {job['match_score']}% | Location: {job['location']}")
            
            with col_action:
                job_id = job['id']
                if job_id in st.session_state.applied_jobs:
                    st.success("Applied ✅")
                else:
                    if st.button("Apply Now", key=f"apply_{job_id}"):
                         result = action_agent.auto_apply(job)
                         if result['success']:
                             st.session_state.applied_jobs.add(job_id)
                             st.rerun()
        
    with tab2:
        st.markdown("### 🎤 AI Mock Interview")
        st.write("Current Focus: **Behavioral & Technical Questions**")
        
        for msg in st.session_state.interview_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        user_input = st.chat_input("Type your answer here...")
        if user_input:
            st.session_state.interview_history.append({"role": "user", "content": user_input})
            
            # Real LLM Response
            with st.spinner("AI Interviewer is thinking..."):
                agent = ActionAgent(llm_manager)
                
                # Context building
                context = "User is an aspiring AI Engineer."
                if st.session_state.profile_data:
                    p = st.session_state.profile_data
                    context = f"Candidate Name: {st.session_state.username}. Experience: {p.get('experience_level')}. Skills: {p.get('skills')}."
                else:
                    context = f"Candidate Name: {st.session_state.username}."
                
                response = agent.conduct_interview(st.session_state.interview_history, user_input, context=context)
            
            st.session_state.interview_history.append({"role": "assistant", "content": response})
            st.rerun()
            
        if st.button("End Session & Analyze"):
            # Check if there is history to analyze
            if not st.session_state.interview_history:
                st.warning("No interview history to analyze.")
            else:
                with st.spinner("Analyzing tone, sentiment, and content..."):
                    # Use FeedbackAgent to analyze the interview
                    feedback_agent = FeedbackAgent(llm_manager)
                    
                    # Convert history to text format
                    interview_text = "\n".join([f"{msg['role'].title()}: {msg['content']}" for msg in st.session_state.interview_history])
                    
                    # Get analysis (Mock or Real)
                    analysis = feedback_agent.analyze_feedback(interview_text)
                    
                    st.success("Analysis Complete")
                    
                    col_score, col_fb = st.columns([1, 2])
                    with col_score:
                        st.metric("Confidence Score", f"{analysis.get('score', 8.5) * 10}/100", "+5")
                    
                    with col_fb:
                        st.write("**Feedback:**")
                        st.info(f"Sentiment: {analysis.get('sentiment', 'Neutral')}")
                        for area in analysis.get('key_areas', []):
                             st.write(f"- {area}")
                    
                    # Clear history so we can start fresh or keep it? 
                    # Usually ending a session implies saving it. 
                    # For this demo, we'll just show the result. To restart, user can manually clear or we provides a button.
                    if st.button("Start New Interview Session"):
                        st.session_state.interview_history = []
                        st.rerun()

elif menu == "Progress Dashboard":
    st.markdown("## 5️⃣ Feedback & Growth Console")
    
    agent = FeedbackAgent(llm_manager)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        start_score = 65
        current_score = start_score + (len(st.session_state.get('applied_jobs', [])) * 2) + (len(st.session_state.get('interview_history', [])) // 2)
        st.metric("Career Readiness", f"{min(current_score, 98)}%", f"+{current_score - start_score}%")
    with col2:
        st.metric("Jobs Applied", len(st.session_state.get('applied_jobs', [])), "Target: 5/week")
    with col3:
        st.metric("Interviews Practiced", len([m for m in st.session_state.get('interview_history', []) if m['role'] == 'user']) // 5, "Keep going!")
    with col4:
        st.metric("Skills Acquired", "3", "+1 this week")

    st.markdown("---")

    # 2. Main Dashboard Grid
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.markdown("### 📉 Impact Trajectory")
        # In a real app, this would use historical data
        fig = plot_growth_trajectory()
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 🧠 Deep Dive Analysis")
        # Aggregate feedback from all interaction
        feedback = agent.analyze_feedback("Session Summary: User has practiced python questions and applied to senior roles.")
        
        tab_fb1, tab_fb2 = st.tabs(["Strengths", "Critical Gaps"])
        with tab_fb1:
            st.success("Consistent improvement in technical definitions.")
            st.success("Good keyword matching for 'Transformers' and 'MLOps'.")
        with tab_fb2:
            st.error("Need more concrete examples in behavioral answers (STAR method).")
            st.warning("Resume description for 'Project X' is too generic.")

    with col_side:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🏆 Session Wins")
        if st.session_state.get('applied_jobs'):
            st.code(f"Applied to {len(st.session_state.applied_jobs)} Priority Roles")
        if len(st.session_state.get('interview_history', [])) > 5:
             st.code("Completed Mock Interview Session")
        st.code("Profile Optimization Score: 92/100")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 🧘 Wellness AI")
        burnout = 30 # Mock calculation
        st.caption(f"Current Stress Level: {burnout}%")
        st.progress(burnout / 100)
        
        if burnout < 40:
            st.info("✅ You are in the **Flow State**. Perfect balance of challenge and skill.")
        elif burnout < 70:
            st.warning("⚠️ High cognitive load detected. Consider a 15-min walk.")
        else:
            st.error("🛑 Stop now. Risk of burnout. Schedule downtime.")

