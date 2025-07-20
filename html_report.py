import html
from datetime import datetime
import os


def generate_html(listings):
    now = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    html_content = f"""<html>
<head>
    <title>Certified Truck Search Results</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .card {{
            background: #fff;
            border: 1px solid #ccc;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 20px;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.08);
        }}
        img {{
            max-width: 300px;
            height: auto;
            border-radius: 8px;
            margin: 10px 0;
        }}
        h1 {{
            color: #2a2a2a;
        }}
        h2 {{
            margin-top: 0;
            color: #0b3d91;
        }}
        p {{
            margin: 5px 0;
        }}
        a {{
            text-decoration: none;
            color: #0366d6;
        }}
        .footer {{
            margin-top: 40px;
            font-size: 0.9em;
            color: #666;
            text-align: center;
        }}
        .highlight {{
            background: #e6f2ff;
            padding: 2px 4px;
            border-radius: 4px;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h1>Certified Truck Search Results</h1>
    <p>Report generated on <strong>{now}</strong></p>
"""

    for i, car in enumerate(listings, 1):
        title = html.escape(car.get('title', 'Unknown'))
        price = html.escape(car.get('price', 'N/A'))
        mileage = html.escape(car.get('mileage', 'N/A'))
        color = html.escape(car.get('color', 'N/A'))
        description = html.escape(car.get('description', 'No description'))
        image_url = car.get('image_url', '')
        dealer = car.get('dealer', {})
        dealer_name = html.escape(dealer.get('name', 'N/A'))
        dealer_address = html.escape(dealer.get('address', 'N/A'))
        dealer_phone = html.escape(dealer.get('phone', 'N/A'))
        dealer_website = html.escape(dealer.get('website', '#'))
        city_state = html.escape(car.get('city_state', 'N/A'))

        color_tag = f"<span class='highlight'>{color}</span> 🌊" if "blue" in color.lower() else color
        image_tag = f"<img src='{image_url}' alt='Truck Image - {title}'>" if image_url else ""

        html_content += f"""
    <div class='card'>
        <h2>#{i}: <a href="{dealer_website}" target="_blank">{title}</a></h2>
        <p><strong>Price:</strong> {price}</p>
        <p><strong>Mileage:</strong> {mileage}</p>
        <p><strong>Exterior Color:</strong> {color_tag}</p>
        <p><strong>Description:</strong> {description}</p>
        {image_tag}
        <p><strong>City/State:</strong> {city_state}</p>
        <p><strong>Address:</strong> {dealer_address}</p>
        <p><strong>Phone:</strong> {dealer_phone}</p>
        <p><strong>Website:</strong> <a href="{dealer_website}" target="_blank">{dealer_website}</a></p>
    </div>
"""

    html_content += """
    <div class="footer">
        <p>ZIP code location data provided by <a href="https://simplemaps.com/data/us-zips" target="_blank">SimpleMaps</a>.</p>
        <p>Vehicle listings retrieved from <a href="https://cars.com" target="_blank">Cars.com</a>.</p>
        <p>Filtered by: certified status, exterior color "blue", 2017+ model year, ≤20,000 miles.</p>
    </div>
</body>
</html>
"""

    os.makedirs("report", exist_ok=True)
    with open("report/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
