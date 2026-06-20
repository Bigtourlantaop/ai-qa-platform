import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from src.ai_engine.prompts import SYSTEM_PROMPT, build_test_case_prompt

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

user_story = "As a user, I want to log in with my email and password so that I can access my account."

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,  # เพิ่มจาก 1024 เป็น 4096
    temperature=0.3,
    system=SYSTEM_PROMPT,
    messages=[
        {"role": "user", "content": build_test_case_prompt(user_story)}
    ]
)

raw_text = response.content[0].text
print("--- RAW RESPONSE ---")
print(raw_text)

# ลอง parse เป็น JSON
parsed = json.loads(raw_text)
print("\n--- PARSED SUCCESSFULLY ---")
print(json.dumps(parsed, indent=2, ensure_ascii=False))