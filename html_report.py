def generate_html(listings):
    html = """<html>
<head>
    <title>Truck Search Results</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .card { border: 1px solid #ccc; border-radius: 10px; padding: 15px; margin-bottom: 20px; }
        img { max-width: 100%; height: auto; border-radius: 8px; }
        h2 { margin-top: 0; }
        a { text-decoration: none; color: #0366d6; }
    </style>
</head>
<body>
    <h1>Certified Truck Search Results</h1>
"""

    for car in listings:
        title = car.get('title', 'Unknown')
        price = car.get('price', 'N/A')
        mileage = car.get('mileage', 'N/A')
        color = car.get('color', 'N/A')
        description = car.get('description', 'No description')
        image_url = car.get('image_url', '')
        dealer = car.get('dealer', {})
        dealer_name = dealer.get('name', 'N/A')
        dealer_address = dealer.get('address', 'N/A')
        dealer_phone = dealer.get('phone', 'N/A')
        dealer_website = dealer.get('website', '#')
        city_state = car.get('city_state', 'N/A')  # ✅ NEW

        html += f"""
    <div class='card'>
        <h2>{title}</h2>
        <p><strong>Price:</strong> {price}</p>
        <p><strong>Mileage:</strong> {mileage}</p>
        <p><strong>Exterior Color:</strong> {color}</p>
        <p><strong>Description:</strong> {description}</p>
        <img src="{image_url}" alt="Truck Image">
        <p><strong>Dealer:</strong> {dealer_name}</p>
        <p><strong>Address:</strong> {dealer_address}</p>
        <p><strong>City/State:</strong> {city_state}</p>
        <p><strong>Phone:</strong> {dealer_phone}</p>
        <p><strong>Website:</strong> <a href="{dealer_website}" target="_blank">{dealer_website}</a></p>
    </div>
"""

    html += "</body></html>"

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
