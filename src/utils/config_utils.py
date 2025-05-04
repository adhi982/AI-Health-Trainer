import yaml
import os
import logging
from typing import Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(config_path: str = "src/config/config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dictionary containing configuration settings
    """
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"Configuration loaded successfully from {config_path}")
            return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        # Return default configuration
        return {
            "app": {
                "title": "AI Health Trainer",
                "icon": "💪",
                "layout": "wide",
                "initial_sidebar_state": "expanded"
            }
        }

def get_app_config() -> Dict[str, Any]:
    """
    Get application configuration settings
    
    Returns:
        Dictionary containing app configuration
    """
    config = load_config()
    return config.get("app", {})

def get_model_paths() -> Dict[str, str]:
    """
    Get paths to model files
    
    Returns:
        Dictionary containing model paths
    """
    config = load_config()
    return config.get("models", {})

def get_exercise_data_paths() -> Dict[str, str]:
    """
    Get paths to exercise data files
    
    Returns:
        Dictionary containing data file paths
    """
    config = load_config()
    return config.get("exercise_data", {})

def get_mediapipe_config() -> Dict[str, Any]:
    """
    Get MediaPipe configuration settings
    
    Returns:
        Dictionary containing MediaPipe configuration
    """
    config = load_config()
    return config.get("mediapipe", {}).get("pose", {})

def get_ui_theme() -> Dict[str, Any]:
    """
    Get UI theme configuration
    
    Returns:
        Dictionary containing UI theme settings
    """
    config = load_config()
    return config.get("ui", {}).get("theme", {})

def get_home_config() -> Dict[str, Any]:
    """
    Get home page configuration
    
    Returns:
        Dictionary containing home page settings
    """
    config = load_config()
    return config.get("home", {}) 