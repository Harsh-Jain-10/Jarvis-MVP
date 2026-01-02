# Jarvis - AI Voice Assistant

A Python-based voice-controlled AI assistant inspired by Iron Man's J.A.R.V.I.S. This assistant can perform various tasks through voice commands, including system control, web searches, weather updates, and AI-powered conversations.

## Features

- 🎤 Voice recognition and text-to-speech
- 🤖 AI-powered conversations using Ollama
- 🌤️ Real-time weather information
- 📸 Screenshot capture
- 🔍 Web search functionality
- 💻 System control (shutdown, restart, sleep)
- 📱 Application launcher
- ⏰ Date and time queries

## Project Structure

## 🎯 How It Works

1. **Start**: Run the program
2. **Listen**: JARVIS automatically starts listening
3. **Speak**: Say your command naturally
4. **Respond**: JARVIS speaks the answer
5. **Repeat**: JARVIS keeps listening for next command
6. **Exit**: Say "bye" to stop

**That's it!** No menus, no choices, pure voice interaction.

## 🚀 Installation

### Windows Installation (Step-by-Step)

#### 1. Install Python
- Download Python 3.7+ from https://www.python.org/downloads/
- **Important**: Check "Add Python to PATH" during installation

#### 2. Install PyAudio (Required for Microphone)

Open Command Prompt and run:

```bash
pip install pipwin
pipwin install pyaudio
```

**If above doesn't work**, download PyAudio wheel:
- Go to: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- Download file matching your Python version
- Example: `PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl` for Python 3.9
- Install: `pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl`

#### 3. Install Other Dependencies

```bash
pip install -r requirements.txt
```

#### 4. (Optional) Setup Weather API
- Get free key from: https://openweathermap.org/api
- Create `.env` file with: `WEATHER_API_KEY=your_key_here`

#### 5. Test Your Microphone
- Make sure microphone is connected and working
- Go to Windows Settings → Privacy → Microphone → Allow apps

## ▶️ Run JARVIS

```bash
python main.py
```

**That's it!** Start speaking after you see "Listening..."

## 🎤 Example Conversation

```
======================================================================
       🤖 JARVIS Voice Assistant - Continuous Mode 🤖
======================================================================

🔧 Initializing voice engine...
✅ Voice engine ready!

JARVIS: Hello! I am JARVIS, your voice assistant. I'm ready to help you.

🎤 Listening... (speak now)
You said: hello jarvis
JARVIS: Hello! I'm JARVIS. How can I assist you today?

🎤 Listening... (speak now)
You said: what's the weather in sonipat
JARVIS: Weather in Sonipat: Temperature 25°C, Clear sky, Humidity 60%

🎤 Listening... (speak now)
You said: search for python tutorials
JARVIS: Searching Google for 'python tutorials' in Chrome...

🎤 Listening... (speak now)
You said: open notepad
JARVIS: Opening notepad...

🎤 Listening... (speak now)
You said: who is elon musk
JARVIS: [Speaks Wikipedia summary about Elon Musk]

🎤 Listening... (speak now)
You said: bye
JARVIS: Goodbye! Have a great day!

👋 Exiting JARVIS...
```

## ⚙️ Customize Voice

Edit `config.py`:

```python
# Voice speed (words per minute)
VOICE_RATE = 150  # Try: 120 (slower) or 180 (faster)

# Voice volume (0.0 to 1.0)
VOICE_VOLUME = 0.9  # Try: 0.5 (quieter) or 1.0 (max)

# Listening timeout (seconds)
MICROPHONE_TIMEOUT = 5  # How long to wait for speech
```

## 🛠️ Troubleshooting

### "No speech detected"
**Problem**: JARVIS doesn't hear you
**Solution**:
- Check if microphone is connected and not muted
- Speak louder and clearer
- Reduce background noise
- Increase `MICROPHONE_TIMEOUT` in `config.py`

### "Couldn't understand what you said"
**Problem**: Speech not recognized
**Solution**:
- Speak more slowly and clearly
- Move closer to microphone
- Check internet connection (speech recognition needs internet)
- Reduce background noise

### PyAudio Installation Failed
**Problem**: Can't install PyAudio
**Solution**:
- Use pipwin method (see installation steps)
- Or download wheel file manually
- Make sure you have Visual C++ installed

### No Voice Output
**Problem**: Can't hear JARVIS
**Solution**:
- Check system volume
- Check speaker/headphone connection
- Verify text-to-speech engine in Windows

### Internet Connection Error
**Problem**: "Could not request results"
**Solution**:
- Voice recognition needs internet
- Check your connection
- Try again after internet is back

## 🎯 Tips for Best Experience

### Speaking
✅ Speak clearly at normal pace
✅ Wait for "Listening..." before speaking
✅ Pause briefly between commands
✅ Use natural language (no robotic speech needed)

### Commands
✅ Be specific: "Weather in Delhi" not just "Weather"
✅ Use full names: "Open Google Chrome" not just "Chrome"
✅ For questions, use complete sentences


JARVIS will automatically recognize voice commands for it!

## 📋 File Structure

```
project/
├── main.py              # Continuous voice loop
├── voice_utils.py       # Voice input/output
├── assistant_core.py    # Command processing
├── system_utils.py      # System operations
├── web_utils.py        # Web searches
├── realtime_utils.py   # Weather & knowledge
├── config.py           # Settings
├── requirements.txt    # Dependencies
└── README.md          # This guide
```

## 🚦 Exit Options

1. **Say "Bye"**: Proper exit (recommended)
2. **Press Ctrl+C**: Force quit
3. **Close window**: Emergency exit

## ⚠️ Important Notes

- **Internet Required**: For voice recognition and weather
- **Microphone Required**: Must have working microphone
- **Windows Only**: Designed for Windows (modify for Mac/Linux)
- **Shutdown Works**: Be careful with shutdown commands!
- **Background Noise**: Works best in quiet environment

## 📊 Technology Used

- **pyttsx3**: Text-to-speech (offline)
- **SpeechRecognition**: Speech-to-text (online)
- **PyAudio**: Microphone access
- **Google Speech API**: Voice recognition (free)

## 🎬 Quick Start Guide

```bash
# 1. Install Python 3.7+
# 2. Install PyAudio
pip install pipwin
pipwin install pyaudio

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run JARVIS
python main.py

# 5. Start speaking!
```

## 💡 Example Commands to Try

```
"Hello Jarvis"
"What can you do"
"Weather in [your city]"
"Search for news today"
"Open calculator"
"Who is Bill Gates"
"Tell me about India"
"List all apps"
"Help"
"Bye"
```


## 🤝 Customize Further

Want to make it even better?

1. **Add wake word**: Modify `voice_utils.py` to activate with "Hey Jarvis"
2. **Change voice**: Edit `initialize_tts()` to select different voices
3. **Add commands**: Edit `assistant_core.py` to add new features
4. **Adjust sensitivity**: Modify `MICROPHONE_TIMEOUT` in `config.py`

---

**🎤 Now you have a true hands-free voice assistant! 🤖**

**Just run it, and start talking - no menus, no choices, just pure voice interaction!**

---

## 👥 Authors

- **Harsh Jain** - Initial work

---
