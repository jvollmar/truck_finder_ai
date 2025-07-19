import requests
from bs4 import BeautifulSoup
from config import VEHICLE_FILTERS, USE_OPENAI_FILTER, GOOGLE_MAPS_API_KEY
from filters import passes_color_filter
from openai_filter import is_vehicle_match
from geocode import geocode_address  # ✅ Geocoding zip codes
from math import radians, sin, cos, sqrt, atan2   
import time
import json
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

BASE_URL = "https://www.cars.com"
CENTER_LAT = 36.0626  # Fayetteville, AR
CENTER_LON = -94.1574
SEARCH_RADIUS_MILES = 850
ZIP_CACHE_FILE = "zip_cache.json"

ZIP_LIST = [
    "72701", "60601", "80202", "75201", "28202", "32202",
    "30301", "70112", "37201", "64106", "29401", "98101"
]

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 3958.8
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def get_vehicle_details(detail_url, fallback_city=None):
    try:
        resp = requests.get(detail_url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        mileage = "N/A"
        color = "Unknown"

        spec_section = soup.find("dl", class_="fancy-description-list")
        if spec_section:
            dt_tags = spec_section.find_all("dt")
            for dt in dt_tags:
                label = dt.get_text(strip=True).lower()
                value_tag = dt.find_next_sibling("dd")
                if not value_tag:
                    continue
                value = value_tag.get_text(strip=True)

                if "mileage" in label:
                    mileage = value
                elif "exterior color" in label:
                    color = value
                    if "blue" in color.lower():
                        color = "blue"
                    else:
                        color = color.lower()

        addr_tag = soup.find("div", class_="seller-info__address")
        full_address = addr_tag.text.strip() if addr_tag else f"N/A ({fallback_city})"

        phone_tag = soup.find("a", class_="seller-info__phone")
        phone = phone_tag.get_text(strip=True) if phone_tag else "N/A"

        desc_tag = soup.find("div", class_="seller-notes")
        description = desc_tag.get_text(strip=True) if desc_tag else "No additional description"

        return mileage, full_address, phone, description, color

    except Exception as e:
        print("Error fetching vehicle detail:", e)
        return "N/A", "N/A", "N/A", "N/A", "Unknown"

def load_zip_cache():
    if os.path.exists(ZIP_CACHE_FILE):
        with open(ZIP_CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_zip_cache(cache):
    with open(ZIP_CACHE_FILE, "w") as f:
        json.dump(cache, f)

def scrape_cars(make, model, zip_code, city_state):
    listings = []
    search_url = f"https://www.cars.com/shopping/results/?stock_type=certified&makes[]={make.lower()}&models[]={make.lower()}-{model.lower().replace(' ', '_')}&list_price_max=&maximum_distance=500&zip={zip_code}&year_min={VEHICLE_FILTERS['year_min']}&mileage_max={VEHICLE_FILTERS['mileage_max']}&transmission_slugs=automatic&drivetrain_slugs=4wd&only_with_photos=true"

    try:
        resp = requests.get(search_url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"Error fetching {make} {model} in {zip_code}: {e}")
        return []

    cars = soup.select("div.vehicle-card")
    for car in cars[:10]:
        try:
            title = car.select_one("h2.title").text.strip()
            price = car.select_one(".primary-price").text.strip()
            image = car.select_one("img")["src"]
            link_tag = car.select_one("a.vehicle-card-link")
            if not link_tag:
                continue
            detail_url = BASE_URL + link_tag["href"]

            mileage, full_address, phone, description, color = get_vehicle_details(detail_url, fallback_city=city_state)

            vehicle = {
                "title": title,
                "price": price,
                "description": description,
                "mileage": mileage,
                "color": color,
                "exterior_color_normalized": color,
                "image_url": image,
                "dealer": {
                    "name": "Certified Dealer",
                    "address": full_address,
                    "phone": phone,
                    "website": detail_url
                },
                "lat": None,
                "lon": None,
                "city_state": city_state
            }

            if not passes_color_filter(vehicle):
                continue

            if USE_OPENAI_FILTER and not is_vehicle_match(description):
                continue

            listings.append(vehicle)

        except Exception as e:
            print("Error parsing a car:", e)

        time.sleep(1)

    return listings

def search_vehicles():
    all_listings = []
    zip_cache = load_zip_cache()

    for zip_code in ZIP_LIST:
        try:
            if zip_code in zip_cache:
                lat, lon = zip_cache[zip_code]["lat"], zip_cache[zip_code]["lon"]
                city_state = zip_cache[zip_code]["city_state"]
            else:
                lat, lon = geocode_address(zip_code)
                distance = haversine_distance(CENTER_LAT, CENTER_LON, lat, lon)
                if distance > SEARCH_RADIUS_MILES:
                    print(f"[SKIP] ZIP {zip_code} is {int(distance)} miles away — outside radius.")
                    continue

                response = requests.get(
                    "https://maps.googleapis.com/maps/api/geocode/json",
                    params={"address": zip_code, "key": GOOGLE_MAPS_API_KEY}
                )
                result = response.json()
                if result["status"] == "OK":
                    components = result["results"][0]["address_components"]
                    city = next((c["long_name"] for c in components if "locality" in c["types"]), "Unknown City")
                    state = next((c["short_name"] for c in components if "administrative_area_level_1" in c["types"]), "XX")
                    city_state = f"{city}, {state}"
                else:
                    city_state = f"ZIP {zip_code}"

                zip_cache[zip_code] = {"lat": lat, "lon": lon, "city_state": city_state}

            for make in VEHICLE_FILTERS["make"]:
                for model in VEHICLE_FILTERS["model"]:
                    all_listings += scrape_cars(make, model, zip_code, city_state)

        except Exception as e:
            print(f"[ERROR] Geocoding ZIP {zip_code} failed: {e}")
            continue

    save_zip_cache(zip_cache)
    return all_listingss
