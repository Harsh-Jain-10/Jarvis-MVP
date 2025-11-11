# jarvis/jarvis.py -
import pyttsx3
import threading
import os
import requests
import json
import webbrowser
import ollama 
from dotenv import load_dotenv
from collections import deque 
import notes
import system_utils 

# Load environment variables
load_dotenv()

# --- Global State Variables ---
tts_engine = None
TTS_ENABLED = True
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OLLAMA_MODEL = 'llama3:8b' # Ensure this matches your pulled model
# Fixed-size queue for conversation history (User and Jarvis replies)
# Stores up to 6 turns (3 user queries, 3 assistant replies)
CONVERSATION_HISTORY = deque(maxlen=6) 


# --- Server TTS Implementation (pyttsx3) ---

def _init_tts_engine():
    """Initializes the pyttsx3 engine."""
    global tts_engine 
    global TTS_ENABLED
    try:
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate + 20)
        
        print("Jarvis TTS Engine Initialized.")
        tts_engine = engine 
        TTS_ENABLED = True
        return engine
    except Exception as e:
        print(f"FATAL: pyttsx3 initialization failed. Server speech disabled. Error: {e}")
        TTS_ENABLED = False
        return None

def speak(text):
    """
    Server-side TTS wrapper that runs in a separate thread 
    to prevent blocking the Flask main thread.
    """
    global TTS_ENABLED

    if not TTS_ENABLED:
        print(f"Server Speak (Disabled): {text}")
        return

    def run_speak():
        global tts_engine 
        
        if tts_engine is None:
            _init_tts_engine() 
            if tts_engine is None:
                return 
        
        try:
            tts_engine.say(text)
            tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS Engine Error during runAndWait: {e}. Attempting re-initialization.")
            _init_tts_engine() 

    threading.Thread(target=run_speak, daemon=True).start()


# --- Intent Detection Heuristic ---

def detect_intent(query: str) -> str:
    q_lower = query.lower()
    
    # 1. System Control 
    system_keywords = ["open", "start", "launch", "shutdown", "restart", "screenshot", "folder", "directory", "cancel shutdown", "day today", "date today", "time now", "current time"]
    if any(keyword in q_lower for keyword in system_keywords):
        return "system"

    # 2. Notes/Reminders
    notes_keywords = ["note", "remind", "remember", "list notes", "show notes", "clear notes"]
    if any(keyword in q_lower for keyword in notes_keywords):
        return "notes"
        
    # 3. Real-time Web Data 
    web_keywords = ["weather", "news", "temperature", "aqi", "air quality", "stock price", "latest news"]
    if any(keyword in q_lower for keyword in web_keywords):
        return "web"

    # 4. Default: Conversational Chat
    return "chat"


# --- Web Handler ---

def get_weather(city: str) -> str:
    """Fetches weather data using OpenWeatherMap API."""
    if not OPENWEATHER_API_KEY:
        error_msg = "Error: OpenWeatherMap API key not found in .env. Cannot get live weather."
        print(error_msg)
        return error_msg
        
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    url = f"{base_url}q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() 
        data = response.json()
        
        if data.get("cod") != 200:
            return f"Could not find weather data for {city}. Please check the city name."

        main = data["main"]
        weather = data["weather"][0]
        
        temperature = main["temp"]
        description = weather["description"]
        
        reply = f"The temperature in {city} is {temperature:.1f} degrees Celsius with {description}."
        return reply

    except requests.exceptions.RequestException as e:
        print(f"Weather API Error: {e}")
        return f"I encountered a network error while trying to fetch the weather for {city}."
    except Exception as e:
        print(f"General Weather Error: {e}")
        return f"An unexpected error occurred while processing the weather data."


def handle_web_query(query):
    """Handles real-time web queries (Weather, AQI, Search)."""
    q_lower = query.lower()
    
    # 1. Weather Query
    if "weather" in q_lower or "temperature" in q_lower:
        # ... (Existing weather logic) ...
        parts = query.split("in ")
        city = "Sonipat" 
        if len(parts) > 1:
            city = parts[-1].split("?")[0].strip()
        
        weather_reply = get_weather(city)
        speak(weather_reply)
        return weather_reply

    # 2. AQI and General Search Fallback 
    elif "aqi" in q_lower or "air quality" in q_lower:
        # Force a web search for AQI 
        search_query = query.replace("what is", "").replace("search for", "").strip()
        search_url = f"https://www.google.com/search?q={search_query}"
        
        try:
            webbrowser.open_new_tab(search_url)
            reply = f"I opened a Google search for the latest Air Quality data for: {search_query}"
            speak(reply)
            return reply
        except Exception as e:
            reply = f"I tried to search the web but failed to launch the browser: {e}"
            speak(reply)
            return reply

    # 3. General Search Fallback
    else:
        search_query = query.replace("who is", "").replace("what is", "").replace("search for", "").strip()
        search_url = f"https://www.google.com/search?q={search_query}"
        
        try:
            webbrowser.open_new_tab(search_url)
            reply = f"I opened a Google search for: {search_query}"
            speak(reply)
            return reply
        except Exception as e:
            reply = f"I tried to search the web but failed to launch the browser: {e}"
            speak(reply)
            return reply
