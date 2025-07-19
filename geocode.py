# geocode.py
import requests
from config import GOOGLE_MAPS_API_KEY

def geocode_address(zip_code):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": zip_code, "key": GOOGLE_MAPS_API_KEY}
    resp = requests.get(url, params=params)
    data = resp.json()

    if data["status"] == "OK":
        loc = data["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]

    raise RuntimeError(f"Geocoding failed for '{zip_code}': {data['status']}")
