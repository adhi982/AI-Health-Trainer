import os
import joblib
import logging
from typing import Any, Optional, Dict, List, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def save_model(model: Any, model_path: str) -> bool:
    """
    Save a model to disk
    
    Args:
        model: Model object to save
        model_path: Path to save the model
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Save the model
        joblib.dump(model, model_path)
        logger.info(f"Model saved to {model_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving model: {e}")
        return False

def load_model(model_path: str) -> Optional[Any]:
    """
    Load a model from disk
    
    Args:
        model_path: Path to the model file
        
    Returns:
        Loaded model or None if error
    """
    try:
        if not os.path.exists(model_path):
            logger.warning(f"Model file not found at {model_path}")
            return None
            
        model = joblib.load(model_path)
        logger.info(f"Model loaded from {model_path}")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None

def save_feature_names(feature_names: List[str], path: str) -> bool:
    """
    Save feature names to disk
    
    Args:
        feature_names: List of feature names
        path: Path to save the feature names
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save the feature names
        joblib.dump(feature_names, path)
        logger.info(f"Feature names saved to {path}")
        return True
    except Exception as e:
        logger.error(f"Error saving feature names: {e}")
        return False

def load_feature_names(path: str) -> Optional[List[str]]:
    """
    Load feature names from disk
    
    Args:
        path: Path to the feature names file
        
    Returns:
        List of feature names or None if error
    """
    try:
        if not os.path.exists(path):
            logger.warning(f"Feature names file not found at {path}")
            return None
            
        feature_names = joblib.load(path)
        logger.info(f"Feature names loaded from {path}")
        return feature_names
    except Exception as e:
        logger.error(f"Error loading feature names: {e}")
        return None 