import pandas as pd
import numpy as np
import os
import json
import logging
import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
import plotly.express as px
import plotly.graph_objects as go

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProgressTracker:
    """
    Class for tracking user fitness progress
    """
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the progress tracker
        
        Args:
            data_dir: Directory for storing progress data
        """
        self.data_dir = data_dir
        self.progress_file = os.path.join(data_dir, "progress_data.csv")
        self.progress_data = self._load_progress_data()
        
    def _load_progress_data(self) -> pd.DataFrame:
        """
        Load progress data from CSV file
        
        Returns:
            DataFrame containing progress data
        """
        try:
            if os.path.exists(self.progress_file):
                data = pd.read_csv(self.progress_file)
                # Convert date column to datetime
                data["date"] = pd.to_datetime(data["date"])
                logger.info(f"Loaded progress data with {len(data)} records")
                return data
            else:
                logger.info("No progress data file found, creating new DataFrame")
                return pd.DataFrame(columns=["date", "weight", "body_fat", "exercise", "sets", "reps", "notes"])
        except Exception as e:
            logger.error(f"Error loading progress data: {e}")
            return pd.DataFrame(columns=["date", "weight", "body_fat", "exercise", "sets", "reps", "notes"])
    
    def add_progress_entry(self, 
                           date: str,
                           weight: Optional[float] = None,
                           body_fat: Optional[float] = None,
                           exercise: Optional[str] = None,
                           sets: Optional[int] = None,
                           reps: Optional[int] = None,
                           notes: Optional[str] = None) -> bool:
        """
        Add a new progress entry
        
        Args:
            date: Date of the progress entry (YYYY-MM-DD)
            weight: Weight in kg
            body_fat: Body fat percentage
            exercise: Exercise name
            sets: Number of sets
            reps: Number of reps
            notes: Additional notes
            
        Returns:
            True if entry was added successfully, False otherwise
        """
        try:
            # Convert date string to datetime
            entry_date = pd.to_datetime(date)
            
            # Create new entry
            new_entry = {
                "date": entry_date,
                "weight": weight,
                "body_fat": body_fat,
                "exercise": exercise,
                "sets": sets,
                "reps": reps,
                "notes": notes
            }
            
            # Add entry to DataFrame
            self.progress_data = pd.concat([self.progress_data, pd.DataFrame([new_entry])], ignore_index=True)
            
            # Save updated data
            self._save_progress_data()
            
            logger.info(f"Added new progress entry for {date}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding progress entry: {e}")
            return False
    
    def get_progress_history(self, metric: str = "weight", days: int = 30) -> pd.DataFrame:
        """
        Get progress history for a specific metric
        
        Args:
            metric: Metric to track (weight, body_fat, etc.)
            days: Number of days to include in history
            
        Returns:
            DataFrame containing progress history
        """
        try:
            # Filter data for the specified metric and time period
            if metric not in self.progress_data.columns:
                logger.warning(f"Metric {metric} not found in progress data")
                return pd.DataFrame()
            
            # Calculate cutoff date
            cutoff_date = pd.Timestamp.now() - pd.Timedelta(days=days)
            
            # Filter data
            filtered_data = self.progress_data[self.progress_data["date"] >= cutoff_date].copy()
            
            # Sort by date
            filtered_data = filtered_data.sort_values("date")
            
            # Filter for non-null values of the metric
            filtered_data = filtered_data[filtered_data[metric].notna()]
            
            return filtered_data[["date", metric]]
            
        except Exception as e:
            logger.error(f"Error getting progress history: {e}")
            return pd.DataFrame()
    
    def get_exercise_progress(self, exercise: str, days: int = 30) -> pd.DataFrame:
        """
        Get progress for a specific exercise
        
        Args:
            exercise: Exercise name
            days: Number of days to include in history
            
        Returns:
            DataFrame containing exercise progress
        """
        try:
            # Calculate cutoff date
            cutoff_date = pd.Timestamp.now() - pd.Timedelta(days=days)
            
            # Filter data
            filtered_data = self.progress_data[
                (self.progress_data["date"] >= cutoff_date) & 
                (self.progress_data["exercise"] == exercise)
            ].copy()
            
            # Sort by date
            filtered_data = filtered_data.sort_values("date")
            
            return filtered_data[["date", "exercise", "sets", "reps"]]
            
        except Exception as e:
            logger.error(f"Error getting exercise progress: {e}")
            return pd.DataFrame()
    
    def create_weight_chart(self, days: int = 30) -> go.Figure:
        """
        Create a chart for weight progress
        
        Args:
            days: Number of days to include in chart
            
        Returns:
            Plotly Figure object
        """
        weight_data = self.get_progress_history("weight", days)
        
        if len(weight_data) == 0:
            # Create empty chart with message
            fig = go.Figure()
            fig.add_annotation(
                text="No weight data available for the selected time period",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Create line chart
        fig = px.line(
            weight_data, 
            x="date", 
            y="weight",
            markers=True,
            title=f"Weight Progress (Last {days} Days)",
            labels={"weight": "Weight (kg)", "date": "Date"}
        )
        
        # Customize layout
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Weight (kg)",
            hovermode="x unified"
        )
        
        return fig
    
    def create_body_fat_chart(self, days: int = 30) -> go.Figure:
        """
        Create a chart for body fat progress
        
        Args:
            days: Number of days to include in chart
            
        Returns:
            Plotly Figure object
        """
        body_fat_data = self.get_progress_history("body_fat", days)
        
        if len(body_fat_data) == 0:
            # Create empty chart with message
            fig = go.Figure()
            fig.add_annotation(
                text="No body fat data available for the selected time period",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Create line chart
        fig = px.line(
            body_fat_data, 
            x="date", 
            y="body_fat",
            markers=True,
            title=f"Body Fat Progress (Last {days} Days)",
            labels={"body_fat": "Body Fat (%)", "date": "Date"}
        )
        
        # Customize layout
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Body Fat (%)",
            hovermode="x unified"
        )
        
        return fig
    
    def create_exercise_chart(self, exercise: str, days: int = 30) -> go.Figure:
        """
        Create a chart for exercise progress
        
        Args:
            exercise: Exercise name
            days: Number of days to include in chart
            
        Returns:
            Plotly Figure object
        """
        exercise_data = self.get_exercise_progress(exercise, days)
        
        if len(exercise_data) == 0:
            # Create empty chart with message
            fig = go.Figure()
            fig.add_annotation(
                text=f"No data available for {exercise} in the selected time period",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Calculate volume (sets * reps)
        exercise_data["volume"] = exercise_data["sets"] * exercise_data["reps"]
        
        # Create bar chart
        fig = px.bar(
            exercise_data, 
            x="date", 
            y="volume",
            title=f"{exercise} Progress (Last {days} Days)",
            labels={"volume": "Volume (sets × reps)", "date": "Date"}
        )
        
        # Customize layout
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Volume (sets × reps)",
            hovermode="x unified"
        )
        
        return fig
    
    def get_available_exercises(self) -> List[str]:
        """
        Get list of exercises with tracking data
        
        Returns:
            List of exercise names
        """
        if len(self.progress_data) == 0 or "exercise" not in self.progress_data.columns:
            return []
        
        exercises = self.progress_data["exercise"].dropna().unique().tolist()
        return sorted(exercises)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get summary statistics for progress data
        
        Returns:
            Dictionary containing summary statistics
        """
        stats = {}
        
        if len(self.progress_data) == 0:
            return {
                "total_records": 0,
                "start_date": None,
                "end_date": None,
                "tracked_days": 0,
                "weight_change": None,
                "body_fat_change": None,
                "total_workouts": 0
            }
        
        # General statistics
        stats["total_records"] = len(self.progress_data)
        stats["start_date"] = self.progress_data["date"].min().strftime("%Y-%m-%d")
        stats["end_date"] = self.progress_data["date"].max().strftime("%Y-%m-%d")
        
        # Calculate tracked days
        date_range = (self.progress_data["date"].max() - self.progress_data["date"].min()).days
        stats["tracked_days"] = date_range + 1  # Include both start and end dates
        
        # Calculate weight change
        weight_data = self.progress_data[self.progress_data["weight"].notna()].sort_values("date")
        if len(weight_data) >= 2:
            first_weight = weight_data["weight"].iloc[0]
            last_weight = weight_data["weight"].iloc[-1]
            stats["weight_change"] = last_weight - first_weight
        else:
            stats["weight_change"] = None
        
        # Calculate body fat change
        body_fat_data = self.progress_data[self.progress_data["body_fat"].notna()].sort_values("date")
        if len(body_fat_data) >= 2:
            first_bf = body_fat_data["body_fat"].iloc[0]
            last_bf = body_fat_data["body_fat"].iloc[-1]
            stats["body_fat_change"] = last_bf - first_bf
        else:
            stats["body_fat_change"] = None
        
        # Count workouts (days with exercise data)
        workout_days = self.progress_data[self.progress_data["exercise"].notna()]["date"].dt.date.nunique()
        stats["total_workouts"] = workout_days
        
        return stats
    
    def _save_progress_data(self) -> None:
        """
        Save progress data to CSV file
        """
        try:
            # Ensure data directory exists
            os.makedirs(self.data_dir, exist_ok=True)
            
            # Save to CSV
            self.progress_data.to_csv(self.progress_file, index=False)
            logger.info(f"Progress data saved to {self.progress_file}")
            
        except Exception as e:
            logger.error(f"Error saving progress data: {e}")
    
    def clear_progress_data(self) -> bool:
        """
        Clear all progress data
        
        Returns:
            True if data was cleared successfully, False otherwise
        """
        try:
            self.progress_data = pd.DataFrame(columns=["date", "weight", "body_fat", "exercise", "sets", "reps", "notes"])
            self._save_progress_data()
            logger.info("Progress data cleared")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing progress data: {e}")
            return False 