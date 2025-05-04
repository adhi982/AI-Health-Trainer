import pandas as pd
import numpy as np
import joblib
import logging
import os
from typing import Dict, List, Any, Optional, Tuple, Union
from sklearn.ensemble import RandomForestClassifier

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelManager:
    """
    Class for managing ML models
    """
    def __init__(self, 
                 exercise_model_path: str = "models/exercise_classifier.pkl",
                 body_model_path: str = "models/body_type_model.pkl",
                 feature_names_path: str = "models/feature_names.pkl"):
        """
        Initialize the model manager
        
        Args:
            exercise_model_path: Path to the exercise classification model
            body_model_path: Path to the body type classification model
            feature_names_path: Path to the feature names file
        """
        self.exercise_model_path = exercise_model_path
        self.body_model_path = body_model_path
        self.feature_names_path = feature_names_path
        self.exercise_model = None
        self.body_model = None
        self.feature_names = None
        
        # Try to load models
        self._load_models()
        
    def _load_models(self) -> None:
        """
        Load models from disk
        """
        try:
            # Load exercise classifier model
            if os.path.exists(self.exercise_model_path):
                self.exercise_model = joblib.load(self.exercise_model_path)
                logger.info(f"Exercise model loaded from {self.exercise_model_path}")
            else:
                logger.warning(f"Exercise model file not found at {self.exercise_model_path}")
            
            # Load body type model
            if os.path.exists(self.body_model_path):
                self.body_model = joblib.load(self.body_model_path)
                logger.info(f"Body model loaded from {self.body_model_path}")
            else:
                logger.warning(f"Body model file not found at {self.body_model_path}")
            
            # Load feature names
            if os.path.exists(self.feature_names_path):
                self.feature_names = joblib.load(self.feature_names_path)
                logger.info(f"Feature names loaded from {self.feature_names_path}")
            else:
                logger.warning(f"Feature names file not found at {self.feature_names_path}")
                
        except Exception as e:
            logger.error(f"Error loading models: {e}")
    
    def identify_exercise(self, features: Dict[str, float]) -> Tuple[str, float]:
        """
        Identify exercise type from pose landmarks
        
        Args:
            features: Dictionary of landmark features
            
        Returns:
            Tuple of (exercise name, confidence)
        """
        if self.exercise_model is None:
            logger.error("Exercise model not loaded")
            return "Unknown", 0.0
        
        try:
            # Convert features to DataFrame
            df = pd.DataFrame([features])
            
            # Select only the features used by the model
            if self.feature_names is not None:
                df = df[self.feature_names]
            
            # Make prediction
            prediction = self.exercise_model.predict(df)[0]
            
            # Get confidence score
            confidence = self.exercise_model.predict_proba(df).max()
            
            logger.info(f"Exercise identified as {prediction} with confidence {confidence:.2f}")
            return prediction, float(confidence)
            
        except Exception as e:
            logger.error(f"Error identifying exercise: {e}")
            return "Unknown", 0.0
    
    def classify_body_type(self, measurements: Dict[str, float]) -> str:
        """
        Classify body type from measurements
        
        Args:
            measurements: Dictionary of body measurements
            
        Returns:
            Body type classification
        """
        if self.body_model is None:
            logger.warning("Body model not loaded, using rule-based classification")
            # Use rule-based classification
            ratio = measurements.get("shoulder_hip_ratio", 0)
            if ratio > 1.25:
                return "Inverted Triangle"
            elif ratio < 0.85:
                return "Pear"
            else:
                return "Rectangle"
        
        try:
            # Create a DataFrame with the measurements
            df = pd.DataFrame([{
                "shoulder_width": measurements.get("shoulder_width", 0),
                "hip_width": measurements.get("hip_width", 0),
                "leg_length": measurements.get("leg_length", 0),
                "arm_length": measurements.get("arm_length", 0)
            }])
            
            # Make prediction
            body_type = self.body_model.predict(df)[0]
            logger.info(f"Body type classified as {body_type}")
            return body_type
            
        except Exception as e:
            logger.error(f"Error classifying body type: {e}")
            return "Unknown"
    
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
    
    def train_exercise_model(self, training_data: pd.DataFrame) -> None:
        """
        Train a new exercise classification model
        
        Args:
            training_data: DataFrame containing training data
        """
        try:
            if "exercise" not in training_data.columns:
                logger.error("Training data must contain 'exercise' column")
                return
            
            # Split features and target
            X = training_data.drop("exercise", axis=1)
            y = training_data["exercise"]
            
            # Save feature names
            self.feature_names = X.columns.tolist()
            
            # Train model
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X, y)
            
            # Save model
            self.exercise_model = model
            joblib.dump(model, self.exercise_model_path)
            joblib.dump(self.feature_names, self.feature_names_path)
            
            logger.info(f"Exercise model trained and saved to {self.exercise_model_path}")
            
        except Exception as e:
            logger.error(f"Error training exercise model: {e}")
    
    def train_body_model(self, training_data: pd.DataFrame) -> None:
        """
        Train a new body type classification model
        
        Args:
            training_data: DataFrame containing training data
        """
        try:
            if "body_type" not in training_data.columns:
                logger.error("Training data must contain 'body_type' column")
                return
            
            # Split features and target
            X = training_data.drop("body_type", axis=1)
            y = training_data["body_type"]
            
            # Train model
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X, y)
            
            # Save model
            self.body_model = model
            joblib.dump(model, self.body_model_path)
            
            logger.info(f"Body model trained and saved to {self.body_model_path}")
            
        except Exception as e:
            logger.error(f"Error training body model: {e}")
    
    def save_models(self) -> None:
        """
        Save models to disk
        """
        try:
            if self.exercise_model is not None:
                joblib.dump(self.exercise_model, self.exercise_model_path)
                logger.info(f"Exercise model saved to {self.exercise_model_path}")
            
            if self.body_model is not None:
                joblib.dump(self.body_model, self.body_model_path)
                logger.info(f"Body model saved to {self.body_model_path}")
            
            if self.feature_names is not None:
                joblib.dump(self.feature_names, self.feature_names_path)
                logger.info(f"Feature names saved to {self.feature_names_path}")
                
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    def load_exercise_data(self, path: str) -> pd.DataFrame:
        """
        Load exercise data from CSV
        
        Args:
            path: Path to CSV file
            
        Returns:
            DataFrame containing exercise data
        """
        try:
            data = pd.read_csv(path)
            logger.info(f"Loaded {len(data)} exercise samples from {path}")
            return data
        except Exception as e:
            logger.error(f"Error loading exercise data: {e}")
            return pd.DataFrame() 