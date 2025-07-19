def format_output(listings):
    if not listings:
        return "No matching vehicles found within the area."

    lines = []
    for i, v in enumerate(listings, 1):
        d = v["dealer"]
        lines.append(f"""---
Vehicle #{i}:
Title: {v['title']}
Price: {v.get('price','N/A')}
Image: {v.get('image','N/A')}
Description: {v['description']}

Dealer:
• {d.get('name')}
• {d.get('address')}
• {d.get('phone')}
• {d.get('website')}
""")
    return "\n".join(lines)
