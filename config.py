"""
Configuration file for JARVIS Assistant
This file manages API keys and settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file (if exists)
load_dotenv()

# OpenWeatherMap API key (optional)
# Get your free API key from: https://openweathermap.org/api
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")

# If no API key is provided, weather feature will show a message
# But the assistant will still work for other features

# Common application paths for Windows
# Add more applications as needed
COMMON_APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
    "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "paint": "mspaint.exe",
    "explorer": "explorer.exe",
    "cmd": "cmd.exe",
    "vscode": "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
}

# Assistant name
ASSISTANT_NAME = "JARVIS"

# Voice settings
VOICE_RATE = 150  # Speed of speech (words per minute)
VOICE_VOLUME = 0.9  # Volume (0.0 to 1.0)

# Microphone settings
MICROPHONE_TIMEOUT = 5  # Seconds to wait for speech
MICROPHONE_PHRASE_LIMIT = 10  # Maximum seconds for a single phrase