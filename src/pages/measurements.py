import streamlit as st
import math
import os
import sys
from src.utils.config_utils import get_app_config
from src.utils.ui_utils import set_page_config, apply_custom_css, display_header

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) if __name__ != "__main__" else os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Get app configuration
app_config = get_app_config()

# Set page configuration
set_page_config(
    title=f"{app_config.get('title', 'AI Health Trainer')} - Health Measurements",
    icon="🧮",
    layout=app_config.get("layout", "wide"),
    initial_sidebar_state=app_config.get("initial_sidebar_state", "expanded")
)

# Apply custom CSS
apply_custom_css()

# Display header
display_header(
    title="Health Measurements",
    subtitle="Calculate your BMI, BMR, ideal weight, and more in real time. Enter your details below for instant results.",
    icon="🧮"
)

# Sidebar navigation
st.sidebar.title("Navigation")
if st.sidebar.button("🏠 Home"):
    st.switch_page("app.py")
if st.sidebar.button("🏋️ Exercise Verification"):
    st.switch_page("pages/exercise_verification.py")
if st.sidebar.button("📏 Body Analysis"):
    st.switch_page("pages/body_analysis.py")
if st.sidebar.button("📋 Exercise Recommendations"):
    st.switch_page("pages/exercise_recommendations.py")
if st.sidebar.button("📈 Progress Tracking"):
    st.switch_page("pages/progress_tracking.py")

# Main content layout
col1, col2, col3 = st.columns(3)

with col1:
    weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=70.0, step=0.1)

with col2:
    height_cm = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)
    # Convert cm to feet and inches for display
    total_inches = height_cm / 2.54
    feet = int(total_inches // 12)
    inches = int(round(total_inches % 12))
    st.caption(f"Height: {feet} ft {inches} in")

with col3:
    age = st.number_input("Age (years)", min_value=5, max_value=120, value=30, step=1)
gender = st.selectbox("Gender", ["Male", "Female"], index=0)

# Calculations
def calculate_bmi(weight, height):
    if height <= 0:
        return 0
    return weight / ((height / 100) ** 2)

def calculate_bmr(weight, height, age, gender):
    if gender == "Male":
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

def calculate_ideal_weight(height, gender):
    if gender == "Male":
        return 50 + 0.91 * (height - 152.4)
    else:
        return 45.5 + 0.91 * (height - 152.4)

bmi = calculate_bmi(weight, height_cm)
bmr = calculate_bmr(weight, height_cm, age, gender)
ideal_weight = calculate_ideal_weight(height_cm, gender)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# Results section
st.markdown("## Results")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("BMI", f"{bmi:.2f}", bmi_category(bmi))
with col2:
    st.metric("BMR (kcal/day)", f"{bmr:.0f}")
with col3:
    st.metric("Ideal Weight (kg)", f"{ideal_weight:.1f}")

# Recommendations section
st.markdown("## Recommendations")
if bmi < 18.5:
    st.info("You are underweight. Consider a balanced diet with more calories and strength training.")
    target_weight = 18.5 * ((height_cm / 100) ** 2)
    st.markdown(f"To reach a normal BMI (18.5), your weight should be at least **{target_weight:.1f} kg**.")
    st.markdown(f"You need to gain **{target_weight - weight:.1f} kg** to reach the lower end of the normal BMI range.")
elif bmi < 25:
    st.success("You are in the normal weight range. Maintain your healthy lifestyle!")
else:
    if bmi < 30:
        st.warning("You are overweight. Consider regular exercise and a healthy diet.")
    else:
        st.error("You are in the obese range. Consult a healthcare provider for personalized advice.")
    target_weight = 24.9 * ((height_cm / 100) ** 2)
    st.markdown(f"To reach a normal BMI (24.9), your weight should be **{target_weight:.1f} kg** or less.")
    st.markdown(f"You need to lose **{weight - target_weight:.1f} kg** to reach the upper end of the normal BMI range.")

st.markdown("---")
st.markdown("**Note:** These calculations are estimates and should not replace professional medical advice.") 