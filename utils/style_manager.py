import streamlit as st

def load_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        /* General App Styling */
        .stApp {
            background-color: #0d1117;
            color: #e6edf3;
            font-family: 'Outfit', sans-serif;
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #010409;
            border-right: 1px solid #30363d;
        }
        
        /* Headers */
        h1, h2, h3 {
            background: linear-gradient(135deg, #2F80ED 0%, #B2FFDA 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        
        /* Cards/Containers */
        .glass-card {
            background: rgba(22, 27, 34, 0.7);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(48, 54, 61, 0.5);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            margin-bottom: 20px;
        }
        
        .glass-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(88, 166, 255, 0.3);
        }

        /* Metrics */
        [data-testid="stMetricValue"] {
            font-size: 2.8rem !important;
            font-weight: 700;
            color: #58a6ff;
            text-shadow: 0 0 20px rgba(88, 166, 255, 0.3);
        }
        
        [data-testid="stMetricLabel"] {
            color: #8b949e;
            font-size: 1rem;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(90deg, #238636, #2ea043);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 14px rgba(35, 134, 54, 0.4);
        }
        .stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(35, 134, 54, 0.6);
            background: linear-gradient(90deg, #2ea043, #3fb950);
        }
        
        /* Inputs */
        .stTextInput > div > div > input {
            background-color: #0d1117;
            color: #e6edf3;
            border: 1px solid #30363d;
            border-radius: 8px;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #58a6ff;
            box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.3);
        }
        
        /* Progress Bars */
        .stProgress > div > div > div > div {
            background-image: linear-gradient(90deg, #2F80ED, #B2FFDA);
            border-radius: 10px;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
            background-color: #0d1117;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 4px;
            color: #8b949e;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: rgba(48, 54, 61, 0.4);
            color: #58a6ff;
        }
        
        </style>
    """, unsafe_allow_html=True)

def display_header():
    st.markdown("""
        <div style='text-align: center; padding: 3rem 0; animation: fadeIn 1s ease-in;'>
            <h1 style='font-size: 4rem; margin-bottom: 0px;'>🚀 PathPilot AI</h1>
            <p style='font-size: 1.4rem; color: #8b949e; margin-top: 10px; letter-spacing: 1px;'>
                Your <span style='color: #58a6ff;'>Agentic</span> Career Development Assistant
            </p>
        </div>
    """, unsafe_allow_html=True)
