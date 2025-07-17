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
    print(f"\n🟦 Required color filter: '{required_color}'\n")

    for car in listings:
        title = car.get("title", "Unknown title")
        lat, lon = car.get("lat"), car.get("lon")

        # Radius check
        if lat and lon and not within_radius(lat, lon):
            print(f"⛔ Skipping {title}: Outside radius")
            continue

        # OpenAI semantic match check
        if not is_vehicle_match(car.get("description", "")):
            print(f"⛔ Skipping {title}: OpenAI filter mismatch")
            continue

        # Color check (structured)
        color = car.get("color", "").lower()
        if not color:
            print(f"⛔ Skipping {title}: No color info")
            continue
        if required_color and required_color not in color:
            print(f"⛔ Skipping {title}: Color '{color}' does not match required '{required_color}'")
            continue
        print(f"✅ Passed: {title} - Color '{color}'")

        results.append(car)

    print(f"\n✅ Final filtered count: {len(results)} of {len(listings)} vehicles matched\n")
    return results
