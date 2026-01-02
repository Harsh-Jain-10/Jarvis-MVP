import speech_recognition as sr
import datetime
import os
import webbrowser
import pyautogui
import subprocess
import requests
from chat_ai import chat_with_jarvis

# ================= WINDOWS NATIVE VOICE =================
def speak(text):
    clean = text.replace('"', '').replace("\n", " ").strip()
    print("Jarvis:", clean)

    command = f'''
    Add-Type -AssemblyName System.Speech;
    $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $speak.Speak("{clean}");
    '''

    subprocess.run(
        ["powershell", "-Command", command],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

# ================= VOICE INPUT =================
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎙️ Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You:", text)
        return text.lower()
    except:
        return ""

# ================= WEATHER (FIXED) =================
def get_weather(city):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code != 200:
            return "Unable to fetch weather information."

        return f"The current weather is {response.text}"

    except:
        return "Weather service is currently unavailable."

# ================= CONFIRMATION =================
def confirm_action():
    speak("Are you sure? Please say yes or no.")
    reply = listen()
    return "yes" in reply

# ================= GREETING =================
hour = datetime.datetime.now().hour
if hour < 12:
    speak("Good morning everyone. Jarvis is online and ready to assist.")
elif hour < 18:
    speak("Good afternoon everyone. Jarvis is online and ready to assist.")
else:
    speak("Good evening everyone. Jarvis is online and ready to assist.")

# ================= MAIN LOOP =================
while True:
    command = listen()

    if command == "":
        continue

    # EXIT
    if "exit" in command or "stop" in command:
        speak("Goodbye.")
        break

    # DATE AND TIME
    elif "date and time" in command:
        today = datetime.date.today().strftime("%B %d, %Y")
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Today is {today} and the time is {now}.")

    # DATE ONLY
    elif "date" in command:
        today = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today is {today}.")

    # TIME ONLY
    elif "time" in command and "define" not in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}.")

    # DEFINE TIME (LOCAL)
    elif "define time" in command:
        speak(
            "Time is a fundamental concept used to measure the sequence "
            "and duration of events."
        )

    # SCREENSHOT
    elif "screenshot" in command:
        os.makedirs("screenshots", exist_ok=True)
        pyautogui.screenshot(
            f"screenshots/screenshot_{int(datetime.datetime.now().timestamp())}.png"
        )
        speak("Screenshot taken successfully.")

    # OPEN CALCULATOR
    elif "calculator" in command:
        os.system("calc")
        speak("Opening calculator.")

    # OPEN CAMERA
    elif "camera" in command:
        os.system("start microsoft.windows.camera:")
        speak("Opening camera.")

    # OPEN WHATSAPP
    elif "whatsapp" in command:
        os.system("start whatsapp:")
        speak("Opening WhatsApp.")

    # OPEN GOOGLE
    elif "open google" in command or "open chrome" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google Chrome.")

    # SEARCH
    elif command.startswith("search"):
        query = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching for {query}.")

    # WEATHER
    elif "weather" in command:
        words = command.split()
        if "in" in words:
            city = words[words.index("in") + 1]
            speak(get_weather(city))
        else:
            speak("Please tell me the city name.")

    # SHUTDOWN (REAL, SAFE)
    elif "shutdown" in command:
        if confirm_action():
            speak("Shutting down the system.")
            os.system("shutdown /s /t 5")

    # AI CHAT (LAST RESORT)
    else:
        reply = chat_with_jarvis(command)
        speak(reply)
