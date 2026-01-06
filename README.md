# Jarvis - AI Voice Assistant

A Python-based voice-controlled AI assistant inspired by Iron Man's J.A.R.V.I.S. This assistant can perform various tasks through voice commands, including system control, web searches, weather updates, and AI-powered conversations.

## Features

- 🎤 Voice recognition and text-to-speech
- 🤖 AI-powered conversations using Ollama
- 📸 Screenshot capture
- 🔍 Web search functionality
- 💻 System control (shutdown, restart, sleep)
- 📱 Application launcher
- ⏰ Date and time queries

## Project Structure
```
jarvis-assistant/
│
├── jarvis.py              # Main entry point and command handler
├── chat_ai.py             # AI chat integration with Ollama
├── app_launcher.py        # Application launching functionality
├── system_control.py      # System operations (shutdown, screenshot, etc.)
├── web_search.py          # Web search functionality
├── requirements.txt       # Python dependencies
└── screenshots/           # Directory for saved screenshots (auto-created)
```

## Code Structure

### `jarvis.py`
The main application file that:
- Handles voice input/output using Windows native speech synthesis
- Processes user commands and routes them to appropriate modules
- Implements core features (time, date, weather)
- Manages the main conversation loop
- Includes safety confirmations for destructive actions

### `chat_ai.py`
Manages AI conversations:
- Connects to local Ollama API (default: `http://localhost:11434`)
- Maintains conversation history for context-aware responses
- Uses Llama3 model for intelligent responses
- Handles fallback responses on errors
- Supports streaming and non-streaming responses

### `app_launcher.py`
Opens common Windows applications:
- Camera, Calculator, Chrome, Edge
- VS Code, VLC, WhatsApp
- Microsoft Store
- Returns `True` if app found, `False` otherwise

### `system_control.py`
System-level operations:
- `shutdown_pc()` - Shuts down the computer
- `restart_pc()` - Restarts the computer
- `sleep_pc()` - Puts computer to sleep
- `take_screenshot()` - Captures and saves screenshot with timestamp

### `web_search.py`
Web search functionality:
- Parses search queries from voice commands
- Opens Google search results in default browser
- Handles URL encoding for special characters
- Handles weather searches (ex- "Search Delhi's weather")

## Installation

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Ollama** installed and running locally ([Download Ollama](https://ollama.ai))
3. **Microphone** for voice input
4. **Windows OS** (uses Windows-native speech synthesis)

### Setup Steps

1. Clone or download this repository:
```bash
git clone <repository-url>
cd jarvis-assistant
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Install PyAudio (may require additional steps on Windows):
```bash
pip install pipwin
pipwin install pyaudio
```

4. Install and start Ollama with Llama3:
```bash
ollama pull llama3
ollama serve
```

5. Run the assistant:
```bash
python jarvis.py
```

## Requirements
```
SpeechRecognition
pyaudio
requests
pyautogui
```

**Note:** The following are built-in Python modules and don't need separate installation:
- `os`
- `webbrowser`
- `time`
- `datetime`
- `subprocess`

## Voice Commands

### Basic Commands
- **"exit"** or **"stop"** - Close the assistant
- **"date"** - Get current date
- **"time"** - Get current time
- **"date and time"** - Get both date and time
- **"define time"** - Get definition of time

### Applications
- **"open calculator"** - Opens Windows Calculator
- **"open camera"** - Opens Windows Camera
- **"open whatsapp"** - Opens WhatsApp desktop
- **"open google"** or **"open chrome"** - Opens Google Chrome

### Web & Search
- **"search [query]"** - Search Google for the query
  - Example: *"search Python tutorials"*
- **"search [query]"** - Search Google for the weather updates
  -  Example: *"search Gujarat's weather"*

### System Control
- **"screenshot"** - Capture and save a screenshot
- **"shutdown"** - Shutdown the computer (requires confirmation)

### AI Chat
- Any unrecognized command will be sent to the AI for a conversational response
  - Example: *"Tell me a joke"*
  - Example: *"What is artificial intelligence?"*
  
## Configuration

### Changing AI Model
Edit `chat_ai.py` to change the Ollama model:
```python
MODEL = "llama3"  # Change to "llama2", "mistral", etc.
```

### Changing Ollama URL
If Ollama is running on a different host/port:
```python
OLLAMA_URL = "http://localhost:11434/api/chat"
```

### Adding More Applications
Edit `app_launcher.py` to add more applications:
```python
apps = {
    "your_app": "command_to_launch",
    # Example: "notepad": "notepad"
}
```

## Safety Features

- **Confirmation for Destructive Actions**: Shutdown command requires voice confirmation
- **Error Handling**: Graceful fallbacks for speech recognition failures
- **Timeout Protection**: Network requests have timeout limits

## Troubleshooting

### Microphone Not Working
- Check microphone permissions in Windows Settings
- Ensure microphone is set as default input device
- Test with: `python -m speech_recognition`

### Ollama Connection Error
- Verify Ollama is running: `ollama serve`
- Check if model is downloaded: `ollama list`
- Test API: `curl http://localhost:11434/api/tags`

### Speech Synthesis Issues
- Ensure PowerShell execution policy allows scripts
- Try running PowerShell as administrator
- Check Windows Speech settings

### PyAudio Installation Issues
On Windows, use:
```bash
pip install pipwin
pipwin install pyaudio
```

## Future Enhancements

- [ ] Add support for custom wake words
- [ ] Implement email sending functionality
- [ ] Add calendar integration
- [ ] Support for multiple languages
- [ ] Add Spotify/music control
- [ ] Implement reminder system
- [ ] Add file management commands
- [ ] Create GUI dashboard

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Inspired by Marvel's J.A.R.V.I.S. from Iron Man
- Built with [Ollama](https://ollama.ai) for AI capabilities
- Uses [SpeechRecognition](https://github.com/Uberi/speech_recognition) for voice input
- Weather data from [wttr.in](https://wttr.in)

## Disclaimer

This software is for educational purposes. Use system control features (shutdown, restart) with caution. The developers are not responsible for any data loss or system issues.

## Contact

For questions or support, please open an issue in the repository.

---

**Made by Harsh Jain**
