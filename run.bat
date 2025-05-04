@echo off
SETLOCAL

REM Run the AI Health Trainer application

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)

REM Check if virtual environment exists
IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create directories if they don't exist
IF NOT EXIST data mkdir data
IF NOT EXIST models mkdir models

REM Copy model files if they exist
FOR %%F IN (exercise_model.pkl body_type_model.pkl feature_names.pkl exercise_classifier.pkl) DO (
    IF EXIST %%F (
        echo Copying %%F to models directory...
        copy %%F models\ >nul
    )
)

REM Copy data files if they exist
FOR %%F IN (body_data.csv exercise_data.csv predicted_body_types.csv test_data.csv) DO (
    IF EXIST %%F (
        echo Copying %%F to data directory...
        copy %%F data\ >nul
    )
)

REM Run the application
echo Starting AI Health Trainer...
python run.py

ENDLOCAL 