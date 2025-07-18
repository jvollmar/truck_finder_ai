import requests
from bs4 import BeautifulSoup
from config import VEHICLE_FILTERS
from filters import passes_color_filter
from openai_filter import is_vehicle_match
import time

SEARCH_ZIPS = {
    "Fayetteville, AR": "72701",
    "Chicago, IL": "60601",
    "Denver, CO": "80202",
    "Dallas, TX": "75201",
    "Charlotte, NC": "28202",
    "Jacksonville, FL": "32202"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

BASE_URL = "https://www.cars.com"

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
                    print(f"[DEBUG] Extracted raw color value: '{color}' from label: '{label}'") 
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

def scrape_cars(make, model, zip_code, city):
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

            mileage, full_address, phone, description, color = get_vehicle_details(detail_url, fallback_city=city)
            print("Extracted color:", color)

            vehicle = {
                "title": title,
                "price": price,
                "description": description,
                "mileage": mileage,
                "color": color,
                "image_url": image,
                "dealer": {
                    "name": "Certified Dealer",
                    "address": full_address,
                    "phone": phone,
                    "website": detail_url
                },
                "lat": None,
                "lon": None
            }

            # ✅ Color filter check BEFORE OpenAI
            if not passes_color_filter(vehicle):
                print(f"[DEBUG] Skipping {title} - color '{color}' rejected")
                continue

            # ✅ OpenAI filter
            if not is_vehicle_match(description):
                print(f"[DEBUG] Skipping {title} - OpenAI filter mismatch")
                continue

            listings.append(vehicle)

        except Exception as e:
            print("Error parsing a car:", e)

        time.sleep(1)

    return listings

def search_vehicles():
    all_listings = []
    for city, zip_code in SEARCH_ZIPS.items():
        for make in VEHICLE_FILTERS["make"]:
            for model in VEHICLE_FILTERS["model"]:
                all_listings += scrape_cars(make, model, zip_code, city)
    return all_listings
