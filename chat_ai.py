import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3"

conversation = []

def chat_with_jarvis(text):
    conversation.append({"role": "user", "content": text})

    payload = {
        "model": MODEL,
        "messages": conversation,
        "stream": False
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=20)
        reply = res.json()["message"]["content"]
        conversation.append({"role": "assistant", "content": reply})
        return reply
    except:
        return "I am having trouble responding right now."
