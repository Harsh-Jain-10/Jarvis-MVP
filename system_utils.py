# jarvis/system_utils.py 
import subprocess
import os
import platform
import webbrowser
import pyautogui
from datetime import datetime

# --- Utility Functions---
# jarvis/system_utils.py (Ensure this is at the top)
from datetime import datetime 


def get_current_datetime(query: str) -> str:
    """Returns the current day, date, and time using the live system clock."""
    
    # This line fetches the time from your computer's operating system
    now = datetime.now()
    
    q_lower = query.lower()
    
    # Default reply format
    reply = now.strftime("The current date is %A, %B %d, %Y, and the time is %I:%M %p.")

    if "date" in q_lower and "time" not in q_lower:
        reply = now.strftime("Today is %A, %B %d, %Y.")
    elif "time" in q_lower and "date" not in q_lower:
        reply = now.strftime("The current time is %I:%M %p.")
    
    # Time Zone context
    reply += " (Time Zone: IST)." 
        
    return reply

# ... (rest of system_utils.py) ...

def open_app(name: str) -> str:
    """Attempts to open a program or file based on the OS."""
    
    name = name.lower().replace('open', '').replace('start', '').strip()
   
    if platform.system() == "Windows":
        if "calculator" in name:
            os.startfile("calc.exe")
        elif "notepad" in name:
            os.startfile("notepad.exe")
        
        else:
            try:
                subprocess.Popen(name)
                return f"Attempting to open {name}..."
            except FileNotFoundError:
                return f"Could not find or open the application: {name}"

    elif platform.system() == "Darwin" or platform.system() == "Linux":
        try:
            subprocess.Popen(['open', name])
        except FileNotFoundError:
            try:
                subprocess.Popen(['xdg-open', name])
            except:
                return f"Could not find or open the application: {name}"
    
    return f"Opened {name}."


def create_folder(name: str) -> str:
    """Creates a new folder in the user's Desktop directory."""
    
    name = name.replace("create folder", "").replace("make directory", "").strip()
    folder_name = f"Jarvis_Folder_{datetime.now().strftime('%Y%m%d_%H%M%S')}" if not name else name.replace(" ", "_")
    
   
    if platform.system() == "Windows":
      
        try:
           
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            path = os.path.join(desktop, folder_name)
            os.makedirs(path, exist_ok=True)
            return f"Folder '{folder_name}' created on the Desktop at: {desktop}."
        except Exception as e:

            try:
                target_drive_desktop = os.path.join("D:", "Desktop")
                path = os.path.join(target_drive_desktop, folder_name)
                os.makedirs(path, exist_ok=True)
                return f"Folder '{folder_name}' created on D-Drive Desktop at: {target_drive_desktop}."
            except Exception as fallback_e:
                
                project_root = os.path.dirname(os.path.abspath(__file__))
                path = os.path.join(project_root, folder_name)
                os.makedirs(path, exist_ok=True)
                return f"Folder '{folder_name}' created in project root as Desktop path was inaccessible. Path: {project_root}"
    
    # --- Linux/macOS path logic ---
    else:
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        path = os.path.join(desktop, folder_name)
        try:
            os.makedirs(path, exist_ok=True)
            return f"Folder '{folder_name}' created on the Desktop."
        except Exception as e:
             return f"Failed to create folder: {e}"


def take_screenshot() -> str:
    """Takes a screenshot and saves it to the user's Downloads folder."""
    try:
        screenshot = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if platform.system() == "Windows":

            target_dir = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        else:

            target_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            

        os.makedirs(target_dir, exist_ok=True)
        
        filename = os.path.join(target_dir, f"Jarvis_Screenshot_{timestamp}.png")
        
        screenshot.save(filename)
        return f"Screenshot saved to your Downloads folder: {os.path.basename(filename)}"
    except Exception as e:
        return f"Failed to take screenshot. Error: {e}. Check if dependencies like PIL are installed."

# --- Power Control 
# ... (shutdown, cancel_shutdown, restart functions )
def shutdown() -> str:
    # ... (code) ...
    if platform.system() == "Windows":
        os.system("shutdown /s /t 60")
        return "System scheduled for shutdown in 1 minute. Say 'cancel shutdown' to stop."
    # ... (rest of the system_utils file)
    elif platform.system() in ["Linux", "Darwin"]:
        os.system("shutdown -h +1")
        return "System scheduled for shutdown in 1 minute. Say 'cancel shutdown' to stop."
    else:
        return "Shutdown command not supported on this OS."

def cancel_shutdown() -> str:
    if platform.system() == "Windows":
        os.system("shutdown /a")
        return "Scheduled shutdown cancelled."
    elif platform.system() in ["Linux", "Darwin"]:
        os.system("shutdown -c")
        return "Scheduled shutdown cancelled."
    else:
        return "Shutdown command not supported on this OS."

def restart() -> str:
    if platform.system() == "Windows":
        os.system("shutdown /r /t 60")
        return "System scheduled for restart in 1 minute. Say 'cancel shutdown' to stop."
    elif platform.system() in ["Linux", "Darwin"]:
        os.system("shutdown -r +1")
        return "System scheduled for restart in 1 minute. Say 'cancel shutdown' to stop."
    else:

        return "Restart command not supported on this OS."



