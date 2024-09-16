import pyttsx3
import speech_recognition as sr

# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 200)  # Speed of speech
engine.setProperty('volume', 0.7)  # Volume (0.0 to 1.0)

print(engine.getProperty('voices'))

engine.setProperty('voice', engine.getProperty('voices')[1].id)  # Voice

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

speak_text('Hello mic testing.')