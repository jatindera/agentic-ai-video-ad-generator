from app.models.weather_models import WeatherInput, WeatherOutput
from app.services.weather_service import get_weather


async def weather_tool(input: WeatherInput) -> WeatherOutput:
    """
    Retrieve current weather information for a specified city.

    This MCP tool allows AI Agents and MCP Clients to fetch structured,
    validated weather data such as temperature, humidity, conditions,
    and wind speed. It uses Pydantic models for strong input and output
    validation, ensuring reliability and consistency.

    Parameters
    ----------
    input : WeatherInput
        A Pydantic model containing:
        - city (str): Name of the city.

    Returns
    -------
    WeatherOutput
        A Pydantic model containing:
        - city (str)
        - temperature (float | None)
        - conditions (str | None)
        - humidity (int | None)
        - wind_speed (float | None)
        - raw_response (dict)

    Raises
    ------
    HTTPError
        If the weather API request fails.
    ValueError
        If the city name is missing or invalid.

    Examples
    --------
    >>> await weather_tool(WeatherInput(city="Delhi"))
    WeatherOutput(
        city="Delhi",
        temperature=31.2,
        conditions="haze",
        humidity=58,
        wind_speed=3.1,
        raw_response={...}
    )

    Notes
    -----
    This tool is exposed as an MCP function, allowing AI-powered editors
    like VSCode, Cursor, or JetBrains to perform real-time weather checks.
    """
    return await get_weather(input.city)
