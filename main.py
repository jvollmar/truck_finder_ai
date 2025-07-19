from search_vehicles import search_vehicles
from filters import apply_filters
from html_report import generate_html
from emailer import send_email_with_link

def main():
    # Step 1: Scrape all vehicle listings
    listings = search_vehicles()

    # Step 2: Apply filters (this includes OpenAI and color filtering)
    filtered = apply_filters(listings)
    print("✅ Passed all filters:", len(filtered), "of", len(listings), "vehicles")

    # Step 3: Display count of vehicles that passed filters
    print("Filtered truck count:", len(filtered))

    # Step 4: Generate the HTML report only with filtered results
    generate_html(filtered)

    # Step 5: Email the report link
    send_email_with_link()

if __name__ == "__main__":
    main()
