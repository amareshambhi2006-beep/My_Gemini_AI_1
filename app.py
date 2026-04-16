import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- ಅತಿ ಮುಖ್ಯವಾದ ಭಾಗ ---
# Render ನ Environment ನಲ್ಲಿ GEMINI_API_KEY ಅಂತ ಹೆಸರು ಕೊಡಿ
# ಒಂದು ವೇಳೆ ಅದು ಕೆಲಸ ಮಾಡದಿದ್ದರೆ, ಕೆಳಗಿನ ಸಾಲಿನಲ್ಲಿ ನೇರವಾಗಿ ನಿಮ್ಮ ಕೀ ಪೇಸ್ಟ್ ಮಾಡಿ
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY or len(API_KEY) < 10:
    # ನಿಮ್ಮ ಹೊಸ API Key ಅನ್ನು ಇಲ್ಲಿ ಹಾಕಲೇಬೇಕು
    API_KEY = "AQ.Ab8RN6K9MDL9MT4yxCGso1Uzdrv3dUna5JcRe_erAiF3rMpKdA"

genai.configure(api_key=API_KEY)

# ಮಾಡೆಲ್ ಸೆಟಪ್
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({"reply": "ಏನಾದರೂ ಟೈಪ್ ಮಾಡಿ ಅಪ್ಪಾಜಿ."})

    try:
        # ನೇರವಾಗಿ ರೆಸ್ಪಾನ್ಸ್ ಪಡೆಯುವುದು
        response = model.generate_content(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        # ಎರರ್ ಬಂದಾಗ ಲೋಗ್ಸ್‌ನಲ್ಲಿ ಕಾಣಿಸಲು ಇದು ಸಹಕಾರಿ
        print(f"ERROR: {str(e)}")
        return jsonify({"reply": "API Key ಅಥವಾ ಇಂಟರ್ನೆಟ್ ಸಮಸ್ಯೆ ಇರಬಹುದು ಅಪ್ಪಾಜಿ. ಒಮ್ಮೆ ಚೆಕ್ ಮಾಡಿ."})

if __name__ == '__main__':
    # Render ಸರ್ವರ್ ಪೋರ್ಟ್ ಪಡೆಯಲು
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
