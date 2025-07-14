# search_vehicles.py
from config import VEHICLE_FILTERS

def search_official_portal(make, model):
    # Mock listing to test HTML output
    return [{
        "title": f"{make} {model} Test Truck",
        "price": "$42,500",
        "description": "Certified pre-owned with leather seats and bed shell.",
        "image_url": "https://via.placeholder.com/400x200.png?text=Truck+Image",
        "dealer": {
            "name": "Test Dealer",
            "address": "123 Main St, Anytown, USA",
            "phone": "(555) 555-5555",
            "website": "https://dealer.example.com"
        },
        "lat": 36.06,
        "lon": -94.15
    }]

def search_vehicles():
    all_listings = []
    for make in VEHICLE_FILTERS["make"]:
        for model in VEHICLE_FILTERS["model"]:
            all_listings += search_official_portal(make, model)
    return all_listings
