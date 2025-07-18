import os

# Email configuration
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = "rmzgrace@yahoo.com"

# Google Maps API
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Search area
CENTER_LAT = 36.0626
CENTER_LON = -94.1574
SEARCH_RADIUS_MILES = 850

# Toggle OpenAI filtering
USE_OPENAI_FILTER = True  # Set to False to skip OpenAI filtering

# Vehicle filtering criteria
VEHICLE_FILTERS = {
    "make": ["GMC", "Chevrolet"],
    "model": ["Denali", "Silverado 1500"],
    "certified": True,
    "year_min": 2017,
    "mileage_max": 30000,
    "drive": "4WD",
    "doors": 4,
    "color_contains": "blue"
}

# For OpenAI prompt - hard requirements
REQUIRED_FEATURES = [
    "Make: GMC or Chevrolet",
    "Model: Denali or Silverado 1500",
    "Certified Pre-Owned",
    "Year: 2017 or newer",
    "Mileage: under 30,000",
    "Drive: 4WD (four-wheel drive)",
    "Doors: 4",
    "Leather seats",
    "Heated and cooled seats",
    "Electrically adjustable seats",
    "No eco or hybrid features",
    "Premium tires",
    "Full-length running boards"
]

# For OpenAI prompt - optional suggestions
PREFERRED_FEATURES = [
    "No GPS system",
    "No DVD system",
    "Hard shell truck bed cover",
    "Carpet interior",
    "Towing package",
    "Color (already filtered elsewhere)"
]

# OpenAI key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(f"[CONFIG DEBUG] OpenAI key loaded: {bool(OPENAI_API_KEY)}")

USE_OPENAI_FILTER = True  # Toggle to True to enable OpenAI filtering

