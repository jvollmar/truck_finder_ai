import geocode
from search_vehicles import search_vehicles
from filters import apply_filters
from html_report import generate_html
from emailer import send_email_with_link  # new function that sends the GitHub Pages URL

def main():
    listings = search_vehicles()
    for car in listings:
        addr = car["dealer"]["address"]
        try:
            car["lat"], car["lon"] = geocode.geocode_address(addr)
        except Exception as e:
            print("Geocode error:", e)

    filtered = apply_filters(listings)
    generate_html(filtered)  # create index.html
    send_email_with_link()   # just send the GitHub Pages link

if __name__ == "__main__":
    main()
