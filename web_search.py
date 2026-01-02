import webbrowser

def google_search(command):
    query = command.replace("search", "").strip()
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
