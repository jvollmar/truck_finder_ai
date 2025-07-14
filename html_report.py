# html_report.py

def generate_html(listings):
    html = """
    <html>
    <head>
        <title>Truck Search Results</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .card { border: 1px solid #ccc; border-radius: 10px; padding: 15px; margin-bottom: 20px; }
            img { max-width: 100%; height: auto; }
        </style>
    </head>
    <body>
        <h1>Certified Truck Search Results</h1>
    """

    for car in listings:
        html += f"""
        <div class='card'>
            <h2>{car['title']}</h2>
            <p><strong>Price:</strong> {car['price']}</p>
            <p><strong>Dealer:</strong> {car['dealer']['name']}</p>
            <p><strong>Address:</strong> {car['dealer']['address']}</p>
            <p><strong>Phone:</strong> {car['dealer']['phone']}</p>
            <p><strong>Description:</strong> {car['description']}</p>
            <img src="{car['image_url']}" alt="Truck Image">
        </div>
        """

    html += "</body></html>"

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
