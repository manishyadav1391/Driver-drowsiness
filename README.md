# 🚗 Driver Drowsiness Detection System

A real-time driver drowsiness detection application that uses computer vision and facial landmark analysis to monitor driver alertness and prevent accidents caused by fatigue.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Face%20Mesh-green)

## 📋 Features

- **Real-time Face Detection** - Uses MediaPipe Face Mesh for accurate facial landmark detection
- **Eye Aspect Ratio (EAR) Analysis** - Calculates eye closure ratio to detect drowsiness
- **Audio Alerts** - Plays warning sounds when drowsiness is detected
- **Pinecone Integration** - Stores drowsiness data vectors for analysis
- **User Authentication** - Secure login system for users and administrators
- **Admin Dashboard** - Analytics and visualization of drowsiness detection data
- **Confidence Scoring** - Real-time drowsiness confidence percentage

## 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| Frontend | Streamlit |
| Computer Vision | OpenCV, MediaPipe |
| Data Analysis | NumPy, Pandas, Matplotlib, Seaborn |
| Vector Database | Pinecone |
| Audio | Pygame |
| Deployment | Local (Streamlit) |

## 📁 Project Structure

```
driver_drowsiness/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── alarm1.wav         # Alert sound file
└── alarm2.mp3         # Welcome sound file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Webcam/Camera

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd driver_drowsiness
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

## 🔐 Login Credentials

### Admin Access
- **Username:** `admin`
- **Password:** `admin123`

### User Access
- **Username:** `user`
- **Password:** `user123`

## 📊 How It Works

### Drowsiness Detection Algorithm

1. **Face Mesh Detection** - MediaPipe detects 468 facial landmarks
2. **Eye Landmark Extraction** - Key points around both eyes are extracted
3. **EAR Calculation** - Eye Aspect Ratio is calculated using:
   ```
   EAR = (A + B) / (2.0 * C)
   ```
   Where A, B, C are distances between eye landmarks
4. **Drowsiness判断** - If EAR < 0.22 for sustained period, drowsiness is detected
5. **Alert Generation** - Audio alert is played and data is stored in Pinecone

### Threshold Values

| Parameter | Value | Description |
|-----------|-------|-------------|
| EAR Threshold | 0.22 | Below this = Drowsy |
| Alert Cooldown | 5 seconds | Minimum time between alerts |
| Detection Confidence | 0.5 | MediaPipe confidence threshold |

## 📈 Admin Dashboard Features

- **Data Table** - View all drowsiness detection records
- **Timestamp Sorting** - Analyze data chronologically
- **Distribution Chart** - Histogram of drowsiness scores with KDE
- **Export Capability** - Data available for further analysis

## 🔧 Configuration

### Pinecone Setup

The application uses Pinecone vector database for storing detection data. The following environment is configured:
- **Cloud:** AWS
- **Region:** us-east-1
- **Dimension:** 384
- **Metric:** Cosine similarity

### Customization

You can modify these parameters in `app.py`:

```python
# EAR Threshold
if avg_ear < 0.22:  # Change this value

# Alert Cooldown
if avg_ear < 0.22 and time.time() - last_alert_time > 5:  # Adjust cooldown
```

## ⚠️ Important Notes

1. **Webcam Required** - A functional webcam is needed for detection
2. **Lighting Conditions** - Best results in good lighting
3. **Face Position** - Keep face centered in camera frame
4. **Pinecone API** - Requires valid Pinecone account and API key

## 📝 Dependencies

```
opencv-python
numpy
mediapipe
streamlit
pygame
matplotlib
seaborn
pandas
pinecone-client
```

## 🎯 Use Cases

- 🚚 Commercial truck drivers
- 🏎️ Racing drivers
- 🚗 Ride-sharing services
- 🏭 Industrial vehicle operators
- 🚌 Public transportation

## 🔒 Safety Disclaimer

This system is designed as a **driver assistance tool** and should not be relied upon as the sole method of accident prevention. Drivers should always ensure they are well-rested and take regular breaks during long journeys.

## 📄 License

This project is for educational and demonstration purposes.

## 👤 Author

Created by: Manish Yadav

---

<div align="center">
Made with ❤️ for road safety
</div>

