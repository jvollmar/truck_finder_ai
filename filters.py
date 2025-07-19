rom math import radians, sin, cos, sqrt, atan2
from config import CENTER_LAT, CENTER_LON, SEARCH_RADIUS_MILES, VEHICLE_FILTERS, USE_OPENAI_FILTER
from openai_filter import is_vehicle_match

def within_radius(lat, lon):
    R = 3958.8
    dlat = radians(lat - CENTER_LAT)
    dlon = radians(lon - CENTER_LON)
    a = sin(dlat/2)**2 + cos(radians(CENTER_LAT)) * cos(radians(lat)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c <= SEARCH_RADIUS_MILES

def passes_color_filter(vehicle: dict) -> bool:
    color = vehicle.get("exterior_color_normalized", "").lower()
    return "blue" in color

def apply_filters(listings):
    results = []
    required_filters = VEHICLE_FILTERS.get("required", {})
    preferred_filters = VEHICLE_FILTERS.get("preferred", {})
    required_color = required_filters.get("color_contains", "").lower()

    for car in listings:
        title = car.get("title", "Unknown Title")

        lat, lon = car.get("lat"), car.get("lon")
        if lat is not None and lon is not None and not within_radius(lat, lon):
            continue

        if USE_OPENAI_FILTER:
            if not is_vehicle_match(car.get("description", "")):
                continue

        raw_color = car.get("color", "")
        normalized_color = raw_color.strip().lower()

        if required_color and required_color not in normalized_color:
            continue

        results.append(car)

    print(f"\n✅ Passed all filters: {len(results)} of {len(listings)} vehicles\n")
    return results
