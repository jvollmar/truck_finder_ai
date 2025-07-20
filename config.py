import os


# Email configuration
EMAIL_SENDER = "rmzgrace@yahoo.com"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = "rmzgrace@yahoo.com"

# Google Maps API
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Search center for ZIP radius filtering
CENTER_LAT = 36.0626  # Fayetteville, AR
CENTER_LON = -94.1574
SEARCH_RADIUS_MILES = 350  # miles

# Toggle OpenAI filtering
USE_OPENAI_FILTER = False  # Set True to enable OpenAI semantic filtering

# Vehicle filtering criteria
VEHICLE_FILTERS = {
    "make": ["GMC", "Chevrolet"],
    "model": ["Denali", "Silverado 1500"],
    "certified": True,
    "year_min": 2017,
    "mileage_max": 20000,
    "drive": "4WD",
    "doors": 4,
    "color_contains": "blue"  # Used in both OpenAI and direct filters
}

# For OpenAI filtering prompt
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

PREFERRED_FEATURES = [
    "No GPS system",
    "No DVD system",
    "Hard shell truck bed cover",
    "Carpet interior",
    "Towing package",
    "Color (already filtered elsewhere)"
]

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(f"[CONFIG DEBUG] OpenAI key loaded: {bool(OPENAI_API_KEY)}")

