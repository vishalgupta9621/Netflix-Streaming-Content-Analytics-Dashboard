import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import logging
import io
import os
from datetime import datetime

# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')

log_filename = f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(io.StringIO()) # Keep stream handler for UI display
    ]
)

# Capture log stream for UI display
log_capture_string = io.StringIO()
ch = logging.StreamHandler(log_capture_string)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logging.getLogger().addHandler(ch)

logging.info("Application started")

warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="Netflix Content Analysis",
    layout="wide",
    page_icon="🎬",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS matching Walmart style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #141414 0%, #000000 50%, #1a0000 100%);
        background-attachment: fixed;
    }
    .block-container {
        background: rgba(20, 20, 20, 0.95);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(229, 9, 20, 0.3);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(229, 9, 20, 0.2);
    }
    h1 {
        background: linear-gradient(135deg, #E50914 0%, #ff6b6b 50%, #ff0000 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeInDown 1s ease-in-out;
        letter-spacing: -1px;
    }
    h2 { 
        color: #f3f4f6 !important; 
        border-bottom: 3px solid #E50914; 
        padding-bottom: 0.5rem; 
        margin-top: 2rem; 
        font-weight: 700 !important;
        text-shadow: 0 2px 10px rgba(229, 9, 20, 0.3);
    }
    h3 { 
        color: #e5e7eb !important; 
        margin-top: 1.5rem; 
        font-weight: 600 !important; 
    }
    p, li, span, div { color: #cbd5e1; }
    
    [data-testid="stMetricValue"] {
        background: linear-gradient(135deg, #E50914 0%, #ff6b6b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: pulse 2s ease-in-out infinite;
    }
    [data-testid="stMetricLabel"] { 
        color: #9ca3af !important; 
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.75rem !important;
    }
    
    .stTabs [data-baseweb="tab-list"] { 
        gap: 12px; 
        background-color: rgba(20, 20, 20, 0.5);
        padding: 0.5rem;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, rgba(229, 9, 20, 0.1) 0%, rgba(255, 107, 107, 0.1) 100%);
        color: #E50914; 
        border-radius: 10px; 
        padding: 12px 24px; 
        font-weight: 600; 
        transition: all 0.3s ease; 
        border: 1px solid rgba(229, 9, 20, 0.3);
    }
    .stTabs [data-baseweb="tab"]:hover { 
        background: linear-gradient(135deg, rgba(229, 9, 20, 0.2) 0%, rgba(255, 107, 107, 0.2) 100%);
        transform: translateY(-2px); 
        box-shadow: 0 4px 12px rgba(229, 9, 20, 0.4);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #E50914 0%, #ff6b6b 100%) !important; 
        color: white !important; 
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.6);
        transform: translateY(-2px);
    }
    
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #1a0000 0%, #000000 100%); 
        border-right: 1px solid rgba(229, 9, 20, 0.3);
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 { 
        color: white !important; 
        -webkit-text-fill-color: white !important; 
    }
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] li, 
    [data-testid="stSidebar"] span { 
        color: #cbd5e1 !important; 
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #E50914 0%, #ff6b6b 100%); 
        color: white; 
        border-radius: 12px; 
        padding: 0.75rem 2rem; 
        font-weight: 600; 
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.4); 
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover { 
        transform: translateY(-3px); 
        box-shadow: 0 8px 25px rgba(229, 9, 20, 0.6); 
        color: white; 
    }
    
    @keyframes fadeInDown { 
        from { opacity: 0; transform: translateY(-30px); } 
        to { opacity: 1; transform: translateY(0); } 
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    .card {
        padding: 1rem; 
        border-radius: 16px; 
        text-align: center; 
        color: white; 
        box-shadow: 0 8px 32px rgba(0,0,0,0.4); 
        transition: all 0.4s ease; 
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    .card:hover::before {
        left: 100%;
    }
    .card:hover { 
        transform: translateY(-8px) scale(1.02); 
        box-shadow: 0 12px 40px rgba(229, 9, 20, 0.4);
    }
    
    .metric-container {
        background: rgba(20, 20, 20, 0.7);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(229, 9, 20, 0.2);
        transition: all 0.3s ease;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(229, 9, 20, 0.3);
        border-color: rgba(229, 9, 20, 0.5);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    .metric-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        background: rgba(229, 9, 20, 0.1);
        width: 50px;
        height: 50px;
        line-height: 50px;
        border-radius: 50%;
        margin: 0 auto 1rem auto;
    }
</style>
""", unsafe_allow_html=True)

# Header with animation
st.markdown("""
<div style='position: fixed; top: 3.5rem; right: 1.5rem; z-index: 9999;'>
    <div style='background: linear-gradient(135deg, #E50914 0%, #ff6b6b 100%); 
                border-radius: 20px; padding: 0.6rem 1.2rem; 
                box-shadow: 0 4px 20px rgba(229, 9, 20, 0.5);
                animation: fadeInDown 1s ease-in-out;'>
        <span style='color: white; font-weight: 700; font-size: 0.9rem; letter-spacing: 1.5px;'>
            ✨ By RATNESH SINGH
        </span>
    </div>
</div>
<div style='text-align: center; padding: 2rem 0 1rem 0;'>
    <h1 style='font-size: 4rem; margin-bottom: 0;'>🎬 Netflix Content Strategy Analysis</h1>
    <p style='font-size: 1.3rem; background: linear-gradient(135deg, #E50914 0%, #ff6b6b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700; margin-top: 0.5rem; letter-spacing: 1px;'>
        🎯 Data-Driven Insights for Content Growth & Strategy
    </p>
</div>
""", unsafe_allow_html=True)

# --- Data Loading and Preprocessing ---
@st.cache_data
def load_data():
    logging.info("Attempting to load data from netflix.csv")
    try:
        df = pd.read_csv("netflix.csv")
        logging.info(f"Data loaded successfully. Shape: {df.shape}")
    except FileNotFoundError:
        logging.error("File 'netflix.csv' not found.")
        st.error("❌ File 'netflix.csv' not found in the current directory.")
        return None

    # Handling missing values
    logging.info("Preprocessing: Handling missing values")
    df["director"].fillna("Unknown", inplace=True)
    df["cast"].fillna("Unknown", inplace=True)
    df["country"].fillna("Unknown", inplace=True)
    
    # Date processing
    logging.info("Preprocessing: Parsing dates")
    df["date_added"] = pd.to_datetime(df["date_added"], errors='coerce')
    df["year_added"] = df["date_added"].dt.year
    df["month_added"] = df["date_added"].dt.month_name()
    
    # Duration processing
    logging.info("Preprocessing: Extracting durations")
    df["Movie_duration"] = df.loc[df["type"] == "Movie", "duration"].astype(str).str.split(" ").str[0].astype(float)
    df["Series_duration"] = df.loc[df["type"] == "TV Show", "duration"].astype(str).str.split(" ").str[0].astype(float)
    
    # Rating categorization
    logging.info("Preprocessing: Categorizing ratings")
    rating_map = {
        "TV-MA": "Adults", "R": "Adults", "NC-17": "Adults", "UR": "Adults", "NR": "Adults",
        "TV-14": "Teens", "PG-13": "Teens",
        "TV-PG": "Older Kids", "TV-Y7": "Older Kids", "TV-Y7-FV": "Older Kids", "PG": "Older Kids",
        "TV-Y": "Kids", "TV-G": "Kids", "G": "Kids"
    }
    df["Content_For"] = df["rating"].map(rating_map)
    
    return df

@st.cache_data
def load_unnested_data(df):
    logging.info("Preprocessing: Unnesting multi-value columns")
    def unnest_col(df, col, new_col_name):
        return df[col].astype(str).str.split(", ").explode().reset_index().rename(columns={col: new_col_name, "index": "original_index"})

    actors = unnest_col(df, "cast", "actor")
    directors = unnest_col(df, "director", "director_unnested")
    countries = unnest_col(df, "country", "country_unnested")
    genres = unnest_col(df, "listed_in", "genre")
    
    return actors, directors, countries, genres

df = load_data()

if df is not None:
    actors_df, directors_df, countries_df, genres_df = load_unnested_data(df)

    # Enhanced Feature Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class='card' style='background: linear-gradient(135deg, #E50914 0%, #b20710 100%);'>
            <div style='font-size: 2rem; margin-bottom: 0.25rem;'>📊</div>
            <h3 style='color: white !important; margin: 0.25rem 0; font-size: 1.1rem;'>Data</h3>
            <p style='margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.8);'>Content Library</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='card' style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);'>
            <div style='font-size: 2rem; margin-bottom: 0.25rem;'>🔍</div>
            <h3 style='color: white !important; margin: 0.25rem 0; font-size: 1.1rem;'>EDA</h3>
            <p style='margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.8);'>Visual Analysis</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='card' style='background: linear-gradient(135deg, #c92a2a 0%, #a61e4d 100%);'>
            <div style='font-size: 2rem; margin-bottom: 0.25rem;'>📈</div>
            <h3 style='color: white !important; margin: 0.25rem 0; font-size: 1.1rem;'>Trends</h3>
            <p style='margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.8);'>Growth Patterns</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class='card' style='background: linear-gradient(135deg, #862e9c 0%, #5f3dc4 100%);'>
            <div style='font-size: 2rem; margin-bottom: 0.25rem;'>💡</div>
            <h3 style='color: white !important; margin: 0.25rem 0; font-size: 1.1rem;'>Insights</h3>
            <p style='margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.8);'>Recommendations</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Enhanced Sidebar
    with st.sidebar:
        st.markdown("## 📑 Navigation")
        st.markdown("---")
        st.markdown("""
        <div style='background: rgba(229, 9, 20, 0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(229, 9, 20, 0.3);'>
            <h3 style='color: #E50914 !important; margin-top: 0;'>📊 Project Overview</h3>
            <p><strong>Company:</strong> Netflix Inc.</p>
            <p><strong>Goal:</strong> Analyze content strategy</p>
            <p><strong>Focus:</strong> Growth opportunities</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: rgba(255, 107, 107, 0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(255, 107, 107, 0.3);'>
            <h3 style='color: #ff6b6b !important; margin-top: 0;'>📈 Key Metrics</h3>
            <p>📺 <strong>Total Titles:</strong> {len(df):,}</p>
            <p>🌍 <strong>Countries:</strong> {df['country'].nunique()}</p>
            <p>🎭 <strong>Genres:</strong> {df['listed_in'].nunique()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: rgba(201, 42, 42, 0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(201, 42, 42, 0.3);'>
            <h3 style='color: #c92a2a !important; margin-top: 0;'>🔍 Analysis Steps</h3>
            <ul style='margin: 0; padding-left: 1.2rem;'>
                <li>Data Loading & Preprocessing</li>
                <li>Content Distribution Analysis</li>
                <li>Trend & Pattern Identification</li>
                <li>Genre & Regional Insights</li>
                <li>Strategic Recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Main Tabs
    tabs = st.tabs([
        "📊 Problem Statement",
        "🔍 Interactive EDA", 
        "🎥 Content Analysis",
        "⭐ Rating Analysis",
        "💡 Recommendations",
        "📑 Complete Analysis",
        "📝 App Logs"
    ])

    # TAB 1: Problem Statement
    with tabs[0]:
        logging.info("Rendering Tab: Problem Statement")
        st.header("📊 Netflix Business Case")
        
        # Enhanced Metrics
        m1, m2, m3, m4 = st.columns(4)
        
        with m1:
            st.markdown(f"""
            <div class="metric-container" style='background: linear-gradient(135deg, rgba(229, 9, 20, 0.15), rgba(229, 9, 20, 0.05));'>
                <div class="metric-icon" style="color: #E50914;">📊</div>
                <div class="metric-value">{len(df):,}</div>
                <div class="metric-label">Total Titles</div>
                <div style="font-size: 0.85rem; color: #E50914; margin-top: 0.5rem; font-weight: 500;">Content Library</div>
            </div>
            """, unsafe_allow_html=True)
            
        with m2:
            st.markdown(f"""
            <div class="metric-container" style='background: linear-gradient(135deg, rgba(255, 107, 107, 0.15), rgba(255, 107, 107, 0.05));'>
                <div class="metric-icon" style="color: #ff6b6b;">🌍</div>
                <div class="metric-value">{df['country'].nunique():,}</div>
                <div class="metric-label">Countries</div>
                <div style="font-size: 0.85rem; color: #ff6b6b; margin-top: 0.5rem; font-weight: 500;">Global Reach</div>
            </div>
            """, unsafe_allow_html=True)
            
        with m3:
            st.markdown(f"""
            <div class="metric-container" style='background: linear-gradient(135deg, rgba(201, 42, 42, 0.15), rgba(201, 42, 42, 0.05));'>
                <div class="metric-icon" style="color: #c92a2a;">🎭</div>
                <div class="metric-value">{df['type'].value_counts()['Movie']:,}</div>
                <div class="metric-label">Movies</div>
                <div style="font-size: 0.85rem; color: #c92a2a; margin-top: 0.5rem; font-weight: 500;">Film Collection</div>
            </div>
            """, unsafe_allow_html=True)
            
        with m4:
            st.markdown(f"""
            <div class="metric-container" style='background: linear-gradient(135deg, rgba(134, 46, 156, 0.15), rgba(134, 46, 156, 0.05));'>
                <div class="metric-icon" style="color: #862e9c;">📺</div>
                <div class="metric-value">{df['type'].value_counts()['TV Show']:,}</div>
                <div class="metric-label">TV Shows</div>
                <div style="font-size: 0.85rem; color: #862e9c; margin-top: 0.5rem; font-weight: 500;">Series Collection</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Business Context
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(229, 9, 20, 0.1), rgba(255, 107, 107, 0.1)); 
                    padding: 1.5rem; border-radius: 15px; border-left: 5px solid #E50914; margin-bottom: 2rem;'>
            <h3 style='color: #E50914; margin-top: 0; display: flex; align-items: center; gap: 10px;'>
                <span style='font-size: 1.8rem;'>🎯</span> Business Objective
            </h3>
            <p style='color: #cbd5e1; line-height: 1.8; font-size: 1.05rem; margin: 0;'>
                Netflix aims to understand content distribution patterns and identify strategic opportunities for growth. 
                The analysis focuses on <strong style='color: #ff6b6b;'>content type distribution, regional production trends, 
                genre preferences, and audience targeting</strong> to inform data-driven decisions for content acquisition, 
                production, and marketing strategies.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns([1.5, 1])
        
        with c1:
            st.markdown("""
            <div style='background: linear-gradient(145deg, rgba(30, 20, 20, 0.8), rgba(15, 10, 10, 0.9)); 
                        padding: 2rem; border-radius: 20px; border: 1px solid rgba(229, 9, 20, 0.3); height: 100%;'>
                <h3 style='color: #E50914 !important; margin-top: 0; display: flex; align-items: center; gap: 10px;'>
                    <span style='font-size: 2rem;'>🎬</span> About Netflix
                </h3>
                <p style='color: #cbd5e1; line-height: 1.8; font-size: 1.05rem;'>
                    <strong style='color: #E50914;'>Netflix Inc.</strong> is the world's leading streaming entertainment service 
                    with over 230 million paid memberships in more than 190 countries. Founded in 1997, Netflix has revolutionized 
                    how people watch TV shows and movies, offering a vast library of content across various genres and languages.
                </p>
                <div style='background: rgba(229, 9, 20, 0.1); padding: 1.2rem; border-radius: 12px; margin-top: 1.5rem;'>
                    <p style='color: #ff6b6b; margin: 0; font-size: 0.95rem; line-height: 1.6;'>
                        <strong>📊 Data Context:</strong> This dataset contains information about movies and TV shows available 
                        on Netflix as of 2021, including details about directors, cast, countries, release years, ratings, 
                        and genres.
                    </p>
                </div>
                <div style='margin-top: 1rem; padding: 1rem; background: rgba(229, 9, 20, 0.05); border-radius: 10px;'>
                    <p style='color: #94a3b8; margin: 0; font-size: 0.9rem;'>
                        <strong>🌍 Global Presence:</strong> 190+ countries | <strong>👥</strong> 230M+ subscribers
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown("""
            <div style='background: linear-gradient(145deg, rgba(30, 20, 20, 0.8), rgba(15, 10, 10, 0.9)); 
                        padding: 2rem; border-radius: 20px; border: 1px solid rgba(255, 107, 107, 0.3); height: 100%;'>
                <h3 style='color: #ff6b6b !important; margin-top: 0; display: flex; align-items: center; gap: 10px;'>
                    <span style='font-size: 2rem;'>❓</span> Research Questions
                </h3>
                <div style='background: rgba(255, 107, 107, 0.1); padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem;'>
                    <p style='color: #fbbf24; line-height: 1.6; font-size: 1.05rem; margin: 0; font-weight: 600;'>
                        "What content strategies should Netflix pursue for sustainable growth?"
                    </p>
                </div>
                <h4 style='color: #ff6b6b; font-size: 1rem; margin-top: 1.5rem;'>🔍 Analysis Scope:</h4>
                <ul style='color: #cbd5e1; margin-bottom: 0; line-height: 1.8;'>
                    <li style='margin-bottom: 0.7rem;'>📊 Content type distribution analysis</li>
                    <li style='margin-bottom: 0.7rem;'>🌍 Regional production patterns</li>
                    <li style='margin-bottom: 0.7rem;'>🎭 Genre popularity trends</li>
                    <li style='margin-bottom: 0.7rem;'>👥 Target audience segmentation</li>
                    <li style='margin-bottom: 0.7rem;'>📈 Growth trend analysis</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Data Dictionary
        st.markdown("""
        <div style='margin-bottom: 1rem;'>
            <h3 style='color: #E50914; display: flex; align-items: center; gap: 10px;'>
                <span style='font-size: 1.5rem;'>📚</span> Data Dictionary
            </h3>
            <p style='color: #94a3b8; font-size: 0.95rem;'>
                Understanding the dataset structure and feature definitions
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        data_dict = pd.DataFrame({
            'Column': ['show_id', 'type', 'title', 'director', 'cast', 'country', 'date_added', 
                       'release_year', 'rating', 'duration', 'listed_in', 'description'],
            'Data Type': ['Text', 'Categorical', 'Text', 'Text', 'Text', 'Text', 'Date', 
                          'Numerical', 'Categorical', 'Text', 'Text', 'Text'],
            'Description': [
                'Unique identifier for each title',
                'Content type: Movie or TV Show',
                'Title of the content',
                'Director(s) of the content',
                'Main cast members',
                'Country/countries of production',
                'Date when added to Netflix',
                'Original release year',
                'Content rating (TV-MA, PG-13, etc.)',
                'Duration in minutes or seasons',
                'Genre categories',
                'Brief description of the content'
            ]
        })
        
        st.dataframe(data_dict, use_container_width=True, hide_index=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Dataset Preview
        st.markdown("""
        <div style='margin-bottom: 1rem;'>
            <h3 style='color: #E50914; display: flex; align-items: center; gap: 10px;'>
                <span style='font-size: 1.5rem;'>👀</span> Dataset Preview
            </h3>
            <p style='color: #94a3b8; font-size: 0.95rem;'>
                First 10 rows of the Netflix content data
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.dataframe(df.head(10), use_container_width=True)
        
        # Key Statistics
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style='background: rgba(229, 9, 20, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(229, 9, 20, 0.3);'>
                <h4 style='color: #E50914; margin-top: 0;'>📊 Dataset Size</h4>
                <p style='color: #cbd5e1; margin: 0;'>
                    <strong>Rows:</strong> {df.shape[0]:,}<br>
                    <strong>Columns:</strong> {df.shape[1]}<br>
                    <strong>Memory:</strong> {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            missing_count = df.isnull().sum().sum()
            st.markdown(f"""
            <div style='background: rgba(255, 107, 107, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255, 107, 107, 0.3);'>
                <h4 style='color: #ff6b6b; margin-top: 0;'>🎯 Data Quality</h4>
                <p style='color: #cbd5e1; margin: 0;'>
                    <strong>Missing Values:</strong> {missing_count}<br>
                    <strong>Duplicates:</strong> {df.duplicated().sum()}<br>
                    <strong>Completeness:</strong> {((1 - missing_count/(df.shape[0]*df.shape[1]))*100):.1f}%
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='background: rgba(201, 42, 42, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(201, 42, 42, 0.3);'>
                <h4 style='color: #c92a2a; margin-top: 0;'>📅 Time Range</h4>
                <p style='color: #cbd5e1; margin: 0;'>
                    <strong>Earliest:</strong> {df['release_year'].min()}<br>
                    <strong>Latest:</strong> {df['release_year'].max()}<br>
                    <strong>Span:</strong> {df['release_year'].max() - df['release_year'].min()} years
                </p>
            </div>
            """, unsafe_allow_html=True)

    # TAB 2: Interactive EDA
    with tabs[1]:
        logging.info("Rendering Tab: Interactive EDA")
        st.header("🔍 Interactive Exploratory Data Analysis")
        
        viz_tabs = st.tabs(["📊 Overview", "🎭 Content Types", "🌍 Geographic", "📅 Temporal"])
        
        with viz_tabs[0]:
            st.subheader("📊 Dataset Overview")
            st.markdown("""
            <div style='background: rgba(229, 9, 20, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
                <p style='color: #cbd5e1; margin: 0;'>
                    📊 Comprehensive statistical overview of the Netflix content library, including distributions, 
                    central tendencies, and data quality metrics.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick Stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Total Records", f"{len(df):,}")
            with col2:
                st.metric("📋 Features", f"{df.shape[1]}")
            with col3:
                missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100)
                st.metric("✅ Completeness", f"{100-missing_pct:.1f}%")
            with col4:
                st.metric("💾 Memory", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📈 Numerical Features Summary**")
                numeric_summary = df[['release_year']].describe().T
                st.dataframe(numeric_summary, use_container_width=True)
                
            with col2:
                st.markdown("**📋 Categorical Features**")
                cat_summary = []
                for col in ['type', 'rating', 'country']:
                    value_counts = df[col].value_counts()
                    cat_summary.append({
                        'Feature': col,
                        'Unique': df[col].nunique(),
                        'Most Common': str(value_counts.index[0])[:20],
                        'Frequency': value_counts.values[0]
                    })
                st.dataframe(pd.DataFrame(cat_summary), use_container_width=True, hide_index=True)
        
        with viz_tabs[1]:
            st.subheader("🎭 Content Type Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📺 Movies vs TV Shows**")
                type_counts = df['type'].value_counts().reset_index()
                type_counts.columns = ['Type', 'Count']
                type_counts['Percentage'] = (type_counts['Count'] / type_counts['Count'].sum() * 100).round(2)
                
                fig = px.pie(type_counts, values='Count', names='Type', 
                            color='Type', color_discrete_map={'Movie':'#E50914', 'TV Show':'#564d4d'},
                            title='Content Type Distribution',
                            hole=0.4)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#cbd5e1')
                )
                st.plotly_chart(fig, use_container_width=True)
                
                movie_pct = type_counts[type_counts['Type']=='Movie']['Percentage'].values[0]
                st.success(f"✅ **Key Finding:** Movies dominate with {movie_pct}% of total content")
                
            with col2:
                st.markdown("**📊 Content Type Statistics**")
                for _, row in type_counts.iterrows():
                    st.metric(row['Type'], f"{row['Count']:,}", f"{row['Percentage']:.1f}%")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Duration comparison
                st.markdown("**⏱️ Average Duration**")
                avg_movie_dur = df[df['type']=='Movie']['Movie_duration'].mean()
                avg_series_dur = df[df['type']=='TV Show']['Series_duration'].mean()
                
                st.metric("Movies", f"{avg_movie_dur:.0f} min")
                st.metric("TV Shows", f"{avg_series_dur:.1f} seasons")
        
        with viz_tabs[2]:
            st.subheader("🌍 Geographic Distribution")
            
            st.markdown("**🗺️ Top Producing Countries**")
            clean_countries = countries_df[countries_df['country_unnested'] != 'Unknown']
            top_countries = clean_countries['country_unnested'].value_counts().head(15).reset_index()
            top_countries.columns = ['Country', 'Count']
            
            fig = px.bar(top_countries, x='Country', y='Count',
                        color='Count', color_continuous_scale='Reds',
                        title='Top 15 Countries by Content Volume')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)
            
            top_country = top_countries.iloc[0]
            st.info(f"💡 **Insight:** {top_country['Country']} leads with {top_country['Count']:,} titles")
            
            st.markdown("---")
            
            # Country vs Type
            st.markdown("**🌍 Content Type by Top Countries**")
            top_5_countries = top_countries.head(5)['Country'].tolist()
            country_type_data = []
            
            for country in top_5_countries:
                country_df = df[df['country'].str.contains(country, na=False)]
                type_counts = country_df['type'].value_counts()
                for content_type, count in type_counts.items():
                    country_type_data.append({
                        'Country': country,
                        'Type': content_type,
                        'Count': count
                    })
            
            country_type_df = pd.DataFrame(country_type_data)
            fig = px.bar(country_type_df, x='Country', y='Count', color='Type',
                        color_discrete_map={'Movie':'#E50914', 'TV Show':'#564d4d'},
                        title='Content Type Distribution by Top 5 Countries',
                        barmode='group')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with viz_tabs[3]:
            st.subheader("📅 Temporal Analysis")
            
            st.markdown("**📈 Content Added Over Years**")
            df_year = df.groupby(['year_added', 'type']).size().reset_index(name='Count')
            df_year = df_year.dropna()
            
            fig = px.area(df_year, x='year_added', y='Count', color='type',
                        color_discrete_map={'Movie':'#E50914', 'TV Show':'#ffffff'},
                        title='Content Addition Trend Over Time')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1')
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Peak year
            year_totals = df_year.groupby('year_added')['Count'].sum().reset_index()
            peak_year = year_totals.loc[year_totals['Count'].idxmax()]
            st.success(f"✅ **Key Finding:** Peak content addition was in {int(peak_year['year_added'])} with {peak_year['Count']} titles")
            
            st.markdown("---")
            
            # Monthly distribution
            st.markdown("**📆 Content Added by Month**")
            month_counts = df['month_added'].value_counts().reset_index()
            month_counts.columns = ['Month', 'Count']
            
            # Order months correctly
            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                          'July', 'August', 'September', 'October', 'November', 'December']
            month_counts['Month'] = pd.Categorical(month_counts['Month'], categories=month_order, ordered=True)
            month_counts = month_counts.sort_values('Month')
            
            fig = px.bar(month_counts, x='Month', y='Count',
                        color='Count', color_continuous_scale='Reds',
                        title='Content Addition by Month')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)

    # TAB 3: Content Analysis
    with tabs[2]:
        logging.info("Rendering Tab: Content Analysis")
        st.header("🎥 Comprehensive Content Analysis")
        
        st.markdown("""
        <div style='background: rgba(229, 9, 20, 0.1); padding: 1.5rem; border-radius: 10px; border-left: 4px solid #E50914; margin-bottom: 1.5rem;'>
            <h4 style='color: #E50914; margin-top: 0;'>🎬 Deep Dive into Content Library</h4>
            <p style='color: #cbd5e1; margin: 0;'>
                This section analyzes Netflix's content library across multiple dimensions including genres, 
                production countries, release patterns, and content characteristics to identify strategic opportunities.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Genre Analysis
        st.markdown("### 🎭 Genre Analysis")
        st.markdown("*Understanding content categorization and genre preferences*")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**📊 Top 15 Genres**")
            top_genres = genres_df['genre'].value_counts().head(15).reset_index()
            top_genres.columns = ['Genre', 'Count']
            
            fig = px.bar(top_genres, x='Count', y='Genre', orientation='h',
                        color='Count', color_continuous_scale='Reds',
                        title='Most Popular Genres on Netflix')
            fig.update_layout(
                yaxis={'categoryorder':'total ascending'},
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1')
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("**🏆 Top 5 Genres**")
            for idx, row in top_genres.head(5).iterrows():
                pct = (row['Count'] / len(genres_df) * 100)
                st.metric(
                    row['Genre'][:20],
                    f"{row['Count']:,}",
                    f"{pct:.1f}%"
                )
        
        st.markdown("---")
        
        # Duration Analysis
        st.markdown("### ⏱️ Duration Analysis")
        st.markdown("*Analyzing content length patterns*")
        
        tab1, tab2 = st.tabs(["Movies", "TV Shows"])
        
        with tab1:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = px.histogram(df[df['type']=='Movie'].dropna(subset=['Movie_duration']), 
                                  x='Movie_duration', 
                                  nbins=30, 
                                  color_discrete_sequence=['#E50914'],
                                  title='Distribution of Movie Duration (Minutes)')
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#cbd5e1')
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("**📊 Movie Duration Stats**")
                movie_dur = df[df['type']=='Movie']['Movie_duration'].dropna()
                st.metric("Average", f"{movie_dur.mean():.0f} min")
                st.metric("Median", f"{movie_dur.median():.0f} min")
                st.metric("Most Common", f"{movie_dur.mode()[0]:.0f} min")
                st.metric("Range", f"{movie_dur.min():.0f} - {movie_dur.max():.0f} min")
        
        with tab2:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = px.histogram(df[df['type']=='TV Show'].dropna(subset=['Series_duration']), 
                                  x='Series_duration', 
                                  nbins=15, 
                                  color_discrete_sequence=['#ffffff'],
                                  title='Distribution of TV Show Duration (Seasons)')
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#cbd5e1')
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("**📊 TV Show Duration Stats**")
                series_dur = df[df['type']=='TV Show']['Series_duration'].dropna()
                st.metric("Average", f"{series_dur.mean():.1f} seasons")
                st.metric("Median", f"{series_dur.median():.0f} seasons")
                st.metric("Most Common", f"{series_dur.mode()[0]:.0f} season(s)")
                st.metric("Max", f"{series_dur.max():.0f} seasons")
        
        st.markdown("---")
        
        # Release Year Analysis
        st.markdown("### 📅 Release Year Patterns")
        st.markdown("*Understanding content age and production trends*")
        
        # Last 30 years
        recent_years = df[df['release_year'] >= (df['release_year'].max() - 30)]
        year_counts = recent_years.groupby(['release_year', 'type']).size().reset_index(name='Count')
        
        fig = px.bar(year_counts, x='release_year', y='Count', color='type',
                    color_discrete_map={'Movie':'#E50914', 'TV Show':'#ffffff'},
                    title='Content Released in Last 30 Years',
                    barmode='stack')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent decline insight
        recent_5_years = df[df['release_year'] >= (df['release_year'].max() - 5)]
        recent_count = len(recent_5_years)
        total_count = len(df)
        recent_pct = (recent_count / total_count * 100)
        st.info(f"💡 **Insight:** {recent_pct:.1f}% of Netflix's library consists of content released in the last 5 years ({recent_count:,} titles)")

    # TAB 4: Rating Analysis
    with tabs[3]:
        logging.info("Rendering Tab: Rating Analysis")
        st.header("⭐ Content Rating & Audience Analysis")
        
        st.markdown("""
        <div style='background: rgba(255, 107, 107, 0.1); padding: 1.5rem; border-radius: 10px; border-left: 4px solid #ff6b6b; margin-bottom: 1.5rem;'>
            <h4 style='color: #ff6b6b; margin-top: 0;'>👥 Understanding Target Audiences</h4>
            <p style='color: #cbd5e1; margin: 0;'>
                Analyzing content ratings and target demographics to understand Netflix's audience strategy 
                and identify opportunities for content diversification.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Content Distribution by Target Audience")
            audience_counts = df['Content_For'].value_counts().reset_index()
            audience_counts.columns = ['Audience', 'Count']
            audience_counts['Percentage'] = (audience_counts['Count'] / audience_counts['Count'].sum() * 100).round(2)
            
            fig = px.pie(audience_counts, values='Count', names='Audience',
                        color_discrete_sequence=['#E50914', '#ff6b6b', '#c92a2a', '#862e9c'],
                        title='Target Audience Distribution',
                        hole=0.4)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1')
            )
            st.plotly_chart(fig, use_container_width=True)
            
            top_audience = audience_counts.iloc[0]
            st.success(f"✅ **Key Finding:** {top_audience['Audience']} content dominates with {top_audience['Percentage']:.1f}%")
            
        with col2:
            st.subheader("Detailed Rating Distribution")
            rating_counts = df['rating'].value_counts().head(10).reset_index()
            rating_counts.columns = ['Rating', 'Count']
            
            fig = px.bar(rating_counts, x='Rating', y='Count',
                        color='Count', color_continuous_scale='Reds',
                        title='Top 10 Content Ratings')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1')
            )
            st.plotly_chart(fig, use_container_width=True)
            
            top_rating = rating_counts.iloc[0]
            st.info(f"💡 **Insight:** {top_rating['Rating']} is the most common rating with {top_rating['Count']:,} titles")
        
        st.markdown("---")
        
        # Rating by Type
        st.markdown("### 📊 Rating Distribution by Content Type")
        
        rating_type = df.groupby(['Content_For', 'type']).size().reset_index(name='Count')
        
        fig = px.bar(rating_type, x='Content_For', y='Count', color='type',
                    color_discrete_map={'Movie':'#E50914', 'TV Show':'#ffffff'},
                    title='Content Type Distribution Across Audience Categories',
                    barmode='group')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Audience Statistics Table
        st.markdown("**📋 Audience Category Statistics**")
        audience_stats = df.groupby('Content_For').agg({
            'title': 'count',
            'release_year': 'mean'
        }).reset_index()
        audience_stats.columns = ['Audience', 'Total Content', 'Avg Release Year']
        audience_stats = audience_stats.sort_values('Total Content', ascending=False)
        
        st.dataframe(audience_stats.style.format({
            'Total Content': '{:,}',
            'Avg Release Year': '{:.0f}'
        }), use_container_width=True, hide_index=True)

    # TAB 5: Recommendations
    with tabs[4]:
        logging.info("Rendering Tab: Recommendations")
        st.header("💡 Strategic Recommendations & Future Outlook")
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(229, 9, 20, 0.1), rgba(255, 107, 107, 0.1)); 
                    padding: 1.5rem; border-radius: 15px; border-left: 5px solid #E50914; margin-bottom: 2rem;'>
            <h3 style='color: #E50914; margin-top: 0;'>🚀 Executive Summary</h3>
            <p style='color: #cbd5e1; line-height: 1.8;'>
                To sustain growth, Netflix must pivot from a volume-based strategy to a <strong>value-driven, localized approach</strong>. 
                Our analysis identifies clear opportunities in <strong>Asian markets</strong>, <strong>underserved genre niches</strong>, 
                and <strong>optimized content formats</strong> for specific audience segments.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # --- Strategic Pillars ---
        st.subheader("🏗️ Strategic Pillars")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-container" style="height: 100%;">
                <div class="metric-icon">🌏</div>
                <h4 style="color: #E50914; margin: 0;">Localization</h4>
                <p style="font-size: 0.8rem; margin-top: 0.5rem; color: #cbd5e1;">Deepen investment in local language originals, specifically in India, South Korea, and Japan.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="metric-container" style="height: 100%;">
                <div class="metric-icon">🎭</div>
                <h4 style="color: #ff6b6b; margin: 0;">Diversification</h4>
                <p style="font-size: 0.8rem; margin-top: 0.5rem; color: #cbd5e1;">Expand into Anime, Documentaries, and Reality TV to capture niche but loyal audiences.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="metric-container" style="height: 100%;">
                <div class="metric-icon">⏱️</div>
                <h4 style="color: #c92a2a; margin: 0;">Optimization</h4>
                <p style="font-size: 0.8rem; margin-top: 0.5rem; color: #cbd5e1;">Focus on 8-10 episode Limited Series which show higher completion rates than long-running shows.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
            <div class="metric-container" style="height: 100%;">
                <div class="metric-icon">👨‍👩‍👧</div>
                <h4 style="color: #862e9c; margin: 0;">Retention</h4>
                <p style="font-size: 0.8rem; margin-top: 0.5rem; color: #cbd5e1;">Bolster the Kids & Family library to reduce churn among household subscribers.</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        
        # --- Market Opportunity Heatmap ---
        st.subheader("🗺️ Global Content Opportunity Heatmap")
        st.markdown("*Identifying genre gaps across key regions*")
        
        # Data Prep for Heatmap
        # Merge genres and countries on original_index
        genre_country = pd.merge(genres_df, countries_df, on="original_index")
        # Filter for top 10 genres and top 10 countries to keep heatmap readable
        top_10_genres = genres_df['genre'].value_counts().head(10).index
        top_10_countries = countries_df['country_unnested'].value_counts().head(10).index
        
        gc_filtered = genre_country[
            (genre_country['genre'].isin(top_10_genres)) & 
            (genre_country['country_unnested'].isin(top_10_countries)) &
            (genre_country['country_unnested'] != 'Unknown')
        ]
        
        heatmap_data = pd.crosstab(gc_filtered['genre'], gc_filtered['country_unnested'])
        
        fig_heat = px.imshow(heatmap_data,
                             labels=dict(x="Country", y="Genre", color="Content Count"),
                             x=heatmap_data.columns,
                             y=heatmap_data.index,
                             color_continuous_scale='Reds',
                             aspect="auto")
        fig_heat.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1')
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        st.info("💡 **Opportunity:** Darker squares indicate saturation. Lighter squares represent potential market gaps where demand might exist but supply is low (e.g., Anime in non-Japanese markets, or Documentaries in India).")

        st.markdown("---")

        # --- Interactive Strategy Simulator ---
        st.subheader("🛠️ Content Strategy Simulator")
        st.markdown("""
        <div style='background: rgba(20, 20, 20, 0.5); padding: 1rem; border-radius: 10px; border: 1px solid rgba(229, 9, 20, 0.3);'>
            <p style='color: #cbd5e1; margin: 0;'>
                Use this tool to simulate a new content launch. Select your target parameters to see current market saturation and historical performance benchmarks.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sim_genre = st.selectbox("Target Genre", sorted(genres_df['genre'].unique()), key='sim_genre')
        with col2:
            sim_type = st.selectbox("Content Format", ["Movie", "TV Show"], key='sim_type')
        with col3:
            sim_audience = st.selectbox("Target Audience", sorted(df['Content_For'].dropna().unique()), key='sim_audience')
        
        logging.info(f"Strategy Simulator: Genre={sim_genre}, Type={sim_type}, Audience={sim_audience}")
            
        # Calculation
        # Filter main df
        # We need to filter by genre (which is in listed_in string)
        mask = (df['listed_in'].str.contains(sim_genre, na=False)) & \
               (df['type'] == sim_type) & \
               (df['Content_For'] == sim_audience)
        
        sim_data = df[mask]
        
        st.markdown("### 📊 Market Analysis Report")
        
        if len(sim_data) > 0:
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("📦 Existing Titles", f"{len(sim_data)}")
            with m2:
                if sim_type == "Movie":
                    avg_dur = sim_data['Movie_duration'].mean()
                    st.metric("⏱️ Avg Duration", f"{avg_dur:.0f} min")
                else:
                    avg_dur = sim_data['Series_duration'].mean()
                    st.metric("⏱️ Avg Duration", f"{avg_dur:.1f} seasons")
            with m3:
                # Top country for this niche
                top_c = sim_data['country'].value_counts().index[0] if not sim_data['country'].value_counts().empty else "Unknown"
                st.metric("🏆 Dominant Market", str(top_c)[:15])
            
            # Saturation Gauge
            saturation_level = len(sim_data)
            if saturation_level < 50:
                status = "🔵 Blue Ocean (High Opportunity)"
                color = "#38ef7d"
            elif saturation_level < 200:
                status = "🟡 Competitive (Moderate)"
                color = "#fb923c"
            else:
                status = "🔴 Saturated (High Competition)"
                color = "#ff6b6b"
                
            st.markdown(f"""
            <div style='background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 10px; margin-top: 1rem; text-align: center; border: 1px solid {color};'>
                <h4 style='color: #cbd5e1; margin: 0;'>Market Status</h4>
                <h2 style='color: {color}; margin: 0.5rem 0;'>{status}</h2>
                <p style='font-size: 0.9rem; color: #cbd5e1;'>There are currently <strong>{saturation_level}</strong> titles matching these criteria.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show recent examples
            st.markdown("**Recent Examples in this Niche:**")
            st.dataframe(sim_data[['title', 'release_year', 'country', 'rating']].sort_values('release_year', ascending=False).head(5), use_container_width=True)
            
        else:
            st.warning("⚠️ No existing content found matching these exact criteria. This could be a **massive untapped opportunity** or a **niche with no demand**.")
            st.markdown("### 🚀 Recommendation: Pilot Project")
            st.write("Consider launching a low-budget pilot or acquiring a license to test this specific market segment.")

    # TAB 6: Complete Analysis
    with tabs[5]:
        logging.info("Rendering Tab: Complete Analysis")
        st.header("📑 Complete Analysis Report")
        
        import textwrap
        
        # Executive Summary Banner
        st.markdown(textwrap.dedent("""
        <div style='background: linear-gradient(135deg, #E50914 0%, #B20710 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem;'>
            <h2 style='color: white !important; margin: 0 0 1rem 0; text-align: center;'>📊 Executive Summary</h2>
            <p style='color: white; font-size: 1.1rem; line-height: 1.8; text-align: center; margin: 0;'>
                Analysis of <strong>8,807 titles</strong> reveals a strategic pivot towards <strong>Original Content</strong> and 
                <strong>International Expansion</strong>. Key opportunities lie in hyper-localization for emerging markets, 
                optimizing content formats for retention, and diversifying into high-demand niche genres.
            </p>
        </div>
        """), unsafe_allow_html=True)
        
        # Key Metrics Dashboard
        st.markdown("### 📈 Key Performance Indicators")
        
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        with kpi1:
            total_titles = len(df)
            st.metric(
                label="🎬 Total Titles",
                value=f"{total_titles:,}",
                delta="Content Library"
            )
        
        with kpi2:
            movies_count = len(df[df['type']=='Movie'])
            movie_pct = (movies_count / total_titles) * 100
            st.metric(
                label="🎥 Movies Share",
                value=f"{movie_pct:.1f}%",
                delta=f"{movies_count:,} titles"
            )
        
        with kpi3:
            tv_count = len(df[df['type']=='TV Show'])
            tv_pct = (tv_count / total_titles) * 100
            st.metric(
                label="📺 TV Shows Share",
                value=f"{tv_pct:.1f}%",
                delta=f"{tv_count:,} titles"
            )
        
        with kpi4:
            top_country = df['country'].mode()[0]
            st.metric(
                label="🌍 Top Market",
                value=top_country,
                delta="Production Hub"
            )
        
        st.markdown("---")
        
        # Detailed Insights Section
        st.markdown("### 🔍 Detailed Insights")
        
        insight_tabs = st.tabs(["👥 Audience", "🎭 Content Strategy", "🌍 Geographic", "⏱️ Duration"])
        
        # Audience Tab
        with insight_tabs[0]:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(textwrap.dedent("""
                <div class='card' style='background: linear-gradient(135deg, #E50914 0%, #B20710 100%); text-align: left; padding: 1.5rem; border-radius: 10px;'>
                    <div style='font-size: 2rem; margin-bottom: 1rem;'>👨👩</div>
                    <h3 style='color: white !important; margin: 0 0 1rem 0;'>Target Audience</h3>
                    <p style='color: rgba(255,255,255,0.9); line-height: 1.8;'>
                        • <strong>Adults (TV-MA, R):</strong> Dominant segment<br>
                        • <strong>Teens (TV-14):</strong> Strong secondary focus<br>
                        • <strong>Kids:</strong> Significant gap vs competitors<br>
                        • <strong>Strategy:</strong> Mature content drives subs
                    </p>
                </div>
                """), unsafe_allow_html=True)
            
            with col2:
                # Audience distribution chart
                audience_counts = df['Content_For'].value_counts().reset_index()
                audience_counts.columns = ['Audience', 'Count']
                
                fig = px.pie(audience_counts, values='Count', names='Audience',
                            title='Content Distribution by Audience',
                            color_discrete_sequence=['#E50914', '#ff6b6b', '#c92a2a', '#862e9c'])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#cbd5e1')
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Content Strategy Tab
        with insight_tabs[1]:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(textwrap.dedent("""
                <div class='card' style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); text-align: left; padding: 1.5rem; border-radius: 10px;'>
                    <div style='font-size: 2rem; margin-bottom: 1rem;'>🎭</div>
                    <h3 style='color: white !important; margin: 0 0 1rem 0;'>Genre Trends</h3>
                    <p style='color: rgba(255,255,255,0.9); line-height: 1.8;'>
                        • <strong>Top Genres:</strong> Dramas, Comedies<br>
                        • <strong>Rising Stars:</strong> Documentaries, Anime<br>
                        • <strong>Niche:</strong> Reality TV, Sci-Fi<br>
                        • <strong>Insight:</strong> Diversification key to growth
                    </p>
                </div>
                """), unsafe_allow_html=True)
            
            with col2:
                # Top Genres Chart
                top_genres = genres_df['genre'].value_counts().head(10).reset_index()
                top_genres.columns = ['Genre', 'Count']
                
                fig = px.bar(top_genres, x='Count', y='Genre', orientation='h',
                            title='Top 10 Genres',
                            color='Count', color_continuous_scale='Reds')
                fig.update_layout(
                    yaxis={'categoryorder':'total ascending'},
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#cbd5e1')
                )
                st.plotly_chart(fig, use_container_width=True)

        # Geographic Tab
        with insight_tabs[2]:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(textwrap.dedent("""
                <div class='card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); text-align: left; padding: 1.5rem; border-radius: 10px;'>
                    <div style='font-size: 2rem; margin-bottom: 1rem;'>🌍</div>
                    <h3 style='color: white !important; margin: 0 0 1rem 0;'>Global Footprint</h3>
                    <p style='color: rgba(255,255,255,0.9); line-height: 1.8;'>
                        • <strong>USA:</strong> Primary production hub<br>
                        • <strong>India:</strong> High volume, high growth<br>
                        • <strong>East Asia:</strong> Korea & Japan rising<br>
                        • <strong>Europe:</strong> UK & Spain leading
                    </p>
                </div>
                """), unsafe_allow_html=True)
            
            with col2:
                # Top Countries Chart
                top_countries = countries_df['country_unnested'].value_counts().head(10).reset_index()
                top_countries.columns = ['Country', 'Count']
                top_countries = top_countries[top_countries['Country'] != 'Unknown']
                
                fig = px.bar(top_countries, x='Country', y='Count',
                            title='Top Production Countries',
                            color='Count', color_continuous_scale='Reds')
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#cbd5e1')
                )
                st.plotly_chart(fig, use_container_width=True)

        # Duration Tab
        with insight_tabs[3]:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(textwrap.dedent("""
                <div class='card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); text-align: left; padding: 1.5rem; border-radius: 10px;'>
                    <div style='font-size: 2rem; margin-bottom: 1rem;'>⏱️</div>
                    <h3 style='color: white !important; margin: 0 0 1rem 0;'>Format Analysis</h3>
                    <p style='color: rgba(255,255,255,0.9); line-height: 1.8;'>
                        • <strong>Movies:</strong> 90-100 min sweet spot<br>
                        • <strong>TV Shows:</strong> 1-Season Limited Series<br>
                        • <strong>Trend:</strong> Shorter, bingeable formats<br>
                        • <strong>Risk:</strong> Long-running series cancellations
                    </p>
                </div>
                """), unsafe_allow_html=True)
            
            with col2:
                # Duration Chart (Movies)
                fig = px.histogram(df[df['type']=='Movie'].dropna(subset=['Movie_duration']), 
                                  x='Movie_duration', nbins=30,
                                  title='Movie Duration Distribution',
                                  color_discrete_sequence=['#E50914'])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#cbd5e1')
                )
                st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        
        # Strategic Recommendations
        st.markdown("### 🚀 Strategic Recommendations")
        
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            with st.expander("🎯 **Content Strategy**", expanded=True):
                st.markdown(textwrap.dedent("""
                #### Immediate Actions:
                1. **Hyper-Localization**
                   - Invest in local language originals (India, LATAM)
                   - "Local stories, global appeal" (e.g., Squid Game)
                
                2. **Format Optimization**
                   - Prioritize Limited Series (6-10 eps)
                   - Reduce risk of long-term commitments
                
                3. **Genre Diversification**
                   - Expand Anime library (high engagement)
                   - Invest in True Crime & Reality TV (low cost, high buzz)
                """))
            
            with st.expander("👨‍👩‍👧 **Audience Growth**", expanded=True):
                st.markdown(textwrap.dedent("""
                #### Target Segments:
                1. **Kids & Family**
                   - Bolster animation library to compete with Disney+
                   - Create "Family Movie Night" bundles
                
                2. **Teens & Young Adults**
                   - Focus on YA adaptations and coming-of-age dramas
                   - Leverage social media trends for promotion
                """))
        
        with rec_col2:
            with st.expander("💰 **Business Impact**", expanded=True):
                st.markdown(textwrap.dedent("""
                #### Expected Outcomes:
                1. **Retention**
                   - Lower churn through consistent "event" releases
                   - Higher engagement with bingeable formats
                
                2. **Acquisition**
                   - New subs from emerging markets via localization
                   - Niche audiences via genre expansion
                
                3. **Brand Value**
                   - "Home of Originals" positioning
                   - Cultural dominance via global hits
                """))
            
            with st.expander("📊 **Data-Driven Tactics**", expanded=True):
                st.markdown(textwrap.dedent("""
                #### Analytics Focus:
                1. **Completion Rates**
                   - Monitor drop-off points in pilot episodes
                
                2. **Regional Demand**
                   - Heatmap analysis for under-served regions
                
                3. **Social Sentiment**
                   - Track viral potential of new releases
                """))
        
        # Expected Impact Summary
        st.markdown("---")
        st.markdown("### 📊 Projected Growth")
        
        impact_col1, impact_col2, impact_col3 = st.columns(3)
        
        with impact_col1:
            st.markdown(textwrap.dedent("""
            <div style='text-align: center; padding: 1rem; background: rgba(229, 9, 20, 0.1); border-radius: 10px;'>
                <div style='font-size: 2rem;'>📈</div>
                <div style='font-size: 1.5rem; font-weight: bold; color: #E50914;'>+15-20%</div>
                <div style='color: #cbd5e1;'>Intl. Sub Growth</div>
            </div>
            """), unsafe_allow_html=True)
            
        with impact_col2:
            st.markdown(textwrap.dedent("""
            <div style='text-align: center; padding: 1rem; background: rgba(229, 9, 20, 0.1); border-radius: 10px;'>
                <div style='font-size: 2rem;'>📉</div>
                <div style='font-size: 1.5rem; font-weight: bold; color: #E50914;'>-5-8%</div>
                <div style='color: #cbd5e1;'>Churn Rate Reduction</div>
            </div>
            """), unsafe_allow_html=True)
            
        with impact_col3:
            st.markdown(textwrap.dedent("""
            <div style='text-align: center; padding: 1rem; background: rgba(229, 9, 20, 0.1); border-radius: 10px;'>
                <div style='font-size: 2rem;'>💰</div>
                <div style='font-size: 1.5rem; font-weight: bold; color: #E50914;'>High</div>
                <div style='color: #cbd5e1;'>ROI on Originals</div>
            </div>
            """), unsafe_allow_html=True)

    # TAB 7: App Logs
    with tabs[6]:
        logging.info("Rendering Tab: App Logs")
        st.header("📝 Application Logs")
        
        st.markdown("""
        <div style='background: rgba(20, 20, 20, 0.5); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
            <p style='color: #cbd5e1; margin: 0;'>
                System logs for debugging and tracking application events.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Log Display Area
        log_contents = log_capture_string.getvalue()
        
        if not log_contents:
            st.info("ℹ️ No logs recorded yet.")
        else:
            st.code(log_contents, language='text')
            
        # Add a download button for logs
        st.download_button(
            label="⬇️ Download Logs",
            data=log_contents,
            file_name="netflix_app_logs.txt",
            mime="text/plain"
        )
        
        # Test Log Button
        if st.button("Generate Test Log"):
            logging.info("Test log entry generated by user.")
            st.rerun()

else:
    st.error("Could not load data. Please ensure 'netflix.csv' is in the same directory as this app.")
