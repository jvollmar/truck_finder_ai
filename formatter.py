def format_output(listings):
    if not listings:
        return "No matching vehicles found within the area."

    lines = []
    for i, v in enumerate(listings, 1):
        d = v["dealer"]
        lines.append(f"""---
Vehicle #{i}
Title: {v['title']}
Price: {v.get('price', 'N/A')}
Image: {v.get('image_url', 'N/A')}
Description: {v['description']}

Dealer Info:
• Name: {d.get('name', 'N/A')}
• Address: {d.get('address', 'N/A')}
• Phone: {d.get('phone', 'N/A')}
• Website: {d.get('website', 'N/A')}
""")
    return "\n".join(lines)
