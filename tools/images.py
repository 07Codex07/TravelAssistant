import time


# Direct image URLs (Wikimedia Commons, Unsplash, Pexels) — hotlink-friendly, no API key
CITY_IMAGES = {
    "paris": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg/1280px-Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Paris_-_Eiffelturm_und_Marsfeld2.jpg/1280px-Paris_-_Eiffelturm_und_Marsfeld2.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Paris_Night.jpg/1280px-Paris_Night.jpg",
    ],
    "tokyo": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Skyscrapers_of_Shinjuku_2009_January.jpg/1280px-Skyscrapers_of_Shinjuku_2009_January.jpg",
        "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800&q=80",
        "https://images.pexels.com/photos/2506923/pexels-photo-2506923.jpeg?auto=compress&cs=tinysrgb&w=800",
    ],
    "new york": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/New_york_times_square-terabass.jpg/1280px-New_york_times_square-terabass.jpg",
        "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=800&q=80",
        "https://images.pexels.com/photos/466685/pexels-photo-466685.jpeg?auto=compress&cs=tinysrgb&w=800",
    ],
}

FALLBACK = [
    "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=800&q=80",
    "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&q=80",
    "https://images.pexels.com/photos/346885/pexels-photo-346885.jpeg?auto=compress&cs=tinysrgb&w=800",
]


def get_city_images(city: str) -> list:
    time.sleep(0.4)
    return CITY_IMAGES.get(city.lower(), FALLBACK)
