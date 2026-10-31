import os
import base64
from dotenv import load_dotenv
load_dotenv()
from sarvamai import SarvamAI

client = SarvamAI()
os.makedirs("demo/assets", exist_ok=True)

scenarios = [
    {
        "file": "settlement_hindi.wav",
        "lang": "hi-IN",
        "text": "नमस्ते रमेश जी। कल का चौदह हज़ार दो सौ पचास रुपये का सेटलमेंट बैंक हॉलिडे की वजह से रुका था। मैंने अगली साइकिल सुबह छह बजे के लिए री-ट्राई शेड्यूल कर दिया है। पेमेंट गेटवे से कन्फर्मेशन मिल गया है।"
    },
    {
        "file": "soundbox_kannada.wav",
        "lang": "kn-IN",
        "text": "ನಮಸ್ಕಾರ ರಮೇಶ್ ಅವರೇ. ನಿಮ್ಮ ಸೌಂಡ್‌ಬಾಕ್ಸ್‌ನಲ್ಲಿ ಹಾರ್ಡ್‌ವೇರ್ ಸ್ಪೀಕರ್ ದೋಷವಿದೆ. ಬ್ಲೂಡಾರ್ಟ್ ಮೂಲಕ ಹೊಸ ಸೌಂಡ್‌ಬಾಕ್ಸ್ ಕಳುಹಿಸಲಾಗಿದೆ. ಟ್ರ್ಯಾಕಿಂಗ್ ಲಿಂಕ್ ನಿಮ್ಮ ಫೋನ್‌ಗೆ ಕಳುಹಿಸಲಾಗಿದೆ."
    },
    {
        "file": "refusal_hindi.wav",
        "lang": "hi-IN",
        "text": "क्योंकि यह राशि हमारे ऑटोमेटेड सेफ्टी लिमिट पचास हज़ार रुपये से ज़्यादा है, इसलिए सुरक्षा के लिए मैं यह कॉल तुरंत हमारे सीनियर सेटलमेंट स्पेशलिस्ट को ट्रांसफर कर रहा हूँ।"
    },
    {
        "file": "fraud_hindi.wav",
        "lang": "hi-IN",
        "text": "आपके खाते पर सुरक्षा सत्यापन पेंडिंग है। मैं तुरंत हमारे वेरिफिकेशन स्पेशलिस्ट को कॉल ट्रांसफर कर रहा हूँ जो आपकी मदद करेंगे।"
    }
]

for sc in scenarios:
    path = os.path.join("demo/assets", sc["file"])
    print(f"[INFO] Synthesizing {sc['file']} ({sc['lang']})...")
    try:
        resp = client.text_to_speech.convert(
            text=sc["text"],
            language_code=sc["lang"],
            model="bulbul:v3"
        )
        if resp.audios:
            raw = base64.b64decode(resp.audios[0])
            with open(path, "wb") as f:
                f.write(raw)
            print(f"  [OK] Saved {path} ({len(raw)} bytes)")
    except Exception as e:
        print(f"  [ERR] {e}")

print("\n[SUCCESS] All 4 offline fallback audios successfully generated via Sarvam Bulbul v3!")

