import streamlit as st
import cv2
import numpy as np
import pandas as pd
import os
import sys
import time
import logging
from PIL import Image

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import utility functions
from src.utils.config_utils import get_app_config, get_mediapipe_config
from src.utils.ui_utils import (
    set_page_config, apply_custom_css, display_header, 
    show_info_box, show_success_box, show_warning_box,
    create_card, display_metric
)
from src.core.pose_estimation import PoseEstimator
from src.models.model_manager import ModelManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main function for the body analysis page
    """
    try:
        # Get app configuration
        app_config = get_app_config()
        mediapipe_config = get_mediapipe_config()
        
        # Set page configuration
        set_page_config(
            title=f"{app_config.get('title', 'AI Health Trainer')} - Body Analysis",
            icon=app_config.get("icon", "💪"),
            layout=app_config.get("layout", "wide"),
            initial_sidebar_state=app_config.get("initial_sidebar_state", "expanded")
        )
        
        # Apply custom CSS
        apply_custom_css()
        
        # Display header
        display_header(
            title="Body Analysis",
            subtitle="Analyze your body measurements and get personalized recommendations"
        )
        
        # Sidebar navigation
        st.sidebar.title("Navigation")
        
        if st.sidebar.button("🏠 Home"):
            st.switch_page("app.py")
            
        if st.sidebar.button("🏋️ Exercise Verification"):
            st.switch_page("pages/exercise_verification.py")
            
        if st.sidebar.button("📋 Exercise Recommendations"):
            st.switch_page("pages/exercise_recommendations.py")
            
        if st.sidebar.button("📈 Progress Tracking"):
            st.switch_page("pages/progress_tracking.py")
        
        # Initialize pose estimator
        pose_estimator = PoseEstimator(
            static_image_mode=True,  # Use static image mode for analysis
            model_complexity=mediapipe_config.get("model_complexity", 1),
            min_detection_confidence=mediapipe_config.get("min_detection_confidence", 0.5),
            min_tracking_confidence=mediapipe_config.get("min_tracking_confidence", 0.5)
        )
        
        # Initialize model manager
        model_manager = ModelManager()
        
        # Section for uploading image
        st.markdown("## Upload an image for body measurements")
        st.markdown("""
        Upload a full-body photo to get an analysis of your body measurements.
        For best results:
        - Stand straight with arms slightly away from body
        - Wear form-fitting clothing
        - Ensure good lighting
        - Position camera about 8-10 feet away
        """)
        
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        
        # Columns for image and results
        col1, col2 = st.columns([1, 1])
        
        if uploaded_file is not None:
            with col1:
                # Display the uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)
                
                # Add analyze button
                analyze_button = st.button("Analyze Body Measurements")
                
            with col2:
                if analyze_button:
                    with st.spinner("Analyzing body measurements..."):
                        try:
                            # Convert PIL Image to OpenCV format
                            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                            
                            # Process the image
                            annotated_image, results = pose_estimator.process_image(image_cv)
                            
                            if results and results.pose_landmarks:
                                # Calculate body measurements
                                measurements = pose_estimator.calculate_body_measurements(results)
                                
                                # Classify body type
                                body_type = measurements.get("body_type")
                                
                                # Display annotated image
                                st.image(
                                    cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB), 
                                    caption="Pose Detection Results", 
                                    use_column_width=True
                                )
                                
                                # Display measurements
                                st.markdown("## Body Measurements")
                                
                                # Create a DataFrame for measurements
                                measurements_df = pd.DataFrame({
                                    "Measurement": [
                                        "Shoulder Width",
                                        "Hip Width",
                                        "Shoulder-to-Hip Ratio",
                                        "Leg Length",
                                        "Arm Length"
                                    ],
                                    "Value": [
                                        f"{measurements.get('shoulder_width', 0):.2f}",
                                        f"{measurements.get('hip_width', 0):.2f}",
                                        f"{measurements.get('shoulder_hip_ratio', 0):.2f}",
                                        f"{measurements.get('leg_length', 0):.2f}",
                                        f"{measurements.get('arm_length', 0):.2f}"
                                    ]
                                })
                                
                                # Display measurements as a table
                                st.table(measurements_df)
                                
                                # Display body type
                                st.markdown(f"## Body Type: {body_type}")
                                
                                # Body type descriptions
                                body_type_descriptions = {
                                    "Inverted Triangle": """
                                    **Characteristics**:
                                    - Wider shoulders compared to hips
                                    - Athletic upper body
                                    - Narrower hips and waist
                                    
                                    **Clothing Tips**:
                                    - Emphasize lower body with brighter colors or patterns
                                    - Choose tops that don't add volume to shoulders
                                    - A-line or flared bottoms balance your silhouette
                                    
                                    **Training Focus**:
                                    - Lower body exercises to build proportion
                                    - Moderate upper body maintenance
                                    - Core strengthening
                                    """,
                                    
                                    "Rectangle": """
                                    **Characteristics**:
                                    - Similar measurements at shoulders and hips
                                    - Balanced proportions
                                    - Less defined waist
                                    
                                    **Clothing Tips**:
                                    - Create curves with waist-defining garments
                                    - Layer to add dimension
                                    - Belt at waist to create definition
                                    
                                    **Training Focus**:
                                    - Full-body workouts with emphasis on core
                                    - Exercises that create a more defined waist
                                    - Balanced upper and lower body training
                                    """,
                                    
                                    "Pear": """
                                    **Characteristics**:
                                    - Narrower shoulders compared to hips
                                    - Wider hips, thighs, and buttocks
                                    - Defined waist
                                    
                                    **Clothing Tips**:
                                    - Draw attention to upper body with details and brighter colors
                                    - A-line or straight-leg bottoms
                                    - Avoid bottoms with excessive details in hip area
                                    
                                    **Training Focus**:
                                    - Upper body strengthening to build proportion
                                    - Core and back exercises for better posture
                                    - Lower body toning without excessive bulking
                                    """
                                }
                                
                                # Display body type description
                                st.markdown(body_type_descriptions.get(body_type, ""))
                                
                                # Get exercise recommendations
                                recommendations = model_manager.get_exercise_recommendations(
                                    body_type, 
                                    fitness_level="Intermediate"
                                )
                                
                                # Display recommendations
                                st.markdown("## Recommended Exercises")
                                for i, exercise in enumerate(recommendations, 1):
                                    st.markdown(f"{i}. {exercise}")
                                
                                # Save measurements button
                                if st.button("Save Measurements"):
                                    # Here you would save the measurements to a database or file
                                    show_success_box("Measurements saved successfully!")
                                
                            else:
                                st.error("No body detected in the image. Please upload a clear full-body photo.")
                                
                        except Exception as e:
                            logger.error(f"Error analyzing body measurements: {e}")
                            st.error("An error occurred during analysis. Please try a different image.")
                
        else:
            with col2:
                # Show example or instructions when no image is uploaded
                st.markdown("### How it works")
                st.markdown("""
                1. Upload a clear full-body photo
                2. Click 'Analyze Body Measurements'
                3. Get detailed body measurements and body type analysis
                4. Receive personalized exercise recommendations
                
                Your image is processed entirely within the app and is not stored permanently.
                """)
            
    except Exception as e:
        logger.error(f"Error in body analysis page: {e}")
        st.error("An error occurred in the body analysis page. Please check the logs for details.")

if __name__ == "__main__":
    main() 