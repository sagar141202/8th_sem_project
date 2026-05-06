# Emotion Recognition Using Speech

A Machine Learning based system that detects human emotions from speech audio using MFCC, Chroma, and Mel features.

## Team Members

- Sagar S. Maddi — 12215121
- Charan Kasagani — 12215095

## Project Overview

This project builds and trains a Speech Emotion Recognition (SER) system capable of identifying emotions such as Happy, Sad, Angry, Neutral, Fear, Disgust, Calm, and more from audio recordings.

### Key Features
- Extracts audio features: MFCC, Chroma, Mel Spectrogram
- Supports ML models: SVM, Random Forest, MLP
- Supports Deep Learning models: LSTM, GRU
- Real-time audio recording and emotion prediction
- Interactive Web Interface (Flask-based)

## Dataset Used
- RAVDESS
- TESS
- EMO-DB
- Custom dataset

## Tech Stack
- Python 3.8
- scikit-learn, Keras, TensorFlow
- librosa (audio feature extraction)
- Flask (web interface)
- HTML/CSS/JavaScript (frontend)

## How to Run

### 1. Install dependencies
pip install -r requirements.txt

### 2. Train the model
python emotion_recognition.py

### 3. Run the Web App
python app.py

Then open: http://localhost:5000

## References
- RAVDESS Dataset: https://zenodo.org/record/1188976
- librosa: https://librosa.org/
- This project is built upon open-source speech emotion recognition research.

## License
For academic use only. 8th Semester Final Year Project.
