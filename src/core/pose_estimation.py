import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import logging
from typing import Dict, List, Tuple, Optional, Any, Union

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

class PoseEstimator:
    """
    Class for pose estimation using MediaPipe
    """
    def __init__(self, 
                 static_image_mode: bool = False, 
                 model_complexity: int = 1, 
                 min_detection_confidence: float = 0.5, 
                 min_tracking_confidence: float = 0.5):
        """
        Initialize the pose estimator
        
        Args:
            static_image_mode: Whether to treat input as a static image
            model_complexity: Model complexity (0, 1, or 2)
            min_detection_confidence: Minimum confidence for detection
            min_tracking_confidence: Minimum confidence for tracking
        """
        self.pose = mp_pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        logger.info("PoseEstimator initialized successfully")
        
    def process_image(self, image: np.ndarray) -> Tuple[np.ndarray, Optional[Any]]:
        """
        Process an image and detect pose landmarks
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Tuple of (annotated image, pose results)
        """
        try:
            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process the image
            results = self.pose.process(image_rgb)
            
            # Make a copy of the image for annotation
            annotated_image = image.copy()
            
            # Draw pose landmarks on the image
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    annotated_image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
                )
                
            return annotated_image, results
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return image, None
    
    def extract_landmarks(self, results: Any) -> Dict[str, float]:
        """
        Extract landmark features from pose results
        
        Args:
            results: Pose detection results from MediaPipe
            
        Returns:
            Dictionary of landmark features
        """
        if not results or not results.pose_landmarks:
            logger.warning("No pose landmarks detected")
            return {}
        
        landmarks = results.pose_landmarks.landmark
        features = {}
        
        # Extract x, y coordinates for each landmark
        for idx, landmark in enumerate(landmarks):
            features[f"landmark_{idx}_x"] = landmark.x
            features[f"landmark_{idx}_y"] = landmark.y
            features[f"landmark_{idx}_z"] = landmark.z
            features[f"landmark_{idx}_visibility"] = landmark.visibility
            
        return features
    
    def landmarks_to_dataframe(self, features: Dict[str, float]) -> pd.DataFrame:
        """
        Convert landmark features to a pandas DataFrame
        
        Args:
            features: Dictionary of landmark features
            
        Returns:
            DataFrame of landmark features
        """
        return pd.DataFrame([features])
    
    def calculate_body_measurements(self, results: Any) -> Dict[str, float]:
        """
        Calculate body measurements from pose landmarks
        
        Args:
            results: Pose detection results from MediaPipe
            
        Returns:
            Dictionary of body measurements
        """
        if not results or not results.pose_landmarks:
            logger.warning("No pose landmarks detected for body measurements")
            return {}
        
        landmarks = results.pose_landmarks.landmark
        
        # Extract key landmarks
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        
        # Calculate measurements
        shoulder_width = self._calculate_distance(left_shoulder, right_shoulder)
        hip_width = self._calculate_distance(left_hip, right_hip)
        left_leg_length = self._calculate_distance(left_hip, left_ankle)
        right_leg_length = self._calculate_distance(right_hip, right_ankle)
        leg_length = (left_leg_length + right_leg_length) / 2
        left_arm_length = self._calculate_distance(left_shoulder, left_wrist)
        right_arm_length = self._calculate_distance(right_shoulder, right_wrist)
        arm_length = (left_arm_length + right_arm_length) / 2
        
        # Calculate shoulder-to-hip ratio
        shoulder_hip_ratio = shoulder_width / hip_width if hip_width > 0 else 0
        
        # Determine body type based on ratio
        if shoulder_hip_ratio > 1.25:
            body_type = "Inverted Triangle"
        elif shoulder_hip_ratio < 0.85:
            body_type = "Pear"
        else:
            body_type = "Rectangle"
            
        return {
            "shoulder_width": shoulder_width,
            "hip_width": hip_width,
            "leg_length": leg_length,
            "arm_length": arm_length,
            "shoulder_hip_ratio": shoulder_hip_ratio,
            "body_type": body_type
        }
    
    def _calculate_distance(self, p1: Any, p2: Any) -> float:
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
    
    def analyze_exercise_form(self, results: Any, exercise_type: str) -> Dict[str, Any]:
        """
        Analyze exercise form based on pose landmarks
        
        Args:
            results: Pose detection results from MediaPipe
            exercise_type: Type of exercise being performed
            
        Returns:
            Dictionary with exercise form analysis
        """
        if not results or not results.pose_landmarks:
            logger.warning(f"No pose landmarks detected for {exercise_type} analysis")
            return {"correct": False, "feedback": "No pose detected. Please ensure your full body is visible."}
        
        landmarks = results.pose_landmarks.landmark
        
        if exercise_type == "Push-up":
            return self._analyze_pushup_form(landmarks)
        elif exercise_type == "Squat":
            return self._analyze_squat_form(landmarks)
        elif exercise_type == "Plank":
            return self._analyze_plank_form(landmarks)
        elif exercise_type == "Lunge":
            return self._analyze_lunge_form(landmarks)
        else:
            return {"correct": False, "feedback": f"Analysis for {exercise_type} not implemented yet."}
    
    def _analyze_pushup_form(self, landmarks: List[Any]) -> Dict[str, Any]:
        """
        Analyze push-up form
        
        Args:
            landmarks: Pose landmarks
            
        Returns:
            Dictionary with push-up form analysis
        """
        # Get key landmarks
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        
        # Calculate angles
        left_elbow_angle = self._calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_elbow_angle = self._calculate_angle(right_shoulder, right_elbow, right_wrist)
        elbow_angle = min(left_elbow_angle, right_elbow_angle)
        
        # Check if back is straight
        back_straightness = self._check_alignment(left_shoulder, left_hip, left_ankle) and \
                           self._check_alignment(right_shoulder, right_hip, right_ankle)
        
        # Determine if form is correct
        correct = elbow_angle < 100 and back_straightness
        
        # Generate feedback
        feedback = []
        if not back_straightness:
            feedback.append("Keep your back straight and core engaged.")
        if elbow_angle >= 100:
            feedback.append("Lower your body more, aim for a 90-degree bend in your elbows.")
        
        if not feedback:
            feedback.append("Great form! Keep it up.")
            
        return {
            "correct": correct,
            "feedback": " ".join(feedback),
            "metrics": {
                "elbow_angle": elbow_angle,
                "back_straight": back_straightness
            }
        }
    
    def _analyze_squat_form(self, landmarks: List[Any]) -> Dict[str, Any]:
        """
        Analyze squat form
        
        Args:
            landmarks: Pose landmarks
            
        Returns:
            Dictionary with squat form analysis
        """
        # Get key landmarks
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        
        # Calculate angles
        left_knee_angle = self._calculate_angle(left_hip, left_knee, left_ankle)
        right_knee_angle = self._calculate_angle(right_hip, right_knee, right_ankle)
        knee_angle = min(left_knee_angle, right_knee_angle)
        
        # Check if back is straight (vertical alignment of shoulders and hips)
        back_straight = abs(left_shoulder.x - left_hip.x) < 0.1 and abs(right_shoulder.x - right_hip.x) < 0.1
        
        # Check knee position (knees should not go too far forward past toes)
        knees_over_toes = (left_knee.x < left_ankle.x) and (right_knee.x < right_ankle.x)
        
        # Determine if form is correct
        correct = knee_angle < 120 and back_straight and knees_over_toes
        
        # Generate feedback
        feedback = []
        if not back_straight:
            feedback.append("Keep your back straight and chest up.")
        if knee_angle >= 120:
            feedback.append("Lower your hips more, aim for a 90-degree bend in your knees.")
        if not knees_over_toes:
            feedback.append("Keep your knees behind your toes.")
        
        if not feedback:
            feedback.append("Great squat form! Keep it up.")
            
        return {
            "correct": correct,
            "feedback": " ".join(feedback),
            "metrics": {
                "knee_angle": knee_angle,
                "back_straight": back_straight,
                "knees_over_toes": knees_over_toes
            }
        }
    
    def _analyze_plank_form(self, landmarks: List[Any]) -> Dict[str, Any]:
        """
        Analyze plank form
        
        Args:
            landmarks: Pose landmarks
            
        Returns:
            Dictionary with plank form analysis
        """
        # Get key landmarks
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        
        # Check if body is in a straight line (shoulders, hips, ankles)
        body_alignment = self._check_alignment(left_shoulder, left_hip, left_ankle) and \
                         self._check_alignment(right_shoulder, right_hip, right_ankle)
        
        # Check if hips are not too high or too low
        hip_position = abs(left_hip.y - left_shoulder.y) < 0.1 and abs(right_hip.y - right_shoulder.y) < 0.1
        
        # Determine if form is correct
        correct = body_alignment and hip_position
        
        # Generate feedback
        feedback = []
        if not body_alignment:
            feedback.append("Maintain a straight line from head to heels.")
        if not hip_position:
            if left_hip.y < left_shoulder.y:
                feedback.append("Lower your hips, they're too high.")
            else:
                feedback.append("Raise your hips, they're too low.")
        
        if not feedback:
            feedback.append("Great plank form! Hold it steady.")
            
        return {
            "correct": correct,
            "feedback": " ".join(feedback),
            "metrics": {
                "body_alignment": body_alignment,
                "hip_position": hip_position
            }
        }
    
    def _analyze_lunge_form(self, landmarks: List[Any]) -> Dict[str, Any]:
        """
        Analyze lunge form
        
        Args:
            landmarks: Pose landmarks
            
        Returns:
            Dictionary with lunge form analysis
        """
        # Get key landmarks
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        
        # Calculate angles
        left_knee_angle = self._calculate_angle(left_hip, left_knee, left_ankle)
        right_knee_angle = self._calculate_angle(right_hip, right_knee, right_ankle)
        front_knee_angle = min(left_knee_angle, right_knee_angle)
        
        # Check if torso is upright
        torso_upright = abs(left_shoulder.x - left_hip.x) < 0.1 and abs(right_shoulder.x - right_hip.x) < 0.1
        
        # Check if front knee is aligned with ankle
        knee_ankle_alignment = (abs(left_knee.x - left_ankle.x) < 0.1) or (abs(right_knee.x - right_ankle.x) < 0.1)
        
        # Determine if form is correct
        correct = front_knee_angle < 110 and torso_upright and knee_ankle_alignment
        
        # Generate feedback
        feedback = []
        if not torso_upright:
            feedback.append("Keep your torso upright.")
        if front_knee_angle >= 110:
            feedback.append("Lower your body more, aim for a 90-degree bend in your front knee.")
        if not knee_ankle_alignment:
            feedback.append("Align your front knee over your ankle, not past your toes.")
        
        if not feedback:
            feedback.append("Great lunge form! Keep it up.")
            
        return {
            "correct": correct,
            "feedback": " ".join(feedback),
            "metrics": {
                "front_knee_angle": front_knee_angle,
                "torso_upright": torso_upright,
                "knee_ankle_alignment": knee_ankle_alignment
            }
        }
    
    def _calculate_angle(self, p1: Any, p2: Any, p3: Any) -> float:
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
    
    def _check_alignment(self, p1: Any, p2: Any, p3: Any) -> bool:
        """
        Check if three points are approximately aligned
        
        Args:
            p1: First point
            p2: Second point
            p3: Third point
            
        Returns:
            True if points are aligned, False otherwise
        """
        # Calculate vectors
        v1 = np.array([p1.x - p2.x, p1.y - p2.y])
        v2 = np.array([p3.x - p2.x, p3.y - p2.y])
        
        # Normalize vectors
        v1_norm = v1 / np.linalg.norm(v1)
        v2_norm = v2 / np.linalg.norm(v2)
        
        # Calculate dot product
        dot_product = np.abs(np.dot(v1_norm, v2_norm))
        
        # Points are considered aligned if dot product is close to 1
        return dot_product > 0.9 