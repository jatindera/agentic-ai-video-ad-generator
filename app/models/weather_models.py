from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class WeatherInput(BaseModel):
    """Input model for requesting weather information."""
    city: str = Field(
        ...,
        description="Name of the city for which weather data is requested.",
        example="Tokyo"
    )


class WeatherOutput(BaseModel):
    """Structured weather information returned by the tool."""
    city: str = Field(..., description="City name")
    temperature: Optional[float] = Field(
        None, description="Temperature in Celsius"
    )
    conditions: Optional[str] = Field(
        None, description="Brief weather description, e.g. 'Clear', 'Rain'"
    )
    humidity: Optional[int] = Field(
        None, description="Humidity percentage"
    )
    wind_speed: Optional[float] = Field(
        None, description="Wind speed in m/s"
    )
    raw_response: Dict[str, Any] = Field(
        ..., description="Full raw API response for debugging and traceability"
    )
