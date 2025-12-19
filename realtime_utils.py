"""
Real-time data utilities for JARVIS Assistant
Handles weather data and general knowledge questions
"""

import requests
import wikipediaapi
from config import WEATHER_API_KEY

def get_weather(city_name):
    """
    Gets current weather for a city using OpenWeatherMap API
    Returns weather information or error message
    """
    # Check if API key is available
    if not WEATHER_API_KEY or WEATHER_API_KEY == "":
        return "Weather API key not configured. Please add WEATHER_API_KEY to your .env file. Get a free key from https://openweathermap.org/api"
    
    try:
        # OpenWeatherMap API endpoint
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        # Parameters for the API request
        params = {
            "q": city_name,
            "appid": WEATHER_API_KEY,
            "units": "metric"  # Use Celsius
        }
        
        # Make the API request
        response = requests.get(base_url, params=params, timeout=5)
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Extract weather information
            temperature = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            description = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            
            # Format the weather report
            weather_report = f"Weather in {city_name}:\n"
            weather_report += f"Temperature: {temperature}°C (Feels like {feels_like}°C)\n"
            weather_report += f"Condition: {description.capitalize()}\n"
            weather_report += f"Humidity: {humidity}%"
            
            return weather_report
        
        elif response.status_code == 404:
            return f"City '{city_name}' not found. Please check the spelling."
        
        else:
            return f"Error getting weather data. Status code: {response.status_code}"
    
    except requests.exceptions.Timeout:
        return "Weather request timed out. Please check your internet connection."
    
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

def get_general_info(query):
    """
    Gets general information using Wikipedia API
    Returns a summary or error message
    """
    try:
        # Create Wikipedia API object (English)
        wiki = wikipediaapi.Wikipedia(
            language='en',
            user_agent='JARVIS-Assistant/1.0'
        )
        
        # Search for the page
        page = wiki.page(query)
        
        # Check if page exists
        if page.exists():
            # Get summary (first 3 sentences)
            summary = page.summary.split('.')[:3]
            summary_text = '. '.join(summary) + '.'
            
            return summary_text
        else:
            return f"Sorry, I couldn't find information about '{query}' on Wikipedia."
    
    except Exception as e:
        return f"Error fetching information: {str(e)}"


def answer_question(question):
    """
    Tries to answer general knowledge questions
    Uses Wikipedia as the primary source
    """
    # Clean up the question
    question = question.lower().strip()
    
    # Remove common question words to get the main topic
    question_words = ["who is", "what is", "where is", "when is", "tell me about", "about"]
    
    topic = question
    for word in question_words:
        if question.startswith(word):
            topic = question.replace(word, "").strip()
            break
    
    # If we have a topic, search for it
    if topic:
        return get_general_info(topic)
    else:
        return "I'm not sure what you're asking about. Could you rephrase your question?"


