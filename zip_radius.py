# zip_radius.py
import os
import requests
import json
from config import SEARCH_RADIUS_MILES

ZIP_RADIUS_CACHE = "zip_radius_cache.json"
ZIPCODE_API_KEY = os.getenv("ZIPCODE_API_KEY")
ZIPCODE_API_URL = "https://www.zipcodeapi.com/rest/{}/radius.json/{}/{}"

def load_cached_zips(center_zip):
    if os.path.exists(ZIP_RADIUS_CACHE):
        with open(ZIP_RADIUS_CACHE, "r") as f:
            cache = json.load(f)
            if center_zip in cache:
                return cache[center_zip]
    return []

def save_cached_zips(center_zip, zips):
    if os.path.exists(ZIP_RADIUS_CACHE):
        with open(ZIP_RADIUS_CACHE, "r") as f:
            cache = json.load(f)
    else:
        cache = {}
    cache[center_zip] = zips
    with open(ZIP_RADIUS_CACHE, "w") as f:
        json.dump(cache, f)

def get_zip_codes_within_radius(center_zip):
    if not ZIPCODE_API_KEY:
        raise RuntimeError("ZIPCODE_API_KEY is not set in environment")

    cached = load_cached_zips(center_zip)
    if cached:
        return cached

    url = ZIPCODE_API_URL.format(ZIPCODE_API_KEY, center_zip, SEARCH_RADIUS_MILES)
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        zip_codes = [item["zip_code"] for item in data.get("zip_codes", [])]
        save_cached_zips(center_zip, zip_codes)
        return zip_codes
    except Exception as e:
        print(f"[ERROR] Failed to fetch zip codes from ZipCodeAPI: {e}")
        return []
