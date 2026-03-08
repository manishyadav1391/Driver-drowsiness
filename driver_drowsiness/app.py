import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import time
import threading
import pygame
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

from pinecone import Pinecone, ServerlessSpec


# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="🚗 Driver Drowsiness Detection",
    layout="wide"
)
#ddkzlxkdo
# -------------------- AUDIO INIT --------------------
pygame.mixer.init()

WELCOME_SOUND = "alarm2.mp3"
ALERT_SOUND = "alarm1.wav"

# -------------------- PINECONE INIT (LATEST SDK) --------------------
pc = Pinecone(
    api_key="pcsk_3DGaof_RbmimZrmcQ4hMGHB9e5ahiGE7JP8P8pEeA412EYvw3rnWpKfh8NiWTJe63DmNqD"
)

INDEX_NAME = "drowsiness-detection"
DIMENSION = 384

if INDEX_NAME not in [idx["name"] for idx in pc.list_indexes()]:
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index(INDEX_NAME)

# -------------------- MEDIAPIPE INIT --------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# -------------------- SOUND FUNCTIONS --------------------
def play_welcome_sound():
    pygame.mixer.music.load(WELCOME_SOUND)
    pygame.mixer.music.play()

def play_alert():
    pygame.mixer.music.load(ALERT_SOUND)
    pygame.mixer.music.play()

# -------------------- EAR CALCULATION --------------------
def calculate_ear(landmarks, eye_points):
    points = np.array([landmarks[p] for p in eye_points])
    A = np.linalg.norm(points[1] - points[5])
    B = np.linalg.norm(points[2] - points[4])
    C = np.linalg.norm(points[0] - points[3])
    return (A + B) / (2.0 * C)

# -------------------- STORE DATA --------------------
def store_data(user_id, drowsiness_score, confidence):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    vector = np.random.rand(384).tolist()

    try:
        index.upsert(
            vectors=[
                {
                    "id": f"{user_id}_{timestamp}",
                    "values": vector,
                    "metadata": {
                        "drowsiness_score": float(drowsiness_score),
                        "confidence": float(confidence),
                        "timestamp": timestamp
                    }
                }
            ]
        )
    except Exception as e:
        st.error(f"❌ Pinecone Error: {e}")

# -------------------- DROWSINESS DETECTION --------------------
def detect_drowsiness():
    stframe = st.empty()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("❌ Webcam not accessible")
        return

    stop = st.button("❌ Stop Detection")
    last_alert_time = 0
    welcome_played = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or stop:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame)

        if not welcome_played:
            threading.Thread(target=play_welcome_sound).start()
            welcome_played = True

        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            landmarks = {
                i: (
                    int(lm.x * frame.shape[1]),
                    int(lm.y * frame.shape[0])
                )
                for i, lm in enumerate(face_landmarks.landmark)
            }

            left_ear = calculate_ear(landmarks, LEFT_EYE)
            right_ear = calculate_ear(landmarks, RIGHT_EYE)
            avg_ear = (left_ear + right_ear) / 2
            confidence = round((1 - avg_ear) * 100, 2)

            if avg_ear < 0.22 and time.time() - last_alert_time > 5:
                st.warning(f"⚠️ Drowsiness Detected | Confidence: {confidence}%")
                store_data("user_123", avg_ear, confidence)
                threading.Thread(target=play_alert).start()
                last_alert_time = time.time()

        stframe.image(frame, channels="RGB")

    cap.release()

# -------------------- ADMIN DASHBOARD --------------------
def admin_dashboard():
    st.subheader("📊 Admin Dashboard – Analytics")

    try:
        response = index.query(
            vector=np.random.rand(384).tolist(),
            top_k=100,
            include_metadata=True
        )

        if not response.matches:
            st.warning("No records found")
            return

        df = pd.DataFrame([m.metadata for m in response.matches])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp", ascending=False)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(df)

        with col2:
            fig, ax = plt.subplots()
            sns.histplot(df["drowsiness_score"], bins=10, kde=True, ax=ax)
            ax.set_title("Drowsiness Score Distribution")
            st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Dashboard Error: {e}")

# -------------------- AUTH --------------------
st.sidebar.title("🔐 Authentication")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login = st.sidebar.button("Login")

if login:
    if username == "admin" and password == "admin123":
        st.session_state["auth"] = "admin"
        st.sidebar.success("Admin Logged In")
    elif username == "user" and password == "user123":
        st.session_state["auth"] = "user"
        st.sidebar.success("User Logged In")
    else:
        st.sidebar.error("Invalid Credentials")

# -------------------- ROUTING --------------------
if "auth" in st.session_state:
    page = st.sidebar.radio("Navigation", ["User", "Admin"])

    if page == "User":
        st.title("🚗 Driver Drowsiness Detection")
        st.write("Real-time EAR-based drowsiness monitoring with alerts.")
        if st.button("▶ Start Detection"):
            detect_drowsiness()

    elif page == "Admin":
        st.title("📊 Admin Dashboard")
        admin_dashboard()
else:
    st.warning("Please login to continue")
