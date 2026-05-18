import time
import random


# TODO: hook this up to a real API later (openweathermap maybe)
def get_weather_forecast(city: str) -> list:
    time.sleep(0.5)

    defaults = {"paris": 18, "tokyo": 22, "new york": 20}
    base = defaults.get(city.lower(), random.randint(15, 30))

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    conditions = ["Sunny", "Cloudy", "Rainy", "Windy", "Clear"]

    forecast = []
    for i in range(7):
        forecast.append({
            "day": days[i],
            "high": base + random.randint(-3, 5),
            "low": base - random.randint(3, 8),
            "condition": random.choice(conditions),
        })
    return forecast
