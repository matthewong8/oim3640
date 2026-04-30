"""
Weather module: Fetches current conditions from the OpenWeatherMap API.

Returns structured data so the briefing renderer (text or HTML) can
present the information however it likes.
"""

import requests
from config import OPENWEATHER_API_KEY, CITY


def get_weather_data():
    """
    Fetch current weather for the configured city.

    Returns:
        dict | None: Dictionary with temperature, condition, humidity,
                     wind speed, etc. Returns None if the request fails.
    """
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": CITY,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric",
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        return {
            "city": CITY,
            "temp": round(data["main"]["temp"], 1),
            "feels_like": round(data["main"]["feels_like"], 1),
            "condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"].capitalize(),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "icon_code": data["weather"][0]["icon"],
        }
    except Exception as e:
        print(f"  Weather fetch failed: {e}")
        return None


if __name__ == "__main__":
    print(get_weather_data())
