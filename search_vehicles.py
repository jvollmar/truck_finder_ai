import requests
from bs4 import BeautifulSoup
from config import VEHICLE_FILTERS
from geocode import geocode_address
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

def scrape_cars(make, model, zip_code):
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
    for car in cars[:10]:  # Limit per zip/make/model
        try:
            title = car.select_one("h2.title").text.strip()
            price = car.select_one(".primary-price").text.strip()
            image = car.select_one("img")["src"]
            desc = car.select_one(".dealer-name").text.strip()

            dealer_name = desc
            dealer_address = f"{zip_code}"

            lat, lon = geocode_address(dealer_address)

            listings.append({
                "title": title,
                "price": price,
                "description": desc,
                "image_url": image,
                "dealer": {
                    "name": dealer_name,
                    "address": dealer_address,
                    "phone": "N/A",
                    "website": "https://www.cars.com"
                },
                "lat": lat,
                "lon": lon
            })
        except Exception as e:
            print("Error parsing a car:", e)
        time.sleep(0.5)  # Be nice to their servers

    return listings

def search_vehicles():
    all_listings = []
    for city, zip_code in SEARCH_ZIPS.items():
        for make in VEHICLE_FILTERS["make"]:
            for model in VEHICLE_FILTERS["model"]:
                all_listings += scrape_cars(make, model, zip_code)
    return all_listings
