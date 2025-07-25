import requests 
from bs4 import BeautifulSoup
from config import VEHICLE_FILTERS, USE_OPENAI_FILTER
from filters import passes_color_filter
from openai_filter import is_vehicle_match
from math import radians, sin, cos, sqrt, atan2
import time
import csv
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

BASE_URL = "https://www.cars.com"
CENTER_LAT = 36.0626  # Fayetteville, AR
CENTER_LON = -94.1574
SEARCH_RADIUS_MILES = 350
USZIPS_CSV = "data/uszips.csv"
CITY_STATE_TARGETS = set()

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 3958.8
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
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
                    color = value.lower()
                    if "blue" in color:
                        color = "blue"

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

def normalize_dealer_name(name):
    name = name.lower()
    name = re.sub(r'[\.,]', '', name)
    name = re.sub(r'\b(of|inc|llc|ltd|group|motors|auto|chevrolet|gmc)\b', '', name)
    name = re.sub(r'\s+', ' ', name)
    return name.strip()

def scrape_cars(make, model, zip_code, city_state):
    listings = []
    search_url = (
        f"https://www.cars.com/shopping/results/?stock_type=certified"
        f"&makes[]={make.lower()}"
        f"&models[]={make.lower()}-{model.lower().replace(' ', '_')}"
        f"&list_price_max=&maximum_distance=500"
        f"&zip={zip_code}"
        f"&year_min={VEHICLE_FILTERS['year_min']}"
        f"&mileage_max={VEHICLE_FILTERS['mileage_max']}"
        f"&transmission_slugs=automatic&drivetrain_slugs=4wd&only_with_photos=true"
    )

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

            # Check if vehicle city/state is in allowed targets
            if CITY_STATE_TARGETS and city_state not in CITY_STATE_TARGETS:
                continue

            listings.append(vehicle)

        except Exception as e:
            print("Error parsing a car:", e)

        time.sleep(1)

    return listings

def search_vehicles():
    all_listings = []
    with open(USZIPS_CSV, newline='') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            if i > 250:
                print("🔚 Reached limit of 250 ZIPs.")
                break

            try:
                zip_code = row["zip"]
                lat = float(row["lat"])
                lon = float(row["lng"])
                city = row["city"]
                state = row["state_id"]
                city_state = f"{city}, {state}"

                distance = haversine_distance(CENTER_LAT, CENTER_LON, lat, lon)
                if distance > SEARCH_RADIUS_MILES:
                    continue

                CITY_STATE_TARGETS.add(city_state)

                for make in VEHICLE_FILTERS["make"]:
                    for model in VEHICLE_FILTERS["model"]:
                        all_listings += scrape_cars(make, model, zip_code, city_state)

            except Exception as e:
                print(f"[ERROR] ZIP {row.get('zip')} failed: {e}")
                continue

    seen_keys = set()
    unique_listings = []
    for vehicle in all_listings:
        title = vehicle.get("title", "").strip().lower()
        dealer_name_raw = vehicle.get("dealer", {}).get("name", "")
        dealer_name = normalize_dealer_name(dealer_name_raw)

        dedupe_key = (title, dealer_name)
        if dedupe_key in seen_keys:
            continue
        seen_keys.add(dedupe_key)
        unique_listings.append(vehicle)

        print(f"[DEDUPED] Keeping: '{title}' @ '{dealer_name_raw}'")

    print(f"🧹 Deduplicated to {len(unique_listings)} unique listings from {len(all_listings)} scraped.")
    return unique_listings
