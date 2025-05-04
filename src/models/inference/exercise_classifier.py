import os
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from models.utils.model_io import load_model, load_feature_names
from models.utils.feature_extraction import extract_pose_features, features_to_dataframe

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExerciseClassifier:
    """
    Class for exercise classification using trained model
    """
    def __init__(self, 
                 model_path: str = "models_data/exercise_model.pkl",
                 feature_names_path: str = "models_data/feature_names.pkl"):
        """
        Initialize the exercise classifier
        
        Args:
            model_path: Path to the exercise model file
            feature_names_path: Path to the feature names file
        """
        self.model_path = model_path
        self.feature_names_path = feature_names_path
        self.model = None
        self.feature_names = None
        
        # Load model and feature names
        self._load_model()
    
    def _load_model(self) -> None:
        """
        Load the exercise classification model
        """
        self.model = load_model(self.model_path)
        self.feature_names = load_feature_names(self.feature_names_path)
        
        if self.model is None:
            logger.error("Failed to load exercise classification model")
        else:
            logger.info("Exercise classification model loaded successfully")
            
        if self.feature_names is None:
            logger.error("Failed to load feature names")
        else:
            logger.info(f"Loaded {len(self.feature_names)} feature names")
    
    def classify_exercise(self, pose_landmarks: Any) -> Tuple[str, float]:
        """
        Classify exercise type from pose landmarks
        
        Args:
            pose_landmarks: Pose landmarks from MediaPipe
            
        Returns:
            Tuple of (exercise name, confidence score)
        """
        if self.model is None or self.feature_names is None:
            logger.error("Model or feature names not loaded")
            return "Unknown", 0.0
        
        try:
            # Extract features from pose landmarks
            features = extract_pose_features(pose_landmarks.landmark)
            
            # Convert to DataFrame
            features_df = features_to_dataframe(features)
            
            # Select only the features used by the model
            if set(self.feature_names).issubset(set(features_df.columns)):
                model_input = features_df[self.feature_names]
            else:
                missing_features = set(self.feature_names) - set(features_df.columns)
                logger.warning(f"Missing features: {missing_features}")
                # Fill missing features with zeros
                for feature in missing_features:
                    features_df[feature] = 0
                model_input = features_df[self.feature_names]
            
            # Make prediction
            prediction = self.model.predict(model_input)[0]
            
            # Get confidence score
            confidence = self.model.predict_proba(model_input).max()
            
            logger.info(f"Exercise classified as {prediction} with confidence {confidence:.2f}")
            return prediction, float(confidence)
            
        except Exception as e:
            logger.error(f"Error classifying exercise: {e}")
            return "Unknown", 0.0
        
    def is_valid_exercise(self, exercise: str, confidence: float, threshold: float = 0.7) -> bool:
        """
        Check if the classified exercise is valid based on confidence threshold
        
        Args:
            exercise: Classified exercise name
            confidence: Classification confidence score
            threshold: Confidence threshold
            
        Returns:
            True if valid exercise, False otherwise
        """
        return exercise != "Unknown" and confidence >= threshold 