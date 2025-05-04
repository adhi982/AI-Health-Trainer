import os
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from models.utils.model_io import save_model

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_body_data(data_path: str) -> Optional[pd.DataFrame]:
    """
    Load body measurement data from CSV
    
    Args:
        data_path: Path to CSV file
        
    Returns:
        DataFrame containing body measurement data
    """
    try:
        if not os.path.exists(data_path):
            logger.error(f"Body data file not found at {data_path}")
            return None
            
        data = pd.read_csv(data_path)
        logger.info(f"Loaded {len(data)} body measurement samples from {data_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading body data: {e}")
        return None

def preprocess_body_data(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Preprocess body measurement data
    
    Args:
        data: DataFrame containing body measurement data
        
    Returns:
        Tuple of (features DataFrame, target Series)
    """
    try:
        if "body_type" not in data.columns:
            logger.error("Training data must contain 'body_type' column")
            raise ValueError("Training data must contain 'body_type' column")
        
        # Required measurement columns
        required_columns = ["shoulder_width", "hip_width", "leg_length", "arm_length"]
        
        # Check if required columns exist
        for column in required_columns:
            if column not in data.columns:
                logger.error(f"Required column '{column}' not found in training data")
                raise ValueError(f"Required column '{column}' not found in training data")
        
        # Split features and target
        X = data[required_columns]
        y = data["body_type"]
        
        # Add derived features
        X["shoulder_hip_ratio"] = X["shoulder_width"] / X["hip_width"]
        
        logger.info(f"Preprocessed data: {X.shape[0]} samples, {X.shape[1]} features")
        return X, y
    except Exception as e:
        logger.error(f"Error preprocessing body data: {e}")
        raise

def train_body_type_model(
    X: pd.DataFrame, 
    y: pd.Series, 
    params: Optional[Dict[str, Any]] = None,
    use_grid_search: bool = False
) -> Any:
    """
    Train body type classification model
    
    Args:
        X: Features DataFrame
        y: Target Series
        params: Model hyperparameters
        use_grid_search: Whether to use grid search for hyperparameter tuning
        
    Returns:
        Trained model
    """
    try:
        # Default parameters
        if params is None:
            params = {
                "n_estimators": 100,
                "max_depth": None,
                "min_samples_split": 2,
                "min_samples_leaf": 1,
                "random_state": 42
            }
            
        # Split data into train and validation sets
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        if use_grid_search:
            # Define parameter grid
            param_grid = {
                "n_estimators": [50, 100, 200],
                "max_depth": [None, 5, 10, 15],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4]
            }
            
            # Create base model
            base_model = RandomForestClassifier(random_state=42)
            
            # Create grid search
            grid_search = GridSearchCV(
                base_model,
                param_grid,
                cv=5,
                scoring="accuracy",
                n_jobs=-1,
                verbose=1
            )
            
            # Fit grid search
            logger.info("Starting grid search for hyperparameter tuning...")
            grid_search.fit(X_train, y_train)
            
            # Get best parameters
            best_params = grid_search.best_params_
            logger.info(f"Best parameters: {best_params}")
            
            # Train model with best parameters
            model = RandomForestClassifier(**best_params)
        else:
            # Train model with provided parameters
            model = RandomForestClassifier(**params)
            
        # Fit model
        logger.info("Training body type classification model...")
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_val)
        accuracy = accuracy_score(y_val, y_pred)
        logger.info(f"Model accuracy: {accuracy:.4f}")
        logger.info("\nClassification Report:\n" + classification_report(y_val, y_pred))
        
        # Get feature importances
        feature_importances = pd.DataFrame({
            'Feature': X.columns,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        logger.info("\nFeature Importances:\n" + str(feature_importances))
        
        return model
    except Exception as e:
        logger.error(f"Error training body type model: {e}")
        raise

def main():
    """
    Main function to train and save the body type model
    """
    try:
        # Load training data
        data_path = os.path.join("src", "data", "model_data", "training_data", "body_training_data.csv")
        data = load_body_data(data_path)
        
        if data is None:
            return
        
        # Preprocess data
        X, y = preprocess_body_data(data)
        
        # Train model
        model = train_body_type_model(X, y, use_grid_search=False)
        
        # Save model
        model_path = os.path.join("models_data", "body_type_model.pkl")
        save_model(model, model_path)
        
        logger.info("Body type model training completed successfully")
    except Exception as e:
        logger.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main() 