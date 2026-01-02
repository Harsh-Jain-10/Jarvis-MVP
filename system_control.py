import os
import pyautogui
import time

def shutdown_pc():
    os.system("shutdown /s /t 1")

def restart_pc():
    os.system("shutdown /r /t 1")

def sleep_pc():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def take_screenshot():
    os.makedirs("screenshots", exist_ok=True)
    filename = f"screenshots/screenshot_{int(time.time())}.png"
    pyautogui.screenshot(filename)
