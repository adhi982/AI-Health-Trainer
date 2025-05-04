# AI Health Trainer

Your personal AI-powered fitness coach that analyzes your form, tracks progress, and provides customized workout plans - all from your computer or mobile device.

## What This Does

AI Health Trainer uses computer vision and artificial intelligence to:

- **Watch Your Form:** Get real-time feedback on your exercise technique
- **Measure Your Body:** Calculate key body measurements from photos 
- **Create Custom Workouts:** Receive personalized exercise plans based on your body type and goals
- **Track Your Progress:** Visualize improvements in your fitness journey

## How It Works

The application uses your device's camera to analyze movement patterns during exercises and compares them to correct form. For body analysis, it processes images to identify key measurements and determine your body type, which helps create tailored workout recommendations.

## Technologies Used

- **Python 3.8+** - Core programming language
- **Streamlit** - Creates the interactive web interface
- **MediaPipe** - Powers the pose detection and body measurement
- **OpenCV** - Processes video and image data
- **Scikit-learn** - Runs machine learning algorithms
- **Pandas & NumPy** - Handles data processing
- **Plotly** - Generates interactive progress charts

## Getting Started

1. Clone this repository
   ```
   git clone https://github.com/adi982/AI-Health-Trainer.git
   cd AI-Health-Trainer
   ```

2. Set up a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install and launch
   ```
   python run.py
   ```

   The app will open in your web browser automatically.

## Using the App

### Exercise Form Check
Choose an exercise, start your webcam, and perform the movement. The AI provides instant feedback on your form, highlighting any corrections needed.

### Body Measurements
Upload a full-body photo to get measurements like shoulder width, waist, and leg length. The system also identifies your body type and suggests suitable exercises.

### Workout Planner
Input your fitness level, body type, and goals to receive a customized workout schedule with detailed instructions for each exercise.

### Progress Dashboard
Log your measurements and completed workouts to visualize your progress with interactive charts and statistics.

## Project Organization

```
AI-Health-Trainer/
├── data/                 # Stores user progress data
├── models/               # AI model files
├── src/                  # Source code
│   ├── config/           # Application settings
│   ├── core/             # Core AI functions
│   ├── models/           # Model implementation
│   ├── pages/            # App interface pages
│   ├── utils/            # Helper functions
│   └── app.py            # Main application
├── requirements.txt      # Dependencies
└── run.py                # Startup script
```

## System Requirements

- Python 3.8 or higher
- Webcam (for exercise analysis)
- Internet connection (initial setup only)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

- MediaPipe team for their pose estimation technology
- Streamlit for the web application framework
- Open-source contributors for various essential tools

## Contributing

Want to help improve AI Health Trainer? Here's how:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add some new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request