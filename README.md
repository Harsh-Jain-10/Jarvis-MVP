## 🤖 Jarvis-MVP: Voice Assistant Core

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask-black)](https://flask.palletsprojects.com/)
[![LLM](https://img.shields.io/badge/LLM-Ollama_Llama3-success)](https://ollama.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)

A powerful, voice-first personal assistant MVP (Minimum Viable Product) built primarily for **local control and privacy**. **Jarvis-MVP** showcases a robust architecture that routes chat via **Ollama (offline LLM)** and uses native Python modules for system automation, all within a sleek, minimalist web interface.

---

### ✨ Key Features & Technical Highlights

| Component | Description | Technical Achievement |
| :--- | :--- | :--- |
| **🎙️ Voice-First UI** | Sleek, minimalist interface with a central glowing orb, designed for **continuous, hands-free interaction**. | Custom CSS/JS animations and Web Speech API integration. |
| **🧠 Local LLM Chat** | Handles complex, conversational queries using the **Ollama Llama 3** model, ensuring fast, private, and zero-cost responses. | `ollama-python` client integration. |
| **📚 Contextual Memory** | Implements a fixed-size **conversation history** (`deque`) to give the LLM memory, eliminating repetitive answers and improving conversational flow. | State management within the stateless Flask environment. |
| **💻 Local System Control**| Executes commands directly on the host PC for system automation (e.g., **Screenshot, Open App, Shutdown**). | Uses `pyautogui`, `webbrowser`, and `os` for desktop interaction. |
| **⏱️ Real-Time Clock** | Retrieves the **local date and time** instantly using internal Python libraries, bypassing the LLM. | Ensures essential time queries are fast and accurate. |
| **🌐 Web Data** | Uses **OpenWeatherMap API** for live weather data and gracefully falls back to a Google search for general web facts. | Robust API handling with secure `.env` key loading. |

---

### ⚙️ Setup & Installation

#### 1. Prerequisites

You must have the following software installed:

* **Python 3.8+**
* **Ollama Server:** Installed and running in the background. (Recommended model: `ollama pull llama3:8b`).

#### 2. Project Setup

1.  Clone or download this repository.
2.  Open your terminal inside the project's root directory (`jarvis/`).
3.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

#### 3. Configuration

Create a file named **`.env`** in the `jarvis/` root folder to store API keys securely.

```text
# Obtain a free API key from OpenWeatherMap
OPENWEATHER_API_KEY=YOUR_OPENWEATHERMAP_API_KEY_HERE
