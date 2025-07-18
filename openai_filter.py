import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# ✅ Debug line: check if key is loaded
print(f"[DEBUG] OpenAI API Key Loaded: {bool(openai.api_key)}")

def is_vehicle_match(description: str) -> bool:
    prompt = f"""
You’re a filter. Is the following listing fully compliant with all given criteria? Only answer YES or NO.

{description}
"""
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}]
    )
    return resp.choices[0].message.content.strip().lower().startswith("yes")
