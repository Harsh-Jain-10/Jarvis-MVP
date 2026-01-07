import os
import subprocess

def open_app(command):
    command = command.lower()

    apps = {
        "camera": "start microsoft.windows.camera:",
        "calculator": "calc",
        "google": "start chrome",
        "chrome": "start chrome",
        "edge": "start msedge",
        "vs code": "code",
        "vlc": "vlc",
        "whatsapp": "start whatsapp:",
        "store": "start ms-windows-store:"
    }

    for app in apps:
        if app in command:
            os.system(apps[app])
            return True

    return False

