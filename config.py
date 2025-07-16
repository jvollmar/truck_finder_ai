import os
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = "rmzgrace@yahoo.com"

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

CENTER_LAT = 36.0626
CENTER_LON = -94.1574
SEARCH_RADIUS_MILES = 850

VEHICLE_FILTERS = {
    "make": ["GMC", "Chevrolet"],
    "model": ["Denali", "Silverado 1500"],
    "certified": True,
    "year_min": 2017,
    "mileage_max": 20000,
    "drive": "4WD",
    "doors": 4,
    "leather_seats": True,
    "heated_cooled_seats": True,
    "electric_adjust": True,
    "push_start": False,
    "eco_features": False,
    "gps": False,
    "dvd": False,
    "bed_shell": True,
    "floor_mats": True,
    "premium_tires": True,
    "interior": "carpet",
    "color_contains": "blue"
}

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
