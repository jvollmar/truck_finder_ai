# filters.py
from math import radians, sin, cos, sqrt, atan2
from openai_filter import is_vehicle_match
from config import CENTER_LAT, CENTER_LON, SEARCH_RADIUS_MILES, VEHICLE_FILTERS

def within_radius(lat, lon):
    R = 3958.8
    dlat = radians(lat - CENTER_LAT)
    dlon = radians(lon - CENTER_LON)
    a = sin(dlat/2)**2 + cos(radians(CENTER_LAT)) * cos(radians(lat)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c <= SEARCH_RADIUS_MILES

def apply_filters(listings):
    results = []
    required_color = VEHICLE_FILTERS.get("color_contains", "").lower()

    for car in listings:
        # Radius check
        lat, lon = car.get("lat"), car.get("lon")
        if lat and lon and not within_radius(lat, lon):
            print(f"Skipping {car['title']} - outside radius")
            continue

        # OpenAI semantic match check
        if not is_vehicle_match(car.get("description", "")):
            print(f"Skipping {car['title']} - OpenAI filter mismatch")
            continue

        # Structured color match
        color = car.get("color", "").lower()
        if required_color:
            if required_color not in color:
                print(f"Skipping {car['title']} - color '{color}' does not match required '{required_color}'")
                continue

        results.append(car)

    print(f"\n✅ Passed color filter: {len(results)} out of {len(listings)} vehicles\n")
    return results
