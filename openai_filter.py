import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# ✅ Optional: Debug check to confirm key is loaded
print(f"[DEBUG] OpenAI API Key Loaded: {bool(openai.api_key)}")

def is_vehicle_match(description: str) -> bool:
    prompt = f"""
You are a strict filter for a vehicle buyer. Determine if the following vehicle listing matches **ALL required criteria** below. Only answer with YES or NO — do not explain your answer.

❗ Required features (must all be clearly mentioned or implied):
- Make: GMC or Chevrolet
- Model: Denali or Silverado 1500
- Certified Pre-Owned
- Year: 2017 or newer
- Mileage: under 30,000
- Drive: 4WD (four-wheel drive)
- Doors: 4
- Leather seats
- Heated and cooled seats
- Electrically adjustable seats
- No eco or hybrid features
- Premium tires
- Full-length running boards

💡 Preferred features (you may ignore if missing):
- No GPS system
- No DVD system
- Hard shell truck bed cover
- Carpet interior
- Towing package
- Color (already filtered elsewhere)

Vehicle Listing:
{description}
"""

    # Optional: print the prompt for debugging
    # print(f"[DEBUG] Sending prompt to OpenAI:\n{prompt}")

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        decision = resp.choices[0].message.content.strip().lower()
        print(f"[DEBUG] OpenAI decision: {decision}")
        return decision.startswith("yes")
    except Exception as e:
        print(f"[ERROR] OpenAI request failed: {e}")
        return False
