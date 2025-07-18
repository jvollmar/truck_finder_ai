import openai
from config import OPENAI_API_KEY, REQUIRED_FEATURES, SUGGESTED_FEATURES

openai.api_key = OPENAI_API_KEY
print(f"[DEBUG] OpenAI API Key Loaded: {bool(openai.api_key)}")

def is_vehicle_match(description: str) -> bool:
    required_text = "\n".join(f"- {item}" for item in REQUIRED_FEATURES)
    suggested_text = "\n".join(f"- {item}" for item in SUGGESTED_FEATURES)

    prompt = f"""
You are a strict filter for a vehicle buyer. Determine if the following vehicle listing matches **ALL required criteria** below. Only answer with YES or NO — do not explain your answer.

❗ Required features (must all be clearly mentioned or implied):
{required_text}

💡 Preferred features (you may ignore if missing):
{suggested_text}

Vehicle Listing:
{description}
"""

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
