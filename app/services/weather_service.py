import httpx
from app.core.config import settings
from app.models.weather_models import WeatherOutput


BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


async def get_weather(city: str) -> WeatherOutput:
    """
    Fetch weather information from the external Weather API and
    return it as a validated WeatherOutput model.
    """
    params = {
        "q": city,
        "appid": settings.WEATHER_API_KEY,
        "units": "metric"
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(BASE_URL, params=params)
        data = resp.json()

    return WeatherOutput(
        city=city,
        temperature=data.get("main", {}).get("temp"),
        conditions=data.get("weather", [{}])[0].get("description"),
        humidity=data.get("main", {}).get("humidity"),
        wind_speed=data.get("wind", {}).get("speed"),
        raw_response=data
    )
