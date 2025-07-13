import geocode
from search_vehicles import search_vehicles
from filters import apply_filters
from formatter import format_output
from emailer import send_email

def main():
    listings = search_vehicles()
    for car in listings:
        addr = car["dealer"]["address"]
        try:
            car["lat"], car["lon"] = geocode.geocode_address(addr)
        except Exception as e:
            print("Geocode error:", e)
    filtered = apply_filters(listings)
    send_email(format_output(filtered))

if __name__ == "__main__":
    main()
