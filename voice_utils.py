"""
Voice utilities for JARVIS Assistant
Handles voice input (speech recognition) and voice output (text-to-speech)
"""

import pyttsx3
import speech_recognition as sr
from config import VOICE_RATE, VOICE_VOLUME, MICROPHONE_TIMEOUT, MICROPHONE_PHRASE_LIMIT


# Initialize text-to-speech engine globally
tts_engine = None

def initialize_tts():
    """
    Initializes the text-to-speech engine
    This is called once when the program starts
    """
    global tts_engine
    
    try:
        # Create TTS engine
        tts_engine = pyttsx3.init()
        
        # Set voice properties
        tts_engine.setProperty('rate', VOICE_RATE)  # Speed of speech
        tts_engine.setProperty('volume', VOICE_VOLUME)  # Volume level
        
        # Try to set a good voice (optional)
        voices = tts_engine.getProperty('voices')
        if len(voices) > 0:
            # Use first available voice (usually default)
            tts_engine.setProperty('voice', voices[0].id)
        
        return True
    
    except Exception as e:
        print(f"Error initializing text-to-speech: {str(e)}")
        return False


def speak(text):
    """
    Converts text to speech and speaks it out loud
    This is how JARVIS talks to you
    """
    global tts_engine
    
    try:
        # Initialize TTS if not already done
        if tts_engine is None:
            initialize_tts()
        
        if tts_engine:
            print(f"\nJARVIS: {text}")  # Also print to console
            tts_engine.say(text)
            tts_engine.runAndWait()
        else:
            # If TTS fails, at least print the text
            print(f"\nJARVIS: {text}")
    
    except Exception as e:
        # If speaking fails, just print
        print(f"\nJARVIS: {text}")
        print(f"(Speech output error: {str(e)})")


def listen():
    """
    Listens to microphone and converts speech to text
    This is how JARVIS hears you
    Returns the text heard, or None if nothing was heard
    """
    # Create recognizer object
    recognizer = sr.Recognizer()
    
    try:
        # Use microphone as source
        with sr.Microphone() as source:
            print("\n🎤 Listening... (speak now)")
            
            # Adjust for ambient noise (makes recognition better)
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Listen for audio
            audio = recognizer.listen(
                source, 
                timeout=MICROPHONE_TIMEOUT,
                phrase_time_limit=MICROPHONE_PHRASE_LIMIT
            )
            
            print("🔄 Processing your speech...")
            
            # Convert speech to text using Google Speech Recognition
            text = recognizer.recognize_google(audio)
            
            print(f"You said: {text}")
            return text
    
    except sr.WaitTimeoutError:
        print("⏰ No speech detected. Please try again.")
        return None
    
    except sr.UnknownValueError:
        print("❌ Sorry, I couldn't understand what you said. Please try again.")
        return None
    
    except sr.RequestError as e:
        print(f"❌ Could not request results from speech recognition service: {str(e)}")
        print("Make sure you have an internet connection.")
        return None
    
    except Exception as e:
        print(f"❌ Error while listening: {str(e)}")
        return None


def listen_for_wake_word(wake_word="jarvis"):
    """
    Continuously listens for the wake word (like "Jarvis")
    Returns True when wake word is detected
    """
    recognizer = sr.Recognizer()
    
    print(f"\n👂 Listening for wake word '{wake_word}'... (say '{wake_word}' to activate)")
    
    try:
        with sr.Microphone() as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Listen for audio
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            
            # Convert to text
            text = recognizer.recognize_google(audio).lower()
            
            # Check if wake word is in the text
            if wake_word in text:
                print(f"✅ Wake word detected: '{text}'")
                return True
            else:
                return False
    
    except:
        return False