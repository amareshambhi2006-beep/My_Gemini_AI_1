import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# API Key ಸೆಟಪ್
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    # ಒಂದು ವೇಳೆ Render ನಲ್ಲಿ ಸೆಟ್ ಮಾಡದಿದ್ದರೆ ಇಲ್ಲಿ ನೇರವಾಗಿ ಹಾಕಿಕೊಳ್ಳಿ
    API_KEY = "AIzaSyChCaYwSLX9umtNUETkflkdNtpGoyKjNoA"

genai.configure(api_key=API_KEY)

# ಮಾಡೆಲ್ ಸೆಟಪ್
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"reply": "ಏನಾದರೂ ಟೈಪ್ ಮಾಡಿ ಅಪ್ಪಾಜಿ."})

    try:
        # ಸರಳವಾಗಿ ಉತ್ತರ ಪಡೆಯುವ ವಿಧಾನ (ಮೆಮೊರಿ ಇಲ್ಲದೆ ಮೊದಲು ಚೆಕ್ ಮಾಡೋಣ)
        response = model.generate_content(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "ಕ್ಷಮಿಸಿ ಅಪ್ಪಾಜಿ, ಸರ್ವರ್‌ನಲ್ಲಿ ತೊಂದರೆಯಾಗಿದೆ. ಮತ್ತೊಮ್ಮೆ ಪ್ರಯತ್ನಿಸಿ."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
