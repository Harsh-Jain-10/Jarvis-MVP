"""
Web utilities for JARVIS Assistant
Handles web searches and opening browsers
"""

import webbrowser


def search_google(query):
    """
    Opens Google Chrome and searches for the query
    Uses the default browser if Chrome is not available
    """
    try:
        # Format the Google search URL
        search_url = f"https://www.google.com/search?q={query}"
        
        # Try to open in Chrome first
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        
        try:
            # Try to register and use Chrome
            webbrowser.get(chrome_path).open(search_url)
            return f"Searching Google for '{query}' in Chrome..."
        except:
            # If Chrome is not found, use default browser
            webbrowser.open(search_url)
            return f"Searching Google for '{query}' in default browser..."
    
    except Exception as e:
        return f"Error opening browser: {str(e)}"


def open_website(url):
    """
    Opens a website in the default browser
    """
    try:
        # Add https:// if not present
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        
        webbrowser.open(url)
        return f"Opening {url}..."
    
    except Exception as e:
        return f"Error opening website: {str(e)}"