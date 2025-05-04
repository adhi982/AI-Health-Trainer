import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import logging

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import utility functions
from src.utils.config_utils import get_app_config
from src.utils.ui_utils import (
    set_page_config, apply_custom_css, display_header, 
    show_info_box, show_success_box, 
    create_card, display_exercise_card
)
from src.models.model_manager import ModelManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main function for the exercise recommendations page
    """
    try:
        # Get app configuration
        app_config = get_app_config()
        
        # Set page configuration
        set_page_config(
            title=f"{app_config.get('title', 'AI Health Trainer')} - Exercise Recommendations",
            icon=app_config.get("icon", "💪"),
            layout=app_config.get("layout", "wide"),
            initial_sidebar_state=app_config.get("initial_sidebar_state", "expanded")
        )
        
        # Apply custom CSS
        apply_custom_css()
        
        # Display header
        display_header(
            title="Exercise Recommendations",
            subtitle="Get personalized workout recommendations based on your goals and body type"
        )
        
        # Display upcoming feature notification
        st.warning("🚧 **UPCOMING FEATURE** 🚧 - The AI model for personalized exercise recommendations is currently in development. This page shows a preview of the interface with sample data.")
        
        # Sidebar navigation
        st.sidebar.title("Navigation")
        
        if st.sidebar.button("🏠 Home"):
            st.switch_page("app.py")
            
        if st.sidebar.button("🏋️ Exercise Verification"):
            st.switch_page("pages/exercise_verification.py")
            
        if st.sidebar.button("📏 Body Analysis"):
            st.switch_page("pages/body_analysis.py")
            
        if st.sidebar.button("📈 Progress Tracking"):
            st.switch_page("pages/progress_tracking.py")
        
        # Initialize model manager
        model_manager = ModelManager()
        
        # Sidebar filters
        st.sidebar.title("Customize Recommendations")
        
        # Body type selection
        body_type = st.sidebar.selectbox(
            "Body Type",
            ["Inverted Triangle", "Rectangle", "Pear"]
        )
        
        # Fitness level selection
        fitness_level = st.sidebar.selectbox(
            "Fitness Level",
            ["Beginner", "Intermediate", "Advanced"]
        )
        
        # Goals selection (multi-select)
        goals = st.sidebar.multiselect(
            "Fitness Goals",
            ["Weight Loss", "Muscle Gain", "Endurance", "Flexibility", "Strength"],
            default=["Weight Loss", "Muscle Gain"]
        )
        
        # Equipment availability
        available_equipment = st.sidebar.multiselect(
            "Available Equipment",
            ["None", "Dumbbells", "Resistance Bands", "Kettlebells", "Pull-up Bar", "Bench"],
            default=["Dumbbells", "Resistance Bands"]
        )
        
        # Workout duration
        workout_duration = st.sidebar.slider(
            "Workout Duration (minutes)",
            min_value=15,
            max_value=90,
            value=45,
            step=15
        )
        
        # Workouts per week
        workouts_per_week = st.sidebar.slider(
            "Workouts per Week",
            min_value=1,
            max_value=7,
            value=3,
            step=1
        )
        
        # Main content
        st.markdown("## Your Personalized Workout Plan")
        
        # Get recommendations based on body type and fitness level
        recommended_exercises = model_manager.get_exercise_recommendations(body_type, fitness_level)
        
        # Additional exercise details (mock data)
        exercise_details = {
            "Push-ups": {
                "description": """
                A compound exercise that works the chest, shoulders, triceps, and core.
                
                **How to do it**:
                1. Start in a plank position with hands slightly wider than shoulder-width
                2. Lower your body until your chest nearly touches the floor
                3. Push back up to the starting position
                4. Repeat for the recommended number of repetitions
                
                **Sets/Reps**: 3 sets of 8-12 reps
                **Rest**: 60-90 seconds between sets
                """,
                "muscles": ["Chest", "Shoulders", "Triceps", "Core"],
                "difficulty": "Beginner-Intermediate"
            },
            "Squats": {
                "description": """
                A fundamental lower body exercise that targets quadriceps, hamstrings, and glutes.
                
                **How to do it**:
                1. Stand with feet shoulder-width apart
                2. Lower your body by bending your knees and hips
                3. Keep your chest up and back straight
                4. Lower until thighs are parallel to the ground
                5. Push through your heels to return to standing
                
                **Sets/Reps**: 3-4 sets of 10-15 reps
                **Rest**: 60-90 seconds between sets
                """,
                "muscles": ["Quadriceps", "Hamstrings", "Glutes", "Core"],
                "difficulty": "Beginner-Intermediate"
            },
            "Deadlifts": {
                "description": """
                A powerful compound exercise that targets multiple major muscle groups.
                
                **How to do it**:
                1. Stand with feet hip-width apart, barbell over midfoot
                2. Bend at hips and knees to grasp the bar
                3. Keep your back flat and core engaged
                4. Stand up by driving through your heels
                5. Lower the bar by hinging at the hips
                
                **Sets/Reps**: 3-4 sets of 6-10 reps
                **Rest**: 2-3 minutes between sets
                """,
                "muscles": ["Lower Back", "Glutes", "Hamstrings", "Traps", "Forearms"],
                "difficulty": "Intermediate-Advanced"
            },
            "Lunges": {
                "description": """
                An excellent exercise for lower body strength and balance.
                
                **How to do it**:
                1. Stand with feet hip-width apart
                2. Take a step forward with one leg
                3. Lower your body until both knees form 90-degree angles
                4. Push back to starting position
                5. Repeat with the other leg
                
                **Sets/Reps**: 3 sets of 10-12 reps per leg
                **Rest**: 60 seconds between sets
                """,
                "muscles": ["Quadriceps", "Hamstrings", "Glutes", "Calves"],
                "difficulty": "Beginner-Intermediate"
            },
            "Plank": {
                "description": """
                A static core exercise that builds stability and strength.
                
                **How to do it**:
                1. Start in a forearm plank position
                2. Rest on your forearms with elbows under shoulders
                3. Create a straight line from head to heels
                4. Engage your core and hold the position
                
                **Sets/Duration**: 3 sets of 30-60 seconds
                **Rest**: 30-60 seconds between sets
                """,
                "muscles": ["Core", "Shoulders", "Back", "Glutes"],
                "difficulty": "Beginner"
            },
            "Pull-ups": {
                "description": """
                A challenging upper body exercise that builds strength and definition.
                
                **How to do it**:
                1. Hang from a pull-up bar with hands shoulder-width apart
                2. Pull your body up until your chin is over the bar
                3. Lower with control to starting position
                
                **Sets/Reps**: 3-4 sets of 5-10 reps
                **Rest**: 90-120 seconds between sets
                """,
                "muscles": ["Back", "Biceps", "Shoulders", "Core"],
                "difficulty": "Intermediate-Advanced"
            },
            "Shoulder Press": {
                "description": """
                An effective exercise for building shoulder strength and muscle.
                
                **How to do it**:
                1. Sit or stand with dumbbells at shoulder height
                2. Press the weights overhead until arms are fully extended
                3. Lower back to starting position with control
                
                **Sets/Reps**: 3 sets of 8-12 reps
                **Rest**: 60-90 seconds between sets
                """,
                "muscles": ["Shoulders", "Triceps", "Upper Back"],
                "difficulty": "Beginner-Intermediate"
            },
            "Bench Press": {
                "description": """
                A classic chest exercise for building upper body strength.
                
                **How to do it**:
                1. Lie on a bench with feet on the floor
                2. Grip the bar with hands wider than shoulder-width
                3. Lower the bar to your chest
                4. Press back up to starting position
                
                **Sets/Reps**: 3-4 sets of 8-12 reps
                **Rest**: 90-120 seconds between sets
                """,
                "muscles": ["Chest", "Shoulders", "Triceps"],
                "difficulty": "Intermediate"
            },
            "Rows": {
                "description": """
                An excellent exercise for building back strength and improving posture.
                
                **How to do it**:
                1. Bend at the hips with a flat back
                2. Hold dumbbells with arms extended
                3. Pull the weights to your ribcage
                4. Lower with control
                
                **Sets/Reps**: 3 sets of 10-15 reps
                **Rest**: 60-90 seconds between sets
                """,
                "muscles": ["Back", "Biceps", "Shoulders", "Core"],
                "difficulty": "Beginner-Intermediate"
            },
            "Glute Bridges": {
                "description": """
                A targeted exercise for glute activation and strength.
                
                **How to do it**:
                1. Lie on your back with knees bent and feet flat
                2. Drive through your heels to lift hips toward ceiling
                3. Squeeze glutes at the top
                4. Lower with control
                
                **Sets/Reps**: 3 sets of 15-20 reps
                **Rest**: 30-60 seconds between sets
                """,
                "muscles": ["Glutes", "Hamstrings", "Lower Back"],
                "difficulty": "Beginner"
            }
        }
        
        # Create workout plan
        if st.button("Generate Workout Plan"):
            with st.spinner("Creating your personalized workout plan..."):
                # Select exercises based on body type, fitness level, and goals
                available_exercises = [ex for ex in recommended_exercises if ex in exercise_details]
                
                # If not enough exercises available, add some generic ones
                generic_exercises = ["Push-ups", "Squats", "Lunges", "Plank"]
                for ex in generic_exercises:
                    if ex not in available_exercises and len(available_exercises) < 6:
                        available_exercises.append(ex)
                
                # Create workout schedule
                workout_schedule = {}
                
                if workouts_per_week == 1:
                    # Full body workout
                    workout_schedule["Day 1 - Full Body"] = available_exercises[:6]
                elif workouts_per_week == 2:
                    # Upper/Lower split
                    upper_body = [ex for ex in available_exercises if any(m in ["Chest", "Back", "Shoulders", "Arms", "Triceps", "Biceps"] 
                                                                 for m in exercise_details.get(ex, {}).get("muscles", []))]
                    lower_body = [ex for ex in available_exercises if any(m in ["Quadriceps", "Hamstrings", "Glutes", "Calves"] 
                                                                 for m in exercise_details.get(ex, {}).get("muscles", []))]
                    
                    workout_schedule["Day 1 - Upper Body"] = upper_body[:4]
                    workout_schedule["Day 2 - Lower Body"] = lower_body[:4]
                elif workouts_per_week == 3:
                    # Push/Pull/Legs split
                    push = [ex for ex in available_exercises if any(m in ["Chest", "Shoulders", "Triceps"] 
                                                           for m in exercise_details.get(ex, {}).get("muscles", []))]
                    pull = [ex for ex in available_exercises if any(m in ["Back", "Biceps", "Forearms"] 
                                                           for m in exercise_details.get(ex, {}).get("muscles", []))]
                    legs = [ex for ex in available_exercises if any(m in ["Quadriceps", "Hamstrings", "Glutes", "Calves"] 
                                                           for m in exercise_details.get(ex, {}).get("muscles", []))]
                    
                    workout_schedule["Day 1 - Push"] = push[:3]
                    workout_schedule["Day 2 - Pull"] = pull[:3]
                    workout_schedule["Day 3 - Legs"] = legs[:3]
                else:
                    # 4+ day split (more specialized)
                    chest = [ex for ex in available_exercises if "Chest" in exercise_details.get(ex, {}).get("muscles", [])]
                    back = [ex for ex in available_exercises if "Back" in exercise_details.get(ex, {}).get("muscles", [])]
                    shoulders = [ex for ex in available_exercises if "Shoulders" in exercise_details.get(ex, {}).get("muscles", [])]
                    legs = [ex for ex in available_exercises if any(m in ["Quadriceps", "Hamstrings", "Glutes", "Calves"] 
                                                           for m in exercise_details.get(ex, {}).get("muscles", []))]
                    core = [ex for ex in available_exercises if "Core" in exercise_details.get(ex, {}).get("muscles", [])]
                    
                    workout_schedule["Day 1 - Chest & Triceps"] = chest[:2] + ["Push-ups"]
                    workout_schedule["Day 2 - Back & Biceps"] = back[:2] + ["Pull-ups"]
                    workout_schedule["Day 3 - Legs"] = legs[:3]
                    workout_schedule["Day 4 - Shoulders & Core"] = shoulders[:2] + core[:2]
                
                # Display workout schedule
                st.markdown("### Your Weekly Workout Schedule")
                
                for day, exercises in workout_schedule.items():
                    st.markdown(f"#### {day}")
                    st.markdown(f"Duration: {workout_duration} minutes")
                    
                    # Create table for exercises
                    exercise_df = pd.DataFrame({
                        "Exercise": exercises,
                        "Sets/Reps": [exercise_details.get(ex, {}).get("description", "").split("**Sets/Reps**: ")[1].split("\n")[0] 
                                     if "**Sets/Reps**: " in exercise_details.get(ex, {}).get("description", "") else "3 sets of 10-12 reps" for ex in exercises],
                        "Rest": [exercise_details.get(ex, {}).get("description", "").split("**Rest**: ")[1].split("\n")[0] 
                                if "**Rest**: " in exercise_details.get(ex, {}).get("description", "") else "60 seconds" for ex in exercises]
                    })
                    
                    st.table(exercise_df)
                
                # Display detailed exercise descriptions
                st.markdown("### Exercise Descriptions")
                
                all_exercises = []
                for exercises in workout_schedule.values():
                    all_exercises.extend(exercises)
                
                # Remove duplicates while preserving order
                all_exercises = list(dict.fromkeys(all_exercises))
                
                # Display exercise cards
                cols = st.columns(2)
                for i, exercise in enumerate(all_exercises):
                    col_idx = i % 2
                    with cols[col_idx]:
                        if exercise in exercise_details:
                            details = exercise_details[exercise]
                            # Use native Streamlit components instead of HTML
                            st.subheader(exercise)
                            st.markdown(f"**Difficulty:** {details.get('difficulty', 'Intermediate')}")
                            st.markdown(f"**Target Muscles:** {', '.join(details.get('muscles', []))}")
                            st.markdown(details.get('description', ''))
                            st.markdown("---") # Add a separator between exercises
                
                # Save button
                if st.button("Save Workout Plan"):
                    show_success_box("Workout plan saved successfully!")
    except Exception as e:
        logger.error(f"Error in exercise recommendations page: {e}")
        st.error("An error occurred in the exercise recommendations page. Please check the logs for details.")

if __name__ == "__main__":
    main() 