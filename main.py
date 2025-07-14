from search_vehicles import search_vehicles
from filters import apply_filters
from html_report import generate_html
from emailer import send_email_with_link

def main():
    listings = search_vehicles()
    
    # Don't re-geocode — already done in search_vehicles
    filtered = apply_filters(listings)
    
    print("Filtered truck count:", len(filtered))

    generate_html(filtered)
    send_email_with_link()

if __name__ == "__main__":
    main()
