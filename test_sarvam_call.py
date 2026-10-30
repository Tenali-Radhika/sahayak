import os
import sys
from dotenv import load_dotenv

# Reconfigure stdout for UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 1. Load environment variables from .env
load_dotenv()

api_key = os.getenv("SARVAM_API_KEY")
if not api_key:
    print("[ERROR] SARVAM_API_KEY is not set in environment or .env file.")
    sys.exit(1)

# Masked verification so secret is never printed
print(f"[OK] Found SARVAM_API_KEY in environment ({api_key[:6]}...{api_key[-4:]})")

# 2. Initialize Sarvam AI Client
from sarvamai import SarvamAI

client = SarvamAI()

# 3. Make chat completion call using sarvam-105b-conversations
print("[INFO] Calling Sarvam AI (model: sarvam-105b-conversations)...")
response = client.chat.completions(
    model="sarvam-105b-conversations",
    messages=[
        {
            "role": "user",
            "content": "Namaste! Briefly introduce yourself in one sentence as Sahayak, an AI teammate for Paytm merchants."
        }
    ],
    max_tokens=100
)

# 4. Print response
reply = response.choices[0].message.content
print("\n--- Sarvam AI Response ---")
print(reply)
print("--------------------------\n")
print("[SUCCESS] First live Sarvam AI call completed successfully!")

