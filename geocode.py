# geocode.py
import requests
import json
import os
from config import GOOGLE_MAPS_API_KEY

ZIP_CACHE_FILE = "zip_cache.json"

def geocode_address(zip_code):
    # Load existing cache or initialize
    cache = {}
    if os.path.exists(ZIP_CACHE_FILE):
        with open(ZIP_CACHE_FILE, "r") as f:
            try:
                cache = json.load(f)
            except json.JSONDecodeError:
                cache = {}

    # Return from cache if available
    if zip_code in cache and "lat" in cache[zip_code] and "lon" in cache[zip_code]:
        return cache[zip_code]["lat"], cache[zip_code]["lon"]

    # If not in cache, call API
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": zip_code, "key": GOOGLE_MAPS_API_KEY}
    resp = requests.get(url, params=params)
    data = resp.json()
    if data["status"] == "OK":
        loc = data["results"][0]["geometry"]["location"]
        lat, lon = loc["lat"], loc["lng"]

        # Extract city/state
        components = data["results"][0]["address_components"]
        city = next((c["long_name"] for c in components if "locality" in c["types"]), "Unknown City")
        state = next((c["short_name"] for c in components if "administrative_area_level_1" in c["types"]), "XX")
        city_state = f"{city}, {state}"

        # Save to cache
        cache[zip_code] = {"lat": lat, "lon": lon, "city_state": city_state}
        with open(ZIP_CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=2)

        return lat, lon

    raise RuntimeError(f"Geocoding failed for '{zip_code}': {data['status']}")
