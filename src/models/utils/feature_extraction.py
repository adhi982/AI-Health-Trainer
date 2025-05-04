import numpy as np
import pandas as pd
import logging
from typing import Dict, List, Any, Optional, Tuple
import mediapipe as mp

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MediaPipe pose landmarks
mp_pose = mp.solutions.pose

def extract_pose_features(landmarks: List[Any]) -> Dict[str, float]:
    """
    Extract features from pose landmarks for model input
    
    Args:
        landmarks: List of pose landmarks from MediaPipe
        
    Returns:
        Dictionary of landmark features
    """
    features = {}
    
    try:
        # Extract x, y coordinates for each landmark
        for idx, landmark in enumerate(landmarks):
            features[f"landmark_{idx}_x"] = landmark.x
            features[f"landmark_{idx}_y"] = landmark.y
            features[f"landmark_{idx}_z"] = landmark.z
            features[f"landmark_{idx}_visibility"] = landmark.visibility
            
        # Calculate additional geometric features
        features.update(calculate_angles(landmarks))
        features.update(calculate_distances(landmarks))
            
        return features
    except Exception as e:
        logger.error(f"Error extracting pose features: {e}")
        return {}

def calculate_angles(landmarks: List[Any]) -> Dict[str, float]:
    """
    Calculate joint angles from landmarks
    
    Args:
        landmarks: List of pose landmarks
        
    Returns:
        Dictionary of angle features
    """
    angles = {}
    
    try:
        # Right elbow angle
        angles["right_elbow_angle"] = calculate_angle(
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        )
        
        # Left elbow angle
        angles["left_elbow_angle"] = calculate_angle(
            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
            landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        )
        
        # Right knee angle
        angles["right_knee_angle"] = calculate_angle(
            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
            landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        )
        
        # Left knee angle
        angles["left_knee_angle"] = calculate_angle(
            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
            landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        )
        
        # Torso angle (between shoulders and hips)
        angles["torso_angle"] = calculate_angle(
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        )
        
        return angles
    except Exception as e:
        logger.error(f"Error calculating joint angles: {e}")
        return {}

def calculate_distances(landmarks: List[Any]) -> Dict[str, float]:
    """
    Calculate distances between key landmarks
    
    Args:
        landmarks: List of pose landmarks
        
    Returns:
        Dictionary of distance features
    """
    distances = {}
    
    try:
        # Shoulder width
        distances["shoulder_width"] = calculate_distance(
            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        )
        
        # Hip width
        distances["hip_width"] = calculate_distance(
            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        )
        
        # Shoulder to hip (torso length)
        distances["torso_length"] = calculate_distance(
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        )
        
        # Wrist to shoulder (arm length)
        distances["arm_length"] = (
            calculate_distance(
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
            ) +
            calculate_distance(
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
            )
        ) / 2
        
        # Hip to ankle (leg length)
        distances["leg_length"] = (
            calculate_distance(
                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
            ) +
            calculate_distance(
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            )
        ) / 2
        
        return distances
    except Exception as e:
        logger.error(f"Error calculating landmark distances: {e}")
        return {}

def calculate_angle(p1: Any, p2: Any, p3: Any) -> float:
    """
    Calculate angle between three points
    
    Args:
        p1: First point
        p2: Second point (joint/vertex)
        p3: Third point
        
    Returns:
        Angle in degrees
    """
    # Calculate vectors
    v1 = np.array([p1.x - p2.x, p1.y - p2.y])
    v2 = np.array([p3.x - p2.x, p3.y - p2.y])
    
    # Normalize vectors
    v1_norm = v1 / np.linalg.norm(v1)
    v2_norm = v2 / np.linalg.norm(v2)
    
    # Calculate dot product
    dot_product = np.clip(np.dot(v1_norm, v2_norm), -1.0, 1.0)
    
    # Calculate angle in degrees
    angle = np.degrees(np.arccos(dot_product))
    
    return angle

def calculate_distance(p1: Any, p2: Any) -> float:
    """
    Calculate 3D distance between two points
    
    Args:
        p1: First point
        p2: Second point
        
    Returns:
        Euclidean distance between points
    """
    return np.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2 +
        (p1.z - p2.z) ** 2
    )

def features_to_dataframe(features: Dict[str, float]) -> pd.DataFrame:
    """
    Convert feature dictionary to DataFrame
    
    Args:
        features: Dictionary of extracted features
        
    Returns:
        DataFrame containing features
    """
    return pd.DataFrame([features]) 