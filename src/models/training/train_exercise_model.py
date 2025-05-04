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

from models.utils.model_io import save_model, save_feature_names

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_training_data(data_path: str) -> Optional[pd.DataFrame]:
    """
    Load training data from CSV
    
    Args:
        data_path: Path to CSV file
        
    Returns:
        DataFrame containing training data
    """
    try:
        if not os.path.exists(data_path):
            logger.error(f"Training data file not found at {data_path}")
            return None
            
        data = pd.read_csv(data_path)
        logger.info(f"Loaded {len(data)} training samples from {data_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading training data: {e}")
        return None

def preprocess_data(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, List[str]]:
    """
    Preprocess training data
    
    Args:
        data: DataFrame containing training data
        
    Returns:
        Tuple of (features DataFrame, target Series, feature names list)
    """
    try:
        if "exercise" not in data.columns:
            logger.error("Training data must contain 'exercise' column")
            raise ValueError("Training data must contain 'exercise' column")
        
        # Split features and target
        X = data.drop("exercise", axis=1)
        y = data["exercise"]
        
        # Get feature names
        feature_names = X.columns.tolist()
        
        logger.info(f"Preprocessed data: {X.shape[0]} samples, {X.shape[1]} features")
        return X, y, feature_names
    except Exception as e:
        logger.error(f"Error preprocessing data: {e}")
        raise

def train_exercise_model(
    X: pd.DataFrame, 
    y: pd.Series, 
    params: Optional[Dict[str, Any]] = None,
    use_grid_search: bool = False
) -> Any:
    """
    Train exercise classification model
    
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
                "max_depth": [None, 10, 20, 30],
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
        logger.info("Training exercise classification model...")
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_val)
        accuracy = accuracy_score(y_val, y_pred)
        logger.info(f"Model accuracy: {accuracy:.4f}")
        logger.info("\nClassification Report:\n" + classification_report(y_val, y_pred))
        
        return model
    except Exception as e:
        logger.error(f"Error training model: {e}")
        raise

def main():
    """
    Main function to train and save the exercise model
    """
    try:
        # Load training data
        data_path = os.path.join("src", "data", "model_data", "training_data", "exercise_training_data.csv")
        data = load_training_data(data_path)
        
        if data is None:
            return
        
        # Preprocess data
        X, y, feature_names = preprocess_data(data)
        
        # Train model
        model = train_exercise_model(X, y, use_grid_search=False)
        
        # Save model and feature names
        model_path = os.path.join("models_data", "exercise_model.pkl")
        feature_names_path = os.path.join("models_data", "feature_names.pkl")
        
        save_model(model, model_path)
        save_feature_names(feature_names, feature_names_path)
        
        logger.info("Exercise model training completed successfully")
    except Exception as e:
        logger.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main() 