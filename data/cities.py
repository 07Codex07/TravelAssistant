CITY_FACTS = {
    "paris": """Paris is France's capital and honestly one of the most visited cities in the world.
    Eiffel Tower, Louvre, great food. Spring and fall are the best times to go.
    Population is around 2.1 million in the city itself.""",

    "tokyo": """Tokyo is massive - like 14 million people massive. It's Japan's capital and mixes
    old temples with very modern stuff. Shibuya crossing, Senso-ji, ramen everywhere.
    Cherry blossom season (late March to April) is peak time to visit.""",

    "new york": """NYC. 8.3 million people, never really sleeps. Central Park, Times Square,
    Statue of Liberty, Broadway. Food from literally every culture.
    Can be overwhelming but worth it.""",
}


def get_known_cities():
    return list(CITY_FACTS.keys())