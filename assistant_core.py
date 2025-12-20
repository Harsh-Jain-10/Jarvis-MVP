"""
Core assistant logic for JARVIS
Handles command recognition and routing
"""

from system_utils import shutdown_system, restart_system, open_application, list_installed_apps
from web_utils import search_google, open_website
from realtime_utils import get_weather, answer_question
from config import ASSISTANT_NAME

def process_command(user_input):
    """
    Main function that processes user input and routes to appropriate functions
    This is the brain of JARVIS
    """
    # Convert input to lowercase for easier matching
    command = user_input.lower().strip()
    
    # Empty input check
    if not command:
        return "I didn't catch that. Could you please say something?"
    
    # ===== GREETING COMMANDS =====
    if any(word in command for word in ["hello", "hi", "hey", "greetings"]):
        return f"Hello! I'm {ASSISTANT_NAME}. How can I assist you today?"
    
    if "how are you" in command:
        return "I'm doing great! Ready to help you with anything you need."
    
    if any(word in command for word in ["thank", "thanks"]):
        return "You're welcome! Happy to help."
    
    if "bye" in command or "goodbye" in command:
        return "Goodbye! Have a great day!"
    
    # ===== SYSTEM COMMANDS =====
    if "shutdown" in command or "shut down" in command:
        return shutdown_system()
    
    if "restart" in command or "reboot" in command:
        return restart_system()
    
    
    # ===== OPEN APPLICATION COMMANDS =====
    if command.startswith("open "):
        # Extract application name after "open "
        app_name = command.replace("open ", "").strip()
        return open_application(app_name)
    
    
    # ===== SEARCH COMMANDS =====
    if "search for" in command or "search" in command:
        # Extract search query
        if "search for" in command:
            query = command.split("search for", 1)[1].strip()
        else:
            query = command.split("search", 1)[1].strip()
        
        if query:
            return search_google(query)
        else:
            return "What would you like me to search for?"
    
    
    # ===== WEATHER COMMANDS =====
    if "weather" in command:
        # Try to extract city name
        words = command.split()
        
        # Look for city name after "in" or "at"
        city = None
        if "in" in words:
            city_index = words.index("in") + 1
            if city_index < len(words):
                city = " ".join(words[city_index:])
        elif "at" in words:
            city_index = words.index("at") + 1
            if city_index < len(words):
                city = " ".join(words[city_index:])
        else:
            # Try to get last word as city name
            city = words[-1]
        
        if city:
            return get_weather(city)
        else:
            return "Please specify a city. For example: 'weather in Sonipat'"
    
    
    # ===== GENERAL KNOWLEDGE QUESTIONS =====
    # Check for question patterns
    question_starters = ["who is", "what is", "where is", "when is", "tell me about", "who was"]
    
    if any(command.startswith(starter) for starter in question_starters):
        return answer_question(command)
    
    
    # ===== LIST APPS COMMAND =====
    if "list apps" in command or "show apps" in command or "what apps" in command:
        apps = list_installed_apps()
        return f"I can open these applications: {', '.join(apps)}"
    
    
    # ===== HELP COMMAND =====
    if "help" in command or "what can you do" in command:
        help_text = f"""
I'm {ASSISTANT_NAME}, your personal assistant. Here's what I can do:

System Commands:
- "shutdown" - Shut down your PC
- "restart" - Restart your PC
- "open <app>" - Open an application (e.g., "open notepad")
- "list apps" - Show all apps I can open

Web Commands:
- "search for <query>" - Search Google for something
- "weather in <city>" - Get weather information

General Knowledge:
- Ask me questions like "Who is PM Modi?" or "What is Python?"

Other:
- "help" - Show this help message
- "bye" - Exit the assistant
        """
        return help_text.strip()
    
    
    # ===== DEFAULT RESPONSE =====
    # If no command matches, try to answer as a general question
    if "?" in command or len(command.split()) > 3:
        # Seems like a question, try to answer it
        return answer_question(command)
    else:
        return "I'm not sure how to help with that. Type 'help' to see what I can do."


def get_response(user_input):
    """
    Wrapper function that safely processes commands
    Ensures the assistant never crashes
    """
    try:
        response = process_command(user_input)
        return response
    except Exception as e:
        # If anything goes wrong, don't crash - return a friendly error

        return f"Oops! Something went wrong: {str(e)}. Please try again."

