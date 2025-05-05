import streamlit as st
import os
import sys
import logging

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import utility functions
from src.utils.config_utils import get_app_config, get_mediapipe_config
from src.utils.ui_utils import set_page_config, apply_custom_css, display_header, create_card

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main function to run the Streamlit app
    """
    try:
        # Get app configuration
        app_config = get_app_config()
        
        # Set page configuration
        set_page_config(
            title=app_config.get("title", "AI Health Trainer"),
            icon=app_config.get("icon", "💪"),
            layout=app_config.get("layout", "wide"),
            initial_sidebar_state=app_config.get("initial_sidebar_state", "expanded")
        )
        
        # Apply custom CSS
        apply_custom_css()
        
        # Display header
        display_header(
            title=app_config.get("title", "AI Health Trainer"),
            subtitle=app_config.get("description", "Your personal AI fitness coach")
        )
        
        # Sidebar navigation
        st.sidebar.title("Navigation")
        
        # Page navigation buttons with icons
        if st.sidebar.button("🏋️ Exercise Verification"):
            st.switch_page("pages/exercise_verification.py")
            
        if st.sidebar.button("📏 Body Analysis"):
            st.switch_page("pages/body_analysis.py")
            
        if st.sidebar.button("📋 Exercise Recommendations"):
            st.switch_page("pages/exercise_recommendations.py")
            
        if st.sidebar.button("📈 Progress Tracking"):
            st.switch_page("pages/progress_tracking.py")
        
        if st.sidebar.button("🧮 Health Measurements"):
            st.switch_page("pages/measurements.py")
        
        # Main content - use columns for a better layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Welcome message
            st.markdown("""
            ## Welcome to AI Health Trainer
            
            Your personal AI-powered fitness assistant designed to improve your workout experience and help you reach your fitness goals.
            
            Use the sidebar navigation to access all the powerful features of this application, or explore the feature cards below.
            """)
            
            # Feature cards in a grid
            features = app_config.get("home", {}).get("features", [])
            
            # Create two columns for features
            feature_col1, feature_col2 = st.columns(2)
            
            # Distribute features between columns
            for i, feature in enumerate(features):
                col = feature_col1 if i % 2 == 0 else feature_col2
                with col:
                    create_card(
                        f"{feature.get('icon', '')} {feature.get('title', '')}",
                        feature.get('description', '')
                    )
        
        with col2:
            # Right sidebar with app info
            st.markdown("""
            ### How It Works
            
            1. **Exercise Verification**: Use your webcam to analyze exercise form in real-time
            
            2. **Body Analysis**: Upload photos to measure body metrics and get personalized insights
            
            3. **Exercise Recommendations**: Get custom workout plans based on your body type and goals
            
            4. **Progress Tracking**: Monitor your fitness journey with detailed charts and metrics
            """)
            
            # Sample visualization or image placeholder
            st.markdown("""
            ### Powered By
            
            - **AI Vision Technology**: Advanced pose estimation for accurate form analysis
            - **Machine Learning Models**: Personalized recommendations based on your unique body metrics
            - **Data Analytics**: Track progress over time with detailed visualizations
            """)
        
        # Bottom section - testimonials or additional info
        st.markdown("---")
        st.markdown("### Get Started Now")
        st.markdown("Select any feature from the sidebar to begin your fitness journey with AI-powered guidance.")
            
    except Exception as e:
        logger.error(f"Error in main function: {e}")
        st.error("An error occurred. Please check the logs for details.")

if __name__ == "__main__":
    main() 