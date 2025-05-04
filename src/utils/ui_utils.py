import streamlit as st
import pandas as pd
import numpy as np
import base64
from PIL import Image
from typing import Dict, List, Tuple, Optional, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def set_page_config(title: str = "AI Health Trainer", 
                    icon: str = "💪", 
                    layout: str = "wide",
                    initial_sidebar_state: str = "expanded") -> None:
    """
    Set Streamlit page configuration
    
    Args:
        title: Page title
        icon: Page icon
        layout: Page layout
        initial_sidebar_state: Initial sidebar state
    """
    try:
        st.set_page_config(
            page_title=title,
            page_icon=icon,
            layout=layout,
            initial_sidebar_state=initial_sidebar_state
        )
        logger.info("Page config set successfully")
    except Exception as e:
        logger.error(f"Error setting page config: {e}")

def apply_custom_css() -> None:
    """
    Apply custom CSS styling to the Streamlit app
    """
    try:
        st.markdown("""
        <style>
        /* Main background and text colors */
        .main {
            background-color: #121212;
            color: #e0e0e0;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #1e1e1e;
        }
        
        /* Make text in sidebar white */
        .css-1d391kg .stMarkdown p {
            color: #ffffff;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(90deg, #4CAF50 0%, #2e7d32 100%);
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: 500;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #2e7d32 0%, #4CAF50 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
        }
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 2px 3px rgba(0, 0, 0, 0.2);
        }
        
        /* Title container styling */
        .title-container {
            background: linear-gradient(135deg, #1e1e1e 0%, #2c3e50 100%);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            border-left: 5px solid #4CAF50;
        }
        .title {
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            padding: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        .subtitle {
            color: #ecf0f1;
            font-size: 1.2rem;
            margin-top: 0.5rem;
            opacity: 0.9;
        }
        
        /* Card styling */
        .card {
            background-color: #1e1e1e;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
            border-left: 3px solid #4CAF50;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.4);
        }
        .card-title {
            color: #4CAF50;
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        .card-content {
            color: #e0e0e0;
        }
        
        /* Metric container styling */
        .metric-container {
            background-color: #2c3e50;
            padding: 1.2rem;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        .metric-container:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.3);
        }
        .metric-value {
            font-size: 2.2rem;
            font-weight: 700;
            color: #4CAF50;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        }
        .metric-label {
            font-size: 1rem;
            color: #e0e0e0;
            margin-top: 0.3rem;
        }
        
        /* Info box styles */
        .info-box {
            background-color: #1a2735;
            padding: 1rem;
            border-radius: 8px;
            border-left: 5px solid #2196f3;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }
        .success-box {
            background-color: #1a2b1d;
            padding: 1rem;
            border-radius: 8px;
            border-left: 5px solid #4caf50;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }
        .warning-box {
            background-color: #2b2310;
            padding: 1rem;
            border-radius: 8px;
            border-left: 5px solid #ffc107;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }
        .error-box {
            background-color: #2b1116;
            padding: 1rem;
            border-radius: 8px;
            border-left: 5px solid #e91e63;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }
        
        /* Table styling */
        .stDataFrame {
            background-color: #1e1e1e !important;
        }
        .dataframe {
            background-color: #1e1e1e !important;
            color: #e0e0e0 !important;
        }
        .dataframe th {
            background-color: #2c3e50 !important;
            color: white !important;
        }
        .dataframe td {
            background-color: #1e1e1e !important;
            color: #e0e0e0 !important;
        }
        
        /* Sidebar navigation buttons */
        .stSidebar button {
            width: 100%;
            text-align: left;
            margin-bottom: 8px;
            border-radius: 5px;
            border: none;
            background-color: rgba(76, 175, 80, 0.1);
            color: #e0e0e0;
            transition: all 0.3s;
            padding: 10px 15px;
        }
        .stSidebar button:hover {
            background-color: rgba(76, 175, 80, 0.3);
            transform: translateX(5px);
        }
        
        /* Form field styling */
        .stTextInput > div > div > input {
            background-color: #2c3e50;
            color: white;
            border: 1px solid #4CAF50;
        }
        .stNumberInput > div > div > input {
            background-color: #2c3e50;
            color: white;
            border: 1px solid #4CAF50;
        }
        .stTextArea > div > div > textarea {
            background-color: #2c3e50;
            color: white;
            border: 1px solid #4CAF50;
        }
        .stSelectbox > div > div > select {
            background-color: #2c3e50;
            color: white;
            border: 1px solid #4CAF50;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #1e1e1e;
            color: #e0e0e0;
            border-radius: 5px 5px 0 0;
            border: none;
            padding: 10px 20px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #4CAF50 !important;
            color: white !important;
        }
        
        /* Slider styling */
        .stSlider [data-baseweb="slider"] > div {
            background-color: #555555 !important;
        }
        .stSlider [data-baseweb="slider"] > div > div > div {
            background-color: #4CAF50 !important;
        }
        .stSlider [data-baseweb="slider"] > div > div {
            background-color: #4CAF50 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        logger.info("Custom CSS applied successfully")
    except Exception as e:
        logger.error(f"Error applying custom CSS: {e}")

def display_header(title: str, subtitle: str = "") -> None:
    """
    Display page header with title and subtitle
    
    Args:
        title: Page title
        subtitle: Page subtitle
    """
    try:
        st.markdown(f"""
        <div class="title-container">
            <h1 class="title">{title}</h1>
            <p class="subtitle">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
        logger.info(f"Header displayed: {title}")
    except Exception as e:
        logger.error(f"Error displaying header: {e}")
        st.title(title)
        if subtitle:
            st.subheader(subtitle)

def create_card(title: str, content: str, key: Optional[str] = None) -> None:
    """
    Create a styled card with title and content
    
    Args:
        title: Card title
        content: Card content (can include HTML)
        key: Optional key for the component
    """
    try:
        st.markdown(f"""
        <div class="card">
            <h2 class="card-title">{title}</h2>
            <div class="card-content">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True, key=key)
    except Exception as e:
        logger.error(f"Error creating card: {e}")
        st.subheader(title)
        st.markdown(content, unsafe_allow_html=True)

def display_metric(value: Any, label: str, prefix: str = "", suffix: str = "") -> None:
    """
    Display a metric value with label
    
    Args:
        value: Metric value
        label: Metric label
        prefix: Prefix for the value
        suffix: Suffix for the value
    """
    try:
        display_value = f"{prefix}{value}{suffix}"
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{display_value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error displaying metric: {e}")
        st.metric(label=label, value=f"{prefix}{value}{suffix}")

def show_info_box(message: str) -> None:
    """
    Display an info box with a message
    
    Args:
        message: Message to display
    """
    try:
        st.markdown(f"""
        <div class="info-box">
            <p>ℹ️ {message}</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error showing info box: {e}")
        st.info(message)

def show_success_box(message: str) -> None:
    """
    Display a success box with a message
    
    Args:
        message: Message to display
    """
    try:
        st.markdown(f"""
        <div class="success-box">
            <p>✅ {message}</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error showing success box: {e}")
        st.success(message)

def show_warning_box(message: str) -> None:
    """
    Display a warning box with a message
    
    Args:
        message: Message to display
    """
    try:
        st.markdown(f"""
        <div class="warning-box">
            <p>⚠️ {message}</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error showing warning box: {e}")
        st.warning(message)

def show_error_box(message: str) -> None:
    """
    Display an error box with a message
    
    Args:
        message: Message to display
    """
    try:
        st.markdown(f"""
        <div class="error-box">
            <p>❌ {message}</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error showing error box: {e}")
        st.error(message)

def get_image_base64(image_path: str) -> Optional[str]:
    """
    Convert an image to base64 encoding
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Base64 encoded string or None if error
    """
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        logger.error(f"Error encoding image: {e}")
        return None

def display_exercise_card(exercise: str, description: str, image_path: Optional[str] = None) -> None:
    """
    Display an exercise card with name, description, and optional image
    
    Args:
        exercise: Exercise name
        description: Exercise description
        image_path: Optional path to exercise image
    """
    try:
        image_html = ""
        if image_path:
            img_base64 = get_image_base64(image_path)
            if img_base64:
                image_html = f'<img src="data:image/png;base64,{img_base64}" alt="{exercise}" style="width:100%; border-radius:5px; margin-bottom:10px;">'
        
        st.markdown(f"""
        <div class="card">
            <h2 class="card-title">{exercise}</h2>
            {image_html}
            <div class="card-content">
                {description}
            </div>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error displaying exercise card: {e}")
        st.subheader(exercise)
        if image_path:
            try:
                st.image(image_path, caption=exercise)
            except:
                pass
        st.markdown(description)

def loading_animation() -> None:
    """
    Display a loading animation
    """
    st.markdown("""
    <style>
    .loader {
        border: 8px solid #1e1e1e;
        border-top: 8px solid #4CAF50;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    <div class="loader"></div>
    """, unsafe_allow_html=True)

def display_progress_summary(stats: Dict[str, Any]) -> None:
    """
    Display a summary of progress statistics
    
    Args:
        stats: Dictionary containing progress statistics
    """
    try:
        tracked_days = stats.get("tracked_days", 0)
        total_workouts = stats.get("total_workouts", 0)
        
        # Calculate workout frequency
        frequency = f"{total_workouts/tracked_days:.1f}" if tracked_days > 0 else "0"
        
        # Format weight change
        weight_change = stats.get("weight_change")
        if weight_change is not None:
            weight_text = f"{weight_change:.1f} kg"
            weight_icon = "📉" if weight_change < 0 else "📈"
        else:
            weight_text = "No data"
            weight_icon = "❓"
            
        # Format body fat change
        bf_change = stats.get("body_fat_change")
        if bf_change is not None:
            bf_text = f"{bf_change:.1f}%"
            bf_icon = "📉" if bf_change < 0 else "📈"
        else:
            bf_text = "No data"
            bf_icon = "❓"
        
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
            <div class="metric-container" style="flex: 1;">
                <div class="metric-value">{tracked_days}</div>
                <div class="metric-label">Days Tracked</div>
            </div>
            <div class="metric-container" style="flex: 1;">
                <div class="metric-value">{total_workouts}</div>
                <div class="metric-label">Workouts</div>
            </div>
            <div class="metric-container" style="flex: 1;">
                <div class="metric-value">{frequency}</div>
                <div class="metric-label">Workouts/Week</div>
            </div>
            <div class="metric-container" style="flex: 1;">
                <div class="metric-value">{weight_icon} {weight_text}</div>
                <div class="metric-label">Weight Change</div>
            </div>
            <div class="metric-container" style="flex: 1;">
                <div class="metric-value">{bf_icon} {bf_text}</div>
                <div class="metric-label">Body Fat Change</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error displaying progress summary: {e}")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Days Tracked", stats.get("tracked_days", 0))
        with col2:
            st.metric("Workouts", stats.get("total_workouts", 0))
        with col3:
            frequency = f"{stats.get('total_workouts', 0)/stats.get('tracked_days', 1):.1f}" if stats.get("tracked_days", 0) > 0 else "0"
            st.metric("Workouts/Week", frequency)
        with col4:
            weight_change = stats.get("weight_change")
            if weight_change is not None:
                st.metric("Weight Change", f"{weight_change:.1f} kg")
            else:
                st.metric("Weight Change", "No data")
        with col5:
            bf_change = stats.get("body_fat_change")
            if bf_change is not None:
                st.metric("Body Fat Change", f"{bf_change:.1f}%")
            else:
                st.metric("Body Fat Change", "No data")

def display_feedback(feedback: str, is_correct: bool) -> None:
    """
    Display exercise form feedback
    
    Args:
        feedback: Feedback text
        is_correct: Whether the form is correct
    """
    try:
        if is_correct:
            st.markdown(f"""
            <div class="success-box">
                <p>✅ {feedback}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="warning-box">
                <p>⚠️ {feedback}</p>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error displaying feedback: {e}")
        if is_correct:
            st.success(feedback)
        else:
            st.warning(feedback) 