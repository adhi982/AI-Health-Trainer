#!/usr/bin/env python
import os
import subprocess
import sys
import webbrowser
import time
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """
    Check if required dependencies are installed
    """
    try:
        # Get the requirements file path
        requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
        
        # Check if the file exists
        if not os.path.exists(requirements_path):
            logger.error("Requirements file not found. Please ensure requirements.txt is present.")
            return False
        
        # Install dependencies
        logger.info("Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        logger.info("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing dependencies: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

def ensure_data_directory():
    """
    Ensure data directory exists
    """
    try:
        # Create data directory if it doesn't exist
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        
        # Create models directory if it doesn't exist
        models_dir = os.path.join(os.path.dirname(__file__), "models")
        Path(models_dir).mkdir(parents=True, exist_ok=True)
        
        logger.info("Data and models directories created/verified")
        return True
    except Exception as e:
        logger.error(f"Error creating directories: {e}")
        return False

def copy_model_files():
    """
    Copy model files to the correct directory
    """
    try:
        import shutil
        
        # Define source paths (original model files)
        source_files = [
            "exercise_model.pkl",
            "body_type_model.pkl",
            "feature_names.pkl",
            "exercise_classifier.pkl"
        ]
        
        # Define target directory
        target_dir = os.path.join(os.path.dirname(__file__), "models")
        
        # Define source directory (models_data)
        source_dir = os.path.join(os.path.dirname(__file__), "models_data")
        
        # Copy files that exist to the models directory
        for file in source_files:
            source_path = os.path.join(source_dir, file)
            if os.path.exists(source_path):
                target_path = os.path.join(target_dir, file)
                shutil.copy2(source_path, target_path)
                logger.info(f"Copied {file} from models_data to models directory")
        
        return True
    except Exception as e:
        logger.error(f"Error copying model files: {e}")
        return False

def copy_data_files():
    """
    Copy data files to the correct directory
    """
    try:
        import shutil
        
        # Define source paths (original data files)
        source_files = [
            "body_data.csv",
            "exercise_data.csv",
            "predicted_body_types.csv",
            "test_data.csv"
        ]
        
        # Define target directory
        target_dir = os.path.join(os.path.dirname(__file__), "data")
        
        # Copy files that exist to the data directory
        for file in source_files:
            source_path = os.path.join(os.path.dirname(__file__), file)
            if os.path.exists(source_path):
                target_path = os.path.join(target_dir, file)
                shutil.copy2(source_path, target_path)
                logger.info(f"Copied {file} to data directory")
        
        return True
    except Exception as e:
        logger.error(f"Error copying data files: {e}")
        return False

def run_app():
    """
    Run the Streamlit app
    """
    try:
        # Get the app path
        app_path = os.path.join(os.path.dirname(__file__), "src", "app.py")
        
        # Check if the file exists
        if not os.path.exists(app_path):
            logger.error("App file not found. Please check that src/app.py exists.")
            return False
        
        # Run the app
        logger.info("Starting the app...")
        
        # Construct the command to run the app
        cmd = [sys.executable, "-m", "streamlit", "run", app_path, "--server.port=8501"]
        
        # Open browser
        webbrowser.open_new("http://localhost:8501")
        
        # Run the app
        subprocess.run(cmd)
        return True
    except Exception as e:
        logger.error(f"Error running app: {e}")
        return False

def main():
    """
    Main function
    """
    logger.info("Starting AI Health Trainer setup...")
    
    # Check dependencies
    if not check_dependencies():
        logger.error("Failed to install dependencies. Exiting...")
        return
    
    # Ensure directories exist
    if not ensure_data_directory():
        logger.error("Failed to create required directories. Exiting...")
        return
    
    # Copy model files
    copy_model_files()
    
    # Copy data files
    copy_data_files()
    
    # Run the app
    run_app()

if __name__ == "__main__":
    main() 