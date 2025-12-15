"""
System utilities for JARVIS Assistant
Handles system commands like shutdown, restart, and opening applications
"""

import os
import subprocess
import psutil
from config import COMMON_APPS


def shutdown_system():
    """
    Shuts down the Windows system
    """
    try:
        print("Shutting down the system...")
        os.system("shutdown /s /t 1")  # /s = shutdown, /t 1 = in 1 second
        return "System is shutting down now."
    except Exception as e:
        return f"Error shutting down: {str(e)}"


def restart_system():
    """
    Restarts the Windows system
    """
    try:
        print("Restarting the system...")
        os.system("shutdown /r /t 1")  # /r = restart, /t 1 = in 1 second
        return "System is restarting now."
    except Exception as e:
        return f"Error restarting: {str(e)}"


def check_if_app_installed(app_name):
    """
    Checks if an application is installed by looking in common paths
    Returns the path if found, None otherwise
    """
    app_name_lower = app_name.lower()
    
    # Check in our predefined common apps
    if app_name_lower in COMMON_APPS:
        app_path = COMMON_APPS[app_name_lower]
        # Expand environment variables like %USERNAME%
        app_path = os.path.expandvars(app_path)
        
        # Check if file exists
        if os.path.exists(app_path):
            return app_path
    
    # Try to find the app in running processes (alternative check)
    for process in psutil.process_iter(['name']):
        try:
            process_name = process.info['name'].lower()
            if app_name_lower in process_name or process_name.startswith(app_name_lower):
                return process_name
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    return None


def open_application(app_name):
    """
    Opens an installed application
    Returns a success or error message
    """
    try:
        # First check if app exists
        app_path = check_if_app_installed(app_name)
        
        if app_path is None:
            return f"Application '{app_name}' is not installed or not found."
        
        # Try to open the application
        if os.path.exists(app_path):
            # If it's a full path, open it directly
            subprocess.Popen(app_path)
        else:
            # If it's just a name (like notepad.exe), use os.system
            os.system(f"start {app_path}")
        
        return f"Opening {app_name}..."
    
    except Exception as e:
        return f"Error opening {app_name}: {str(e)}"


def list_installed_apps():
    """
    Lists all applications that JARVIS knows about
    """
    app_list = []
    for app_name in COMMON_APPS.keys():
        app_list.append(app_name)
    
    return app_list
