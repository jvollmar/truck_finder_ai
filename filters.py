from math import radians, sin, cos, sqrt, atan2
from config import CENTER_LAT, CENTER_LON, SEARCH_RADIUS_MILES, VEHICLE_FILTERS, USE_OPENAI_FILTER
from openai_filter import is_vehicle_match

def within_radius(lat, lon):
    R = 3958.8
    dlat = radians(lat - CENTER_LAT)
    dlon = radians(lon - CENTER_LON)
    a = sin(dlat/2)**2 + cos(radians(CENTER_LAT)) * cos(radians(lat)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c <= SEARCH_RADIUS_MILES

def apply_filters(listings):
    results = []
    required_filters = VEHICLE_FILTERS.get("required", {})
    suggested_filters = VEHICLE_FILTERS.get("suggested", {})
    required_color = required_filters.get("color_contains", "").lower()

    for car in listings:
        title = car.get("title", "Unknown Title")

        # Radius check
        lat, lon = car.get("lat"), car.get("lon")
        if lat is not None and lon is not None and not within_radius(lat, lon):
            print(f"Skipping {title} - outside radius")
            continue

        # OpenAI semantic match check
        if USE_OPENAI_FILTER:
            description = car.get("description", "")
            if not is_vehicle_match(description):
                print(f"Skipping {title} - OpenAI filter mismatch")
                continue

        # Structured color match
        raw_color = car.get("color", "")
        normalized_color = raw_color.strip().lower()

        print(f"[DEBUG] Filtering color: '{raw_color}' (normalized: '{normalized_color}') for vehicle: {title}")

        if required_color and required_color not in normalized_color:
            print(f"Skipping {title} - color '{normalized_color}' does not contain '{required_color}'")
            continue

        results.append(car)

    print(f"\n✅ Passed all filters: {len(results)} of {len(listings)} vehicles\n")
    return results
