from typing import TypedDict, Optional


class TravelState(TypedDict):
    user_query: str
    city: str
    route: Optional[str]
    city_summary: Optional[str]
    weather_forecast: Optional[list]
    image_urls: Optional[list]
    messages: list
    final_output: Optional[dict]