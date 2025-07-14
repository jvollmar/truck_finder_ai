import requests
from config import VEHICLE_FILTERS
from geocode import geocode_address

# Central ZIP for radius-based query
ZIP_CODE = "72701"  # Fayetteville, AR

def search_official_portal(make, model):
    url = "https://api.gmcertified.com/inventory/api/v1/search"

    payload = {
        "make": make,
        "model": model,
        "certified": True,
        "zip": ZIP_CODE,
        "radius": 1000,  # Pulls from a large region including your target cities
        "yearFrom": VEHICLE_FILTERS["year_min"],
        "mileageTo": VEHICLE_FILTERS["mileage_max"],
        "transmission": "Automatic",
        "limit": 30
    }

    try:
        response = requests.get(url, params=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Failed to fetch inventory for {make} {model}: {e}")
        return []

    listings = []

    for vehicle in data.get("vehicles", []):
        try:
            dealer_info = vehicle.get("dealer", {})
            address = dealer_info.get("address", "")
            lat, lon = geocode_address(address)

            listing = {
                "title": f"{vehicle.get('year')} {vehicle.get('make')} {vehicle.get('model')}",
                "price": vehicle.get("price"),
                "description": vehicle.get("description", "No description available."),
                "image_url": vehicle.get("imageUrl", ""),
                "dealer": {
                    "name": dealer_info.get("name", "N/A"),
                    "address": address,
                    "phone": dealer_info.get("phone", "N/A"),
                    "website": dealer_info.get("website", "N/A")
                },
                "lat": lat,
                "lon": lon
            }

            listings.append(listing)
        except Exception as e:
            print(f"Skipping vehicle due to error: {e}")

    return listings

def search_vehicles():
    all_listings = []
    for make in VEHICLE_FILTERS["make"]:
        for model in VEHICLE_FILTERS["model"]:
            all_listings += search_official_portal(make, model)
    return all_listings
