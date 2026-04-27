"""
Weather module: Fetches current conditions and forecast from OpenWeatherMap API
"""

import requests
from config import OPENWEATHER_API_KEY, CITY


def get_weather_briefing():
    """
    Fetch weather data for the configured city and return a formatted briefing.
    
    Returns:
        str: Formatted weather briefing text
    """
    try:
        # Current weather
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": CITY,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract key information
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        condition = data["weather"][0]["main"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        briefing = f"""
WEATHER BRIEFING FOR {CITY.upper()}
Temperature: {temp}°C (feels like {feels_like}°C)
Condition: {condition}
Humidity: {humidity}%
Wind Speed: {wind_speed} m/s
"""
        
        return briefing.strip()
    
    except requests.exceptions.RequestException as e:
        return f"Weather Fetch Failed: {str(e)}"
    except KeyError as e:
        return f"Weather Data Error: Missing field {str(e)}"


if __name__ == "__main__":
    # Test weather module
    print(get_weather_briefing())
