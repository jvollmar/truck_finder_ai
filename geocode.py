# geocode.py
import requests
from config import GOOGLE_MAPS_API_KEY
import json
import os

ZIP_CACHE_FILE = "zip_cache.json"

def geocode_address(zip_code):
    # Check cache first
    if os.path.exists(ZIP_CACHE_FILE):
        with open(ZIP_CACHE_FILE, "r") as f:
            cache = json.load(f)
            if zip_code in cache:
                lat = cache[zip_code].get("lat")
                lon = cache[zip_code].get("lon")
                if lat is not None and lon is not None:
                    return lat, lon

    # If not in cache, call API
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": zip_code, "key": GOOGLE_MAPS_API_KEY}
    resp = requests.get(url, params=params)
    data = resp.json()
    if data["status"] == "OK":
        loc = data["results"][0]["geometry"]["location"]
        lat, lon = loc["lat"], loc["lng"]

        # Update cache
        city = next((c["long_name"] for c in data["results"][0]["address_components"] if "locality" in c["types"]), "Unknown City")
        state = next((c["short_name"] for c in data["results"][0]["address_components"] if "administrative_area_level_1" in c["types"]), "XX")
        city_state = f"{city}, {state}"

        cache = cache if os.path.exists(ZIP_CACHE_FILE) else {}
        cache[zip_code] = {"lat": lat, "lon": lon, "city_state": city_state}
        with open(ZIP_CACHE_FILE, "w") as f:
            json.dump(cache, f)

        return lat, lon

    raise RuntimeError(f"Geocoding failed for '{zip_code}': {data['status']}")
