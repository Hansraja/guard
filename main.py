import sqlite3
import os
import cv2
import face_recognition
import pyttsx3
import speech_recognition as sr
import numpy as np
import pickle
from datetime import datetime

# Create a connection to the SQLite database
conn = sqlite3.connect('security_guard.db')
cursor = conn.cursor()

# Create a table to store user data
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    face_encoding BLOB,
    image_path TEXT
)
''')
conn.commit()

# Initialize the speech engine for text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)
engine.setProperty('voice', engine.getProperty('voices')[1].id)  # Choose a different voice

def speak_text(text):
    """Speak out the provided text."""
    engine.say(text)
    engine.runAndWait()

def listen_to_user():
    """Listen to the user's input and return as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            speak_text("Sorry, I didn't understand that. Please repeat.")
            return listen_to_user()

def add_user(name, email, phone, face_encoding, image_path):
    """Add a new user with the provided details into the database."""
    cursor.execute('''
    INSERT INTO users (name, email, phone, face_encoding, image_path)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, email, phone, face_encoding, image_path))
    conn.commit()

def fetch_users():
    """Fetch all users and their face encodings from the database."""
    cursor.execute('SELECT name, face_encoding FROM users')
    return cursor.fetchall()

def load_known_users():
    """Load all known users and their face encodings."""
    users = fetch_users()
    known_face_encodings = [pickle.loads(user[1]) for user in users]  # Deserialize face encodings
    known_names = [user[0] for user in users]
    return known_face_encodings, known_names

def scan_faces():
    """Capture faces from the camera and return their encodings."""
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    video_capture.release()

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    
    return frame, face_encodings

def recognize_user(known_face_encodings, face_encoding):
    """Check if the face encoding matches a known user."""
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    return any(matches)

def save_user_image(frame, user_id):
    """Save the user's image and return the path."""
    if not os.path.exists('user_images'):
        os.makedirs('user_images')
    image_path = f"user_images/user_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    cv2.imwrite(image_path, frame)
    return image_path

def capture_new_user_info(face_encoding, frame):
    """Capture new user information and add them to the database."""
    speak_text("You are not recognized. Please provide your name.")
    name = listen_to_user()

    speak_text("Please provide your email.")
    email = listen_to_user()

    speak_text("Please provide your phone number.")
    phone = listen_to_user()

    user_image_path = save_user_image(frame, name)
    add_user(name, email, phone, pickle.dumps(face_encoding), user_image_path)

    speak_text(f"Thank you {name}, you are now added to the system.")
    return name

def process_faces(frame, face_encodings, known_face_encodings, known_names):
    """Process each face in the frame and either recognize or add a new user."""
    for face_encoding in face_encodings:
        if recognize_user(known_face_encodings, face_encoding):
            user_index = face_recognition.compare_faces(known_face_encodings, face_encoding).index(True)
            speak_text(f"Welcome back, {known_names[user_index]}. You are allowed to enter.")
        else:
            capture_new_user_info(face_encoding, frame)
            speak_text("Access granted to new user.")

def security_guard():
    """Main function for the robotic security guard."""
    speak_text("Hi, I am Guardia, your smart security system.")
    
    # Load known users
    known_face_encodings, known_names = load_known_users()

    # Scan for faces
    speak_text("Please look at the camera.")
    frame, face_encodings = scan_faces()

    if face_encodings:
        process_faces(frame, face_encodings, known_face_encodings, known_names)
    else:
        speak_text("No face detected. Please try again.")
        security_guard()  # Retry scanning

# Run the security guard
security_guard()
