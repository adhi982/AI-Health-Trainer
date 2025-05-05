import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import datetime
import logging
import plotly.express as px
import plotly.graph_objects as go

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import utility functions
from src.utils.config_utils import get_app_config
from src.utils.ui_utils import (
    set_page_config, apply_custom_css, display_header, 
    show_info_box, show_success_box, show_warning_box,
    display_progress_summary
)
from src.utils.progress_tracker import ProgressTracker

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main function for the progress tracking page
    """
    try:
        # Get app configuration
        app_config = get_app_config()
        
        # Set page configuration
        set_page_config(
            title=f"{app_config.get('title', 'AI Health Trainer')} - Progress Tracking",
            icon=app_config.get("icon", "💪"),
            layout=app_config.get("layout", "wide"),
            initial_sidebar_state=app_config.get("initial_sidebar_state", "expanded")
        )
        
        # Apply custom CSS
        apply_custom_css()
        
        # Display header
        display_header(
            title="Progress Tracking",
            subtitle="Track your fitness journey and visualize your progress"
        )
        
        # Sidebar navigation
        st.sidebar.title("Navigation")
        
        if st.sidebar.button("🏠 Home"):
            st.switch_page("app.py")
            
        if st.sidebar.button("🏋️ Exercise Verification"):
            st.switch_page("pages/exercise_verification.py")
            
        if st.sidebar.button("📏 Body Analysis"):
            st.switch_page("pages/body_analysis.py")
            
        if st.sidebar.button("📋 Exercise Recommendations"):
            st.switch_page("pages/exercise_recommendations.py")
        
        if st.sidebar.button("🧮 Health Measurements"):
            st.switch_page("pages/measurements.py")
        
        # Initialize progress tracker
        progress_tracker = ProgressTracker(data_dir="data")
        
        # Sidebar options
        st.sidebar.title("Options")
        
        # Time period selection
        time_period = st.sidebar.selectbox(
            "Time Period",
            ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Last Year", "All Time"],
            index=1
        )
        
        # Convert time period to days
        time_periods = {
            "Last 7 Days": 7,
            "Last 30 Days": 30,
            "Last 90 Days": 90,
            "Last Year": 365,
            "All Time": 9999
        }
        days = time_periods[time_period]
        
        # Get statistics
        stats = progress_tracker.get_statistics()
        
        # Display tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Add Entry", "Weight & Body Fat", "Exercise Progress"])
        
        with tab1:
            st.markdown("## Progress Summary")
            
            # Display summary metrics
            display_progress_summary(stats)
            
            # Show most recent entries
            st.markdown("### Recent Entries")
            recent_data = progress_tracker.progress_data.sort_values("date", ascending=False).head(5)
            
            if len(recent_data) > 0:
                # Format the data for display
                display_data = recent_data.copy()
                display_data["date"] = display_data["date"].dt.strftime("%Y-%m-%d")
                display_data = display_data.fillna("-")
                
                # Display the data
                st.dataframe(
                    display_data[["date", "weight", "body_fat", "exercise", "sets", "reps", "notes"]],
                    use_container_width=True
                )
            else:
                st.info("No entries yet. Add your first entry in the 'Add Entry' tab.")
        
        with tab2:
            st.markdown("## Add New Entry")
            
            # Create a form for data entry
            with st.form("progress_form"):
                # Date selector (default to today)
                entry_date = st.date_input(
                    "Date",
                    value=datetime.date.today(),
                    max_value=datetime.date.today()
                )
                
                # Create 3 columns for form fields
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Weight entry
                    weight = st.number_input("Weight (kg)", min_value=0.0, max_value=500.0, step=0.1)
                    
                    # Body fat entry
                    body_fat = st.number_input("Body Fat (%)", min_value=0.0, max_value=100.0, step=0.1)
                
                with col2:
                    # Exercise selection
                    exercise = st.text_input("Exercise")
                    
                    # Sets and reps
                    sets = st.number_input("Sets", min_value=0, max_value=100, step=1)
                    reps = st.number_input("Reps", min_value=0, max_value=1000, step=1)
                
                with col3:
                    # Notes
                    notes = st.text_area("Notes", height=132)
                
                # Submit button
                submitted = st.form_submit_button("Save Entry")
                
                if submitted:
                    # Convert to float/int/None
                    weight_val = float(weight) if weight > 0 else None
                    body_fat_val = float(body_fat) if body_fat > 0 else None
                    exercise_val = exercise if exercise else None
                    sets_val = int(sets) if sets > 0 else None
                    reps_val = int(reps) if reps > 0 else None
                    notes_val = notes if notes else None
                    
                    # Add entry
                    success = progress_tracker.add_progress_entry(
                        date=entry_date.strftime("%Y-%m-%d"),
                        weight=weight_val,
                        body_fat=body_fat_val,
                        exercise=exercise_val,
                        sets=sets_val,
                        reps=reps_val,
                        notes=notes_val
                    )
                    
                    if success:
                        show_success_box("Entry added successfully!")
                    else:
                        show_warning_box("Failed to add entry. Please try again.")
            
            # Add a separator
            st.markdown("---")
            
            # Add data import/export options
            st.markdown("## Import/Export Data")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Export button
                if st.button("Export Data (CSV)"):
                    # Get CSV data
                    csv_data = progress_tracker.progress_data.to_csv(index=False)
                    
                    # Create download link
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name="fitness_progress.csv",
                        mime="text/csv"
                    )
            
            with col2:
                # Import functionality
                uploaded_file = st.file_uploader("Import CSV data", type=["csv"])
                
                if uploaded_file is not None:
                    try:
                        # Read CSV
                        imported_data = pd.read_csv(uploaded_file)
                        
                        # Check if data has required columns
                        required_columns = ["date", "weight", "body_fat", "exercise", "sets", "reps"]
                        if all(col in imported_data.columns for col in required_columns):
                            # Convert date column to datetime
                            imported_data["date"] = pd.to_datetime(imported_data["date"])
                            
                            # Replace progress data
                            progress_tracker.progress_data = imported_data
                            
                            # Save data
                            progress_tracker._save_progress_data()
                            
                            show_success_box("Data imported successfully!")
                        else:
                            show_warning_box("Invalid CSV format. CSV must include these columns: date, weight, body_fat, exercise, sets, reps")
                    except Exception as e:
                        logger.error(f"Error importing data: {e}")
                        show_warning_box("Error importing data. Please check the file format.")
        
        with tab3:
            st.markdown("## Weight & Body Fat Tracking")
            
            # Weight chart
            st.markdown("### Weight Progress")
            weight_chart = progress_tracker.create_weight_chart(days)
            st.plotly_chart(weight_chart, use_container_width=True)
            
            # Body fat chart
            st.markdown("### Body Fat Progress")
            body_fat_chart = progress_tracker.create_body_fat_chart(days)
            st.plotly_chart(body_fat_chart, use_container_width=True)
        
        with tab4:
            st.markdown("## Exercise Progress")
            
            # Get available exercises
            available_exercises = progress_tracker.get_available_exercises()
            
            if not available_exercises:
                st.info("No exercise data available. Add exercise entries to track your progress.")
            else:
                # Exercise selection
                selected_exercise = st.selectbox(
                    "Select Exercise to Track",
                    available_exercises
                )
                
                # Exercise chart
                st.markdown(f"### {selected_exercise} Progress")
                exercise_chart = progress_tracker.create_exercise_chart(selected_exercise, days)
                st.plotly_chart(exercise_chart, use_container_width=True)
                
                # Exercise data table
                st.markdown("### Exercise Details")
                exercise_data = progress_tracker.get_exercise_progress(selected_exercise, days)
                
                if len(exercise_data) > 0:
                    # Format the data for display
                    display_data = exercise_data.copy()
                    display_data["date"] = display_data["date"].dt.strftime("%Y-%m-%d")
                    display_data["volume"] = display_data["sets"] * display_data["reps"]
                    
                    # Display the data
                    st.dataframe(
                        display_data[["date", "sets", "reps", "volume"]],
                        use_container_width=True
                    )
                else:
                    st.info(f"No data available for {selected_exercise} in the selected time period.")
        
        # Add option to clear data (for testing purposes)
        if st.sidebar.checkbox("Show Advanced Options"):
            st.sidebar.warning("These options are for advanced users only.")
            
            if st.sidebar.button("Clear All Data"):
                confirm = st.sidebar.checkbox("I understand this will delete all progress data")
                
                if confirm and st.sidebar.button("Confirm Clear Data"):
                    success = progress_tracker.clear_progress_data()
                    
                    if success:
                        st.sidebar.success("All progress data cleared successfully!")
                    else:
                        st.sidebar.error("Failed to clear data. Please try again.")
            
    except Exception as e:
        logger.error(f"Error in progress tracking page: {e}")
        st.error("An error occurred in the progress tracking page. Please check the logs for details.")

if __name__ == "__main__":
    main() 