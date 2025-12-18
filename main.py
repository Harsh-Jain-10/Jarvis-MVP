"""
JARVIS Voice Assistant - Continuous Voice Mode
A fully voice-controlled personal assistant 
"""

from assistant_core import get_response
from voice_utils import speak, listen, initialize_tts
from config import ASSISTANT_NAME


def print_welcome():
    """
    Prints a simple welcome message
    """
    print("=" * 70)
    print(f"       🤖 {ASSISTANT_NAME} Voice Assistant - Continuous Mode 🤖")
    print("=" * 70)
    print("\n🎙️  Voice-only mode active - Just start speaking!")
    print("💡 Say 'bye' or 'exit' to stop the assistant")
    print("🔇 Press Ctrl+C to force quit\n")


def main():
    """
    Main function - Continuous voice loop (no interruptions)
    JARVIS keeps listening until you say goodbye
    """
    # Show welcome message
    print_welcome()
    
    # Initialize text-to-speech engine
    print("🔧 Initializing voice engine...\n")
    
    if not initialize_tts():
        print("❌ Voice engine failed to initialize. Cannot run voice assistant.")
        return
    
    print("✅ Voice engine ready!\n")
    
    # Welcome speech
    speak(f"Hello! I am {ASSISTANT_NAME}, your voice assistant. I'm ready to help you. What can I do for you?")
    
    # Continuous voice loop
    while True:
        try:
            # Listen for user's voice command
            user_input = listen()
            
            # If nothing was heard, keep listening (don't break the loop)
            if user_input is None:
                continue
            
            # Check if user wants to exit
            if user_input.lower() in ["bye", "exit", "quit", "goodbye", "stop"]:
                speak("Goodbye! Have a great day!")
                print("\n👋 Exiting JARVIS...\n")
                break
            
            # Get response from assistant
            response = get_response(user_input)
            
            # Speak the response
            speak(response)
        
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\n\n⚠️  Interrupted by user (Ctrl+C)")
            speak("Interrupted. Goodbye!")
            break
        
        except Exception as e:
            # Handle any unexpected errors without breaking the loop
            error_msg = f"An error occurred, but I'm still listening. Please try again."
            speak(error_msg)
            print(f"Error details: {str(e)}\n")


if __name__ == "__main__":
    # Run the continuous voice assistant

    main()
