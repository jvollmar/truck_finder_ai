from config import VEHICLE_FILTERS, USE_OPENAI_FILTER
from openai_filter import is_vehicle_match

def passes_color_filter(vehicle: dict) -> bool:
    color = vehicle.get("exterior_color_normalized", "").lower()
    return "blue" in color

def apply_filters(listings):
    results = []
    required_color = VEHICLE_FILTERS.get("color_contains", "").lower()

    for car in listings:
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
