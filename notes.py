# jarvis/notes.py
import os

NOTES_FILE = os.path.join(os.path.dirname(__file__), 'notes.txt')

def add_note(text: str) -> str:
    """Adds a note (text) to the notes file."""
    try:
        # Simple extraction for the note content
        note_content = text.replace("note", "", 1).replace("remind", "", 1).strip()
        if not note_content:
            return "Please tell me what you want to save as a note."
            
        timestamp = os.path.getmtime(NOTES_FILE) if os.path.exists(NOTES_FILE) else 0

        with open(NOTES_FILE, 'a', encoding='utf-8') as f:
            f.write(f"- {note_content}\n")
        
        return f"Note saved successfully: {note_content}"
    except Exception as e:
        return f"Failed to save note due to file error: {e}"

def read_notes() -> str:
    """Reads all saved notes from the notes file."""
    try:
        if not os.path.exists(NOTES_FILE) or os.stat(NOTES_FILE).st_size == 0:
            return "You have no notes saved."

        with open(NOTES_FILE, 'r', encoding='utf-8') as f:
            notes = f.read().strip()
            if not notes:
                 return "You have no notes saved."
            return "Here are your saved notes:\n" + notes
            
    except Exception as e:
        return f"Failed to read notes: {e}"

def clear_notes() -> str:
    """Clears all saved notes."""
    try:
        if os.path.exists(NOTES_FILE):
            os.remove(NOTES_FILE)
            # Recreate the file just in case, or just leave it removed
            open(NOTES_FILE, 'w').close() 
        return "All notes have been cleared."
    except Exception as e:
        return f"Failed to clear notes: {e}"