import os
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from models.utils.model_io import load_model

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BodyAnalyzer:
    """
    Class for body type analysis using trained model
    """
    def __init__(self, model_path: str = "models_data/body_type_model.pkl"):
        """
        Initialize the body analyzer
        
        Args:
            model_path: Path to the body type model file
        """
        self.model_path = model_path
        self.model = None
        
        # Load model
        self._load_model()
    
    def _load_model(self) -> None:
        """
        Load the body type classification model
        """
        self.model = load_model(self.model_path)
        
        if self.model is None:
            logger.error("Failed to load body type classification model")
        else:
            logger.info("Body type classification model loaded successfully")
    
    def analyze_body_type(self, measurements: Dict[str, float]) -> Tuple[str, Dict[str, Any]]:
        """
        Analyze body type from measurements
        
        Args:
            measurements: Dictionary of body measurements
            
        Returns:
            Tuple of (body type, additional metrics)
        """
        # Calculate metrics
        metrics = self._calculate_metrics(measurements)
        
        if self.model is None:
            logger.warning("Body type model not loaded, using rule-based classification")
            # Use rule-based classification
            body_type = self._rule_based_classification(measurements)
        else:
            try:
                # Create input features
                features = pd.DataFrame([{
                    "shoulder_width": measurements.get("shoulder_width", 0),
                    "hip_width": measurements.get("hip_width", 0),
                    "leg_length": measurements.get("leg_length", 0),
                    "arm_length": measurements.get("arm_length", 0),
                    "shoulder_hip_ratio": measurements.get("shoulder_hip_ratio", 0)
                }])
                
                # Make prediction
                body_type = self.model.predict(features)[0]
                logger.info(f"Body type classified as {body_type}")
            except Exception as e:
                logger.error(f"Error using model for body type analysis: {e}")
                # Fall back to rule-based classification
                body_type = self._rule_based_classification(measurements)
        
        return body_type, metrics
    
    def _rule_based_classification(self, measurements: Dict[str, float]) -> str:
        """
        Classify body type using rule-based approach
        
        Args:
            measurements: Dictionary of body measurements
            
        Returns:
            Body type classification
        """
        ratio = measurements.get("shoulder_hip_ratio", 0)
        
        if ratio > 1.25:
            return "Inverted Triangle"
        elif ratio < 0.85:
            return "Pear"
        else:
            return "Rectangle"
    
    def _calculate_metrics(self, measurements: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculate additional metrics from measurements
        
        Args:
            measurements: Dictionary of body measurements
            
        Returns:
            Dictionary of calculated metrics
        """
        metrics = {}
        
        # Calculate shoulder-to-height ratio
        if "leg_length" in measurements:
            height_estimate = measurements.get("leg_length", 0) * 1.5  # Rough estimate
            if height_estimate > 0:
                metrics["shoulder_height_ratio"] = measurements.get("shoulder_width", 0) / height_estimate
        
        # Calculate arm-to-height ratio
        if "arm_length" in measurements and "leg_length" in measurements:
            height_estimate = measurements.get("leg_length", 0) * 1.5  # Rough estimate
            if height_estimate > 0:
                metrics["arm_height_ratio"] = measurements.get("arm_length", 0) / height_estimate
        
        # Calculate body proportions
        metrics["upper_lower_ratio"] = measurements.get("torso_length", 0) / measurements.get("leg_length", 1)
        
        return metrics
    
    def get_exercise_recommendations(self, body_type: str, fitness_level: str = "Intermediate") -> List[str]:
        """
        Get exercise recommendations based on body type
        
        Args:
            body_type: Body type classification
            fitness_level: Fitness level (Beginner, Intermediate, Advanced)
            
        Returns:
            List of recommended exercises
        """
        recommendations = {
            "Inverted Triangle": {
                "Beginner": ["Squats", "Lunges", "Glute Bridges", "Calf Raises"],
                "Intermediate": ["Deadlifts", "Romanian Deadlifts", "Hip Thrusts", "Step-Ups"],
                "Advanced": ["Bulgarian Split Squats", "Pistol Squats", "Box Jumps", "Trap Bar Deadlifts"]
            },
            "Pear": {
                "Beginner": ["Push-Ups", "Dumbbell Rows", "Shoulder Press", "Bicep Curls"],
                "Intermediate": ["Bench Press", "Pull-Ups", "Lateral Raises", "Tricep Dips"],
                "Advanced": ["Weighted Pull-Ups", "Incline Bench Press", "Military Press", "Cable Flyes"]
            },
            "Rectangle": {
                "Beginner": ["Burpees", "Mountain Climbers", "Jumping Jacks", "High Knees"],
                "Intermediate": ["Box Jumps", "Kettlebell Swings", "Plank Variations", "Medicine Ball Slams"],
                "Advanced": ["Plyometric Push-Ups", "Tuck Jumps", "Battle Ropes", "Barbell Complexes"]
            }
        }
        
        default_recommendations = ["Push-Ups", "Squats", "Planks", "Lunges", "Mountain Climbers"]
        
        if body_type in recommendations and fitness_level in recommendations[body_type]:
            return recommendations[body_type][fitness_level]
        else:
            logger.warning(f"No specific recommendations for {body_type} at {fitness_level} level")
            return default_recommendations 