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
            background-color: #0e1117;
            color: #f0f2f6;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Sidebar styling */
        .css-1d391kg, [data-testid="stSidebar"] {
            background-color: #161b25;
            border-right: 1px solid #2c3347;
        }
        
        /* Make text in sidebar white */
        .css-1d391kg .stMarkdown p, [data-testid="stSidebar"] .stMarkdown p {
            color: #f0f2f6;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(90deg, #5465ff 0%, #788bff 100%);
            color: white;
            border-radius: 12px;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: 500;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(84, 101, 255, 0.3);
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #788bff 0%, #5465ff 100%);
            transform: translateY(-2px);
            box-shadow: 0 8px 18px rgba(84, 101, 255, 0.35);
        }
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 2px 5px rgba(84, 101, 255, 0.25);
        }
        
        /* Title container styling */
        .title-container {
            background: linear-gradient(135deg, #232b3d 0%, #161b25 100%);
            padding: 2.5rem;
            border-radius: 18px;
            margin-bottom: 2.5rem;
            text-align: center;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
            border-left: 6px solid #5465ff;
        }
        .title {
            color: white;
            font-size: 2.8rem;
            font-weight: 700;
            margin: 0;
            padding: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            letter-spacing: 0.5px;
        }
        .subtitle {
            color: #bdc3c7;
            font-size: 1.3rem;
            margin-top: 0.6rem;
            opacity: 0.95;
            letter-spacing: 0.3px;
        }
        
        /* Card styling */
        .card {
            background: linear-gradient(145deg, #1e2738 0%, #161b25 100%);
            padding: 1.8rem;
            border-radius: 16px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
            margin-bottom: 2rem;
            transition: all 0.35s ease;
            border-left: 4px solid #5465ff;
            border-top: 1px solid #2c3347;
            position: relative;
            overflow: hidden;
        }
        .card:hover {
            transform: translateY(-6px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
        }
        .card::after {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 150px;
            height: 150px;
            background: radial-gradient(circle, rgba(84, 101, 255, 0.1) 0%, rgba(0, 0, 0, 0) 70%);
            border-radius: 50%;
            transform: translate(50%, -50%);
        }
        .card-title {
            color: #5465ff;
            font-size: 1.7rem;
            font-weight: 600;
            margin-bottom: 1.2rem;
            letter-spacing: 0.5px;
            position: relative;
        }
        .card-content {
            color: #f0f2f6;
            line-height: 1.6;
            font-size: 1.05rem;
        }
        
        /* Metric container styling */
        .metric-container {
            background: linear-gradient(145deg, #1e2738 0%, #161b25 100%);
            padding: 1.5rem;
            border-radius: 14px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            transition: all 0.35s ease;
            border-top: 1px solid #2c3347;
            position: relative;
            overflow: hidden;
        }
        .metric-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.25);
        }
        .metric-container::after {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100px;
            height: 100px;
            background: radial-gradient(circle, rgba(84, 101, 255, 0.1) 0%, rgba(0, 0, 0, 0) 70%);
            border-radius: 50%;
            transform: translate(30%, -30%);
        }
        .metric-value {
            font-size: 2.4rem;
            font-weight: 700;
            color: #5465ff;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            position: relative;
        }
        .metric-label {
            font-size: 1.1rem;
            color: #bdc3c7;
            margin-top: 0.5rem;
            letter-spacing: 0.3px;
        }
        
        /* Info box styles */
        .info-box {
            background: linear-gradient(145deg, #192234 0%, #0d1117 100%);
            padding: 1.2rem;
            border-radius: 12px;
            border-left: 5px solid #3498db;
            margin-bottom: 1.2rem;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }
        .success-box {
            background: linear-gradient(145deg, #192234 0%, #0d1117 100%);
            padding: 1.2rem;
            border-radius: 12px;
            border-left: 5px solid #2ecc71;
            margin-bottom: 1.2rem;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }
        .warning-box {
            background: linear-gradient(145deg, #192234 0%, #0d1117 100%);
            padding: 1.2rem;
            border-radius: 12px;
            border-left: 5px solid #f39c12;
            margin-bottom: 1.2rem;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }
        .error-box {
            background: linear-gradient(145deg, #192234 0%, #0d1117 100%);
            padding: 1.2rem;
            border-radius: 12px;
            border-left: 5px solid #e74c3c;
            margin-bottom: 1.2rem;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }
        
        /* Table styling */
        .stDataFrame {
            background-color: #161b25 !important;
            border-radius: 12px !important;
            overflow: hidden !important;
        }
        .dataframe {
            background-color: #161b25 !important;
            color: #f0f2f6 !important;
            border-radius: 12px !important;
        }
        .dataframe th {
            background-color: #232b3d !important;
            color: white !important;
            padding: 12px !important;
            font-size: 1.05rem !important;
        }
        .dataframe td {
            background-color: #1a2133 !important;
            color: #f0f2f6 !important;
            padding: 10px !important;
        }
        
        /* Sidebar navigation buttons */
        .stSidebar button {
            width: 100%;
            text-align: left;
            margin-bottom: 10px;
            border-radius: 10px;
            border: none;
            background-color: rgba(84, 101, 255, 0.1);
            color: #f0f2f6;
            transition: all 0.3s;
            padding: 12px 16px;
            font-weight: 500;
        }
        .stSidebar button:hover {
            background-color: rgba(84, 101, 255, 0.2);
            transform: translateX(5px);
        }
        
        /* Form field styling */
        .stTextInput > div > div > input {
            background-color: #1a2133;
            color: white;
            border: 1px solid #2c3347;
            border-radius: 8px;
            padding: 10px 14px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .stNumberInput > div > div > input {
            background-color: #1a2133;
            color: white;
            border: 1px solid #2c3347;
            border-radius: 8px;
            padding: 10px 14px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .stTextArea > div > div > textarea {
            background-color: #1a2133;
            color: white;
            border: 1px solid #2c3347;
            border-radius: 8px;
            padding: 10px 14px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .stSelectbox > div > div > select {
            background-color: #1a2133;
            color: white;
            border: 1px solid #2c3347;
            border-radius: 8px;
            padding: 10px 14px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: #161b25;
            padding: 10px;
            border-radius: 12px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #1a2133;
            color: #f0f2f6;
            border-radius: 10px;
            border: none;
            padding: 10px 20px;
            font-weight: 500;
        }
        .stTabs [aria-selected="true"] {
            background-color: #5465ff !important;
            color: white !important;
            font-weight: 600 !important;
        }
        
        /* Slider styling */
        .stSlider [data-baseweb="slider"] > div {
            background-color: #2c3347 !important;
        }
        .stSlider [data-baseweb="slider"] > div > div > div {
            background-color: #5465ff !important;
        }
        .stSlider [data-baseweb="slider"] > div > div {
            background-color: #5465ff !important;
        }
        
        /* Checkbox styling */
        .stCheckbox [data-baseweb="checkbox"] {
            border-radius: 6px !important;
        }
        
        /* Radio button styling */
        .stRadio [data-baseweb="radio"] {
            border-radius: 50% !important;
        }
        
        /* Select box arrow styling */
        .stSelectbox [data-baseweb="select"] > div:first-child {
            background-color: #1a2133 !important;
            border-radius: 8px !important;
        }
        
        /* Multi-select styling */
        .stMultiSelect [data-baseweb="select"] > div:first-child {
            background-color: #1a2133 !important;
            border-radius: 8px !important;
        }
        
        /* Progress bar styling */
        .stProgress > div > div > div > div {
            background-color: #5465ff !important;
        }
        
        /* Horizontal rule styling */
        hr {
            border-color: #2c3347 !important;
            margin: 1.5rem 0 !important;
        }
        
        /* Improve spacing of all components */
        div.block-container {
            padding-top: 1.5rem !important;
        }
        
        /* Make markdown text nicer */
        .stMarkdown {
            line-height: 1.6;
        }
        .stMarkdown p {
            margin-bottom: 1rem;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        .stMarkdown a {
            color: #5465ff;
            text-decoration: none;
            border-bottom: 1px dotted #5465ff;
        }
        .stMarkdown a:hover {
            border-bottom: 1px solid #5465ff;
        }
        
        /* Hide Streamlit's default page navigation */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        /* Hide Streamlit's deploy and hamburger menu */
        header [data-testid="stHeader"] {
            display: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        logger.info("Custom CSS applied successfully")
    except Exception as e:
        logger.error(f"Error applying custom CSS: {e}")

def display_header(title: str, subtitle: str = "", icon: str = None) -> None:
    """
    Display page header with title and subtitle
    
    Args:
        title: Page title
        subtitle: Page subtitle
        icon: Optional icon emoji to display
    """
    try:
        # Default icons based on page title
        default_icons = {
            "Exercise Recommendations": "📋",
            "Exercise Verification": "🏋️",
            "Body Analysis": "📏",
            "Progress Tracking": "📈",
            "AI Health Trainer": "💪"
        }
        
        # Use provided icon or get from defaults or use general default
        display_icon = icon or default_icons.get(title, "💪")
        
        st.markdown(f"""
        <div class="title-container">
            <div style="font-size: 3.2rem; margin-bottom: 0.8rem;">{display_icon}</div>
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

def create_card(title: str, content: str, icon: str = None, highlight_color: str = None, key: Optional[str] = None) -> None:
    """
    Create a styled card with title and content
    
    Args:
        title: Card title
        content: Card content (can include HTML)
        icon: Optional icon emoji to display with title
        highlight_color: Optional color to use for highlighting (hex code)
        key: Optional key for the component
    """
    try:
        # Set default highlight color if not provided
        highlight = highlight_color or "#5465ff"
        
        # Include icon if provided
        icon_html = f'<span style="margin-right: 0.5rem;">{icon}</span>' if icon else ''
        
        st.markdown(f"""
        <div class="card" style="border-left: 4px solid {highlight};">
            <h2 class="card-title" style="color: {highlight};">{icon_html}{title}</h2>
            <div class="card-content">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True, key=key)
    except Exception as e:
        logger.error(f"Error creating card: {e}")
        st.subheader(title)
        st.markdown(content, unsafe_allow_html=True)

def display_metric(value: Any, label: str, prefix: str = "", suffix: str = "", icon: str = None, highlight_color: str = None) -> None:
    """
    Display a metric value with label
    
    Args:
        value: Metric value
        label: Metric label
        prefix: Prefix for the value
        suffix: Suffix for the value
        icon: Optional icon emoji
        highlight_color: Optional color to use for highlighting (hex code)
    """
    try:
        display_value = f"{prefix}{value}{suffix}"
        # Set default highlight color if not provided
        highlight = highlight_color or "#5465ff"
        # Include icon if provided
        icon_html = f'<div style="font-size: 1.8rem; margin-bottom: 0.5rem;">{icon}</div>' if icon else ''
        
        st.markdown(f"""
        <div class="metric-container" style="border-top: 1px solid {highlight};">
            {icon_html}
            <div class="metric-value" style="color: {highlight};">{display_value}</div>
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
            <div style="display: flex; align-items: center;">
                <div style="font-size: 1.5rem; margin-right: 0.8rem;">ℹ️</div>
                <p style="margin: 0; font-size: 1.05rem;">{message}</p>
            </div>
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
            <div style="display: flex; align-items: center;">
                <div style="font-size: 1.5rem; margin-right: 0.8rem;">✅</div>
                <p style="margin: 0; font-size: 1.05rem;">{message}</p>
            </div>
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
            <div style="display: flex; align-items: center;">
                <div style="font-size: 1.5rem; margin-right: 0.8rem;">⚠️</div>
                <p style="margin: 0; font-size: 1.05rem;">{message}</p>
            </div>
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
            <div style="display: flex; align-items: center;">
                <div style="font-size: 1.5rem; margin-right: 0.8rem;">❌</div>
                <p style="margin: 0; font-size: 1.05rem;">{message}</p>
            </div>
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

def display_exercise_card(exercise: str, description: str, image_path: Optional[str] = None, icon: str = None) -> None:
    """
    Display an exercise card with name, description, and optional image
    
    Args:
        exercise: Exercise name
        description: Exercise description
        image_path: Optional path to exercise image
        icon: Optional icon emoji to display with title
    """
    try:
        image_html = ""
        if image_path:
            img_base64 = get_image_base64(image_path)
            if img_base64:
                image_html = f'<img src="data:image/png;base64,{img_base64}" alt="{exercise}" style="width:100%; border-radius:12px; margin-bottom:15px;">'
        
        # Include icon if provided
        icon_html = f'<span style="margin-right: 0.6rem;">{icon}</span>' if icon else ''
        
        # Generate exercise icon if not provided
        if not icon:
            exercise_icons = {
                "push": "💪", "pull": "🏋️", "squat": "🦵", "lunge": "🚶",
                "plank": "🧘", "bridge": "🌉", "press": "👆", "bench": "🏋️‍♂️",
                "row": "🚣", "deadlift": "🏋️‍♀️", "curl": "💪", "extension": "🦾"
            }
            
            # Try to find a matching icon
            for key, value in exercise_icons.items():
                if key.lower() in exercise.lower():
                    icon_html = f'<span style="margin-right: 0.6rem;">{value}</span>'
                    break
            
            # If no match found, use a generic icon
            if not icon_html:
                icon_html = '<span style="margin-right: 0.6rem;">🏃</span>'
        
        st.markdown(f"""
        <div class="card">
            {image_html}
            <h2 class="card-title">{icon_html}{exercise}</h2>
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
    .loader-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        margin: 2rem auto;
    }
    
    .loader {
        width: 70px;
        height: 70px;
        position: relative;
    }
    
    .loader-text {
        margin-top: 1.5rem;
        color: #5465ff;
        font-size: 1.2rem;
        font-weight: 500;
    }
    
    .loader:before, .loader:after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border: 5px solid transparent;
        border-top-color: #5465ff;
    }
    
    .loader:before {
        z-index: 10;
        animation: spin 1s infinite;
    }
    
    .loader:after {
        border: 5px solid rgba(84, 101, 255, 0.3);
    }
    
    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
    
    .pulse {
        animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    </style>
    
    <div class="loader-container">
        <div class="loader"></div>
        <div class="loader-text pulse">Loading...</div>
    </div>
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
            weight_color = "#2ecc71" if weight_change < 0 else "#e74c3c"  # Green if weight loss, red if weight gain
        else:
            weight_text = "No data"
            weight_icon = "❓"
            weight_color = "#5465ff"
            
        # Format body fat change
        bf_change = stats.get("body_fat_change")
        if bf_change is not None:
            bf_text = f"{bf_change:.1f}%"
            bf_icon = "📉" if bf_change < 0 else "📈"
            bf_color = "#2ecc71" if bf_change < 0 else "#e74c3c"  # Green if fat loss, red if fat gain
        else:
            bf_text = "No data"
            bf_icon = "❓"
            bf_color = "#5465ff"
        
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
            <div class="metric-container" style="flex: 1; border-top: 1px solid #5465ff;">
                <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">📅</div>
                <div class="metric-value">{tracked_days}</div>
                <div class="metric-label">Days Tracked</div>
            </div>
            <div class="metric-container" style="flex: 1; border-top: 1px solid #5465ff;">
                <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">🏋️</div>
                <div class="metric-value">{total_workouts}</div>
                <div class="metric-label">Workouts</div>
            </div>
            <div class="metric-container" style="flex: 1; border-top: 1px solid #5465ff;">
                <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">📊</div>
                <div class="metric-value">{frequency}</div>
                <div class="metric-label">Workouts/Week</div>
            </div>
            <div class="metric-container" style="flex: 1; border-top: 1px solid {weight_color};">
                <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">{weight_icon}</div>
                <div class="metric-value" style="color: {weight_color};">{weight_text}</div>
                <div class="metric-label">Weight Change</div>
            </div>
            <div class="metric-container" style="flex: 1; border-top: 1px solid {bf_color};">
                <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">{bf_icon}</div>
                <div class="metric-value" style="color: {bf_color};">{bf_text}</div>
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
            icon = "✅"
            box_class = "success-box"
            title = "Good Form!"
        else:
            icon = "⚠️"
            box_class = "warning-box"
            title = "Form Needs Improvement"
            
        st.markdown(f"""
        <div class="{box_class}">
            <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                <div style="font-size: 1.5rem; margin-right: 0.8rem;">{icon}</div>
                <h3 style="margin: 0; font-size: 1.3rem;">{title}</h3>
            </div>
            <p style="margin: 0; font-size: 1.05rem; padding-left: 2.3rem;">{feedback}</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error displaying feedback: {e}")
        if is_correct:
            st.success(feedback)
        else:
            st.warning(feedback) 