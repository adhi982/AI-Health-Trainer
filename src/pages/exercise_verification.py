import streamlit as st
import cv2
import numpy as np
import os
import sys
import time
import logging

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import utility functions
from src.utils.config_utils import get_app_config, get_mediapipe_config
from src.utils.ui_utils import (
    set_page_config, apply_custom_css, display_header, 
    show_info_box, show_success_box, show_warning_box, 
    display_feedback
)
from src.core.pose_estimation import PoseEstimator
from src.models.model_manager import ModelManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main function for the exercise verification page
    """
    try:
        # Get app configuration
        app_config = get_app_config()
        mediapipe_config = get_mediapipe_config()
        
        # Set page configuration
        set_page_config(
            title=f"{app_config.get('title', 'AI Health Trainer')} - Exercise Verification",
            icon=app_config.get("icon", "💪"),
            layout=app_config.get("layout", "wide"),
            initial_sidebar_state=app_config.get("initial_sidebar_state", "expanded")
        )
        
        # Apply custom CSS
        apply_custom_css()
        
        # Display header
        display_header(
            title="Exercise Verification",
            subtitle="Analyze your exercise form in real-time using AI"
        )
        
        # Sidebar navigation
        st.sidebar.title("Navigation")
        
        if st.sidebar.button("🏠 Home"):
            st.switch_page("app.py")
            
        if st.sidebar.button("📏 Body Analysis"):
            st.switch_page("pages/body_analysis.py")
            
        if st.sidebar.button("📋 Exercise Recommendations"):
            st.switch_page("pages/exercise_recommendations.py")
            
        if st.sidebar.button("📈 Progress Tracking"):
            st.switch_page("pages/progress_tracking.py")
        
        # Exercise selection
        st.sidebar.title("Exercise Settings")
        exercise_type = st.sidebar.selectbox(
            "Select Exercise Type",
            ["Push-up", "Squat", "Plank", "Lunge"]
        )
        
        # Exercise descriptions
        exercise_descriptions = {
            "Push-up": """
            **Target Muscles**: Chest, shoulders, triceps, core
            
            **Proper Form**:
            - Start in a plank position with hands slightly wider than shoulder-width
            - Lower your body until your chest nearly touches the floor
            - Keep your elbows close to your body at about a 45-degree angle
            - Maintain a straight line from head to heels
            - Push back up to the starting position
            """,
            
            "Squat": """
            **Target Muscles**: Quadriceps, hamstrings, glutes, core
            
            **Proper Form**:
            - Stand with feet shoulder-width apart
            - Keep your chest up and back straight
            - Lower your body as if sitting in a chair
            - Keep knees in line with toes (don't let them collapse inward)
            - Lower until thighs are parallel to the ground
            - Push through your heels to return to standing
            """,
            
            "Plank": """
            **Target Muscles**: Core, shoulders, back, glutes
            
            **Proper Form**:
            - Start in a forearm plank position with elbows under shoulders
            - Keep your body in a straight line from head to heels
            - Engage your core and glutes
            - Keep your neck neutral (don't drop or lift your head)
            - Hold the position steady without sagging or raising your hips
            """,
            
            "Lunge": """
            **Target Muscles**: Quadriceps, hamstrings, glutes, calves
            
            **Proper Form**:
            - Stand with feet hip-width apart
            - Take a big step forward with one leg
            - Lower your body until both knees are bent at about 90 degrees
            - Front knee should be directly above your ankle, not pushed forward
            - Keep your torso upright
            - Push through your front heel to return to starting position
            """
        }
        
        # Show exercise description
        st.markdown(f"## {exercise_type}")
        st.markdown(exercise_descriptions[exercise_type])
        
        # Initialize pose estimator
        pose_estimator = PoseEstimator(
            static_image_mode=mediapipe_config.get("static_image_mode", False),
            model_complexity=mediapipe_config.get("model_complexity", 1),
            min_detection_confidence=mediapipe_config.get("min_detection_confidence", 0.5),
            min_tracking_confidence=mediapipe_config.get("min_tracking_confidence", 0.5)
        )
        
        # Initialize model manager
        model_manager = ModelManager()
        
        # Webcam preview placeholder
        preview_col, feedback_col = st.columns([3, 1])
        with preview_col:
            video_placeholder = st.empty()
        
        # Feedback placeholder
        with feedback_col:
            feedback_placeholder = st.empty()
            feedback_placeholder.markdown("""
            ### Form Feedback
            Start the verification to get real-time feedback on your exercise form.
            """)
            
            metrics_placeholder = st.empty()
        
        # Control buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            start_button = st.button("Start Verification", key="start_verification")
        with col2:
            stop_button = st.button("Stop", key="stop_verification")
        with col3:
            save_button = st.button("Save Results", key="save_results", disabled=True)
        
        # Store feedback in session state
        if "last_feedback" not in st.session_state:
            st.session_state.last_feedback = {"correct": False, "feedback": "", "metrics": {}}
        
        # Start verification if button is clicked
        if start_button:
            # Set session state to running
            st.session_state.verification_running = True
            
            # Start webcam
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                st.error("Failed to access webcam. Please make sure your webcam is connected and accessible.")
                return
            
            # Process frames from webcam
            while st.session_state.get("verification_running", True):
                # Read frame from webcam
                ret, frame = cap.read()
                
                if not ret:
                    st.error("Failed to read from webcam")
                    break
                
                # Process the frame
                annotated_image, results = pose_estimator.process_image(frame)
                
                # Analyze exercise form
                if results and results.pose_landmarks:
                    form_analysis = pose_estimator.analyze_exercise_form(results, exercise_type)
                    
                    # Update feedback
                    st.session_state.last_feedback = form_analysis
                    
                    # Display feedback
                    feedback_placeholder.empty()
                    with feedback_placeholder.container():
                        st.markdown("### Form Feedback")
                        display_feedback(form_analysis["feedback"], form_analysis["correct"])
                    
                    # Display metrics
                    metrics_placeholder.empty()
                    with metrics_placeholder.container():
                        st.markdown("### Metrics")
                        metrics = form_analysis.get("metrics", {})
                        for metric, value in metrics.items():
                            if isinstance(value, bool):
                                status = "✅" if value else "❌"
                                st.markdown(f"**{metric.replace('_', ' ').title()}**: {status}")
                            elif isinstance(value, (int, float)):
                                st.markdown(f"**{metric.replace('_', ' ').title()}**: {value:.1f}°")
                            else:
                                st.markdown(f"**{metric.replace('_', ' ').title()}**: {value}")
                
                # Display the annotated image
                video_placeholder.image(
                    annotated_image, 
                    channels="BGR",
                    use_column_width=True,
                    caption=f"Live {exercise_type} Analysis"
                )
                
                # Check if stop button was pressed
                if stop_button or not st.session_state.get("verification_running", True):
                    break
                
                # Short sleep to reduce CPU usage
                time.sleep(0.03)
            
            # Release webcam
            cap.release()
            
            # Enable save button
            save_button = st.button("Save Results", key="save_results_enabled")
        
        # Stop verification if button is clicked
        if stop_button:
            st.session_state.verification_running = False
            st.info("Verification stopped. You can save your results or start again.")
        
        # Save results if button is clicked
        if save_button:
            # Here you would save the results to a database or file
            show_success_box("Results saved successfully! You can view your progress in the Progress Tracking page.")
            
            # Disable the save button after saving
            st.session_state.save_button_clicked = True
        
    except Exception as e:
        logger.error(f"Error in exercise verification page: {e}")
        st.error("An error occurred during exercise verification. Please check the logs for details.")

if __name__ == "__main__":
    main() 