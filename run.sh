#!/bin/bash

# Run the AI Health Trainer application

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create directories if they don't exist
mkdir -p data models

# Copy model files if they exist
for model_file in exercise_model.pkl body_type_model.pkl feature_names.pkl exercise_classifier.pkl; do
    if [ -f "$model_file" ]; then
        echo "Copying $model_file to models directory..."
        cp "$model_file" models/
    fi
done

# Copy data files if they exist
for data_file in body_data.csv exercise_data.csv predicted_body_types.csv test_data.csv; do
    if [ -f "$data_file" ]; then
        echo "Copying $data_file to data directory..."
        cp "$data_file" data/
    fi
done

# Run the application
echo "Starting AI Health Trainer..."
python run.py 