# --- System Handler ---

def handle_system_command(query):
    """Routes and executes the appropriate system utility."""
    q_lower = query.lower()
    response = "" # Initialize response variable

    # --- Time/Date Logic (Highest Priority) ---
    if "date" in q_lower or "day" in q_lower or "time" in q_lower:
        response = system_utils.get_current_datetime(query)
    
    # --- System Action Logic ---
    elif "open" in q_lower or "start" in q_lower or "launch" in q_lower:
        response = system_utils.open_app(query)
    elif "create folder" in q_lower or "make directory" in q_lower:
        response = system_utils.create_folder(query)
    elif "screenshot" in q_lower or "take a picture" in q_lower:
        response = system_utils.take_screenshot()
    elif "cancel shutdown" in q_lower:
        response = system_utils.cancel_shutdown()
    elif "shutdown" in q_lower:
        response = system_utils.shutdown()
    elif "restart" in q_lower:
        response = system_utils.restart()
    
    # --- Fallbacks ---
    elif "folder" in q_lower or "directory" in q_lower:
        response = "I detected a command about a folder, but I only know how to 'create folder' right now. I do not have a delete function."
    else:
        # If the intent detector said "system" but none of the commands matched, reply with LLM assistance suggestion.
        response = "I detected a system command, but I'm not sure which one to execute. Try asking for chat advice instead."
        
    speak(response)
    return response

# --- Notes Handler ---

def handle_notes_command(query):
    """Routes and executes the appropriate notes action."""
    q_lower = query.lower()
    
    if "clear notes" in q_lower or "delete notes" in q_lower:
        response = notes.clear_notes()
    elif "read notes" in q_lower or "show notes" in q_lower or "list notes" in q_lower:
        full_list = notes.read_notes() 
        speak_text = full_list.split('\n', 1)[0]
        speak(speak_text)
        return full_list
    elif "note" in q_lower or "remind" in q_lower:
        response = notes.add_note(query)
    else:
        response = "I detected a notes command, but I need a clear action like 'add note' or 'read notes'."
        
    speak(response)
    return response

# --- Ollama Chat Handler (WITH CONTEXT MEMORY) ---

def handle_chat_query(query):
    """Handles conversational queries using the local Ollama LLM, with history."""
    
    global CONVERSATION_HISTORY

    try:
        # 1. Check if Ollama is running
        requests.get("http://localhost:11434", timeout=1)
    except requests.exceptions.RequestException:
        fallback_message = f"Local model offline. Start Ollama with: ollama run {OLLAMA_MODEL} or ask me to search the web."
        print(fallback_message)
        speak("My local model is currently offline. I can only perform web or system commands right now.")
        return fallback_message
    
    # 2. Build the message list for Ollama (System prompt + History + Current Query)
    
    messages = [{"role": "system", "content": "You are Jarvis, a helpful, concise, and slightly formal AI assistant. Do not repeat the same joke in the same conversation."}]

    # Add conversation history
    for role, content in CONVERSATION_HISTORY:
        messages.append({"role": role, "content": content})
        
    # Add current user query
    messages.append({"role": "user", "content": query})

    # 3. Send request to Ollama
    try:
        client = ollama.Client(host='http://localhost:11434')
        
        response = client.chat(
            model=OLLAMA_MODEL, 
            messages=messages,
            options={'temperature': 0.7}
        )
        
        reply_text = response['message']['content'].strip()
        
        # 4. Update history
        # History is stored as (role, content) tuples
        CONVERSATION_HISTORY.append(("user", query))
        CONVERSATION_HISTORY.append(("assistant", reply_text))
        
        speak(reply_text)
        return reply_text
        
    except Exception as e:
        error_msg = f"Ollama Error: Failed to generate response from model {OLLAMA_MODEL}. Error: {e}"
        print(error_msg)
        speak("I ran into an issue while generating a smart reply.")
        return error_msg


# --- Main Entry Point ---

def process_text_query(query: str) -> str:
    """
    Main function to process the user query, route the intent, and return a reply.
    """
    intent = detect_intent(query)
    
    print(f"[Jarvis] Intent detected: {intent} for query: '{query}'")
    
    if intent == "system":
        return handle_system_command(query)
    elif intent == "notes":
        return handle_notes_command(query)
    elif intent == "web":
        return handle_web_query(query)
    else: # intent == "chat"

        return handle_chat_query(query)



