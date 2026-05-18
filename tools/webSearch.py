import time

def mock_web_search(city: str) -> str:
    # placeholder - can swap with Tavily or DuckDuckGo later
    time.sleep(0.7)
    return (
        f"{city.title()} is an interesting place with its own culture and history. "
        f"It has local food, landmarks, and things worth seeing. "
        f"Not as well documented as major tourist cities but worth exploring."
    )
