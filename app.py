import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# API Key ಪಡೆಯುವುದು - ಇಲ್ಲಿ ತಪ್ಪು ಆಗದಂತೆ ಎಚ್ಚರ ವಹಿಸೋಣ
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY or API_KEY == "None":
    # ಒಂದು ವೇಳೆ Render ನಲ್ಲಿ ಸೆಟ್ ಮಾಡದಿದ್ದರೆ ಇಲ್ಲಿ ನೇರವಾಗಿ ನಿಮ್ಮ ಕೀ ಇರಲಿ
    API_KEY = "AIzaSyBVbep69ZkWLx4UMadijJMygN1V68d1Scg"

# API ಕಾನ್ಫಿಗರೇಶನ್
genai.configure(api_key=API_KEY)

# ಮಾಡೆಲ್ ಸೆಟ್ಟಿಂಗ್ - ಇಲ್ಲಿ ಅತ್ಯಂತ ಸ್ಥಿರವಾದ ಹೆಸರನ್ನು ಬಳಸೋಣ
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
        # ನೇರವಾಗಿ ಚಾಟ್ ಮಾಡುವ ಸರಳ ವಿಧಾನ
        response = model.generate_content(user_message)
        
        if response and response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "ಕ್ಷಮಿಸಿ ಅಪ್ಪಾಜಿ, ಉತ್ತರ ಪಡೆಯಲು ಸಾಧ್ಯವಾಗುತ್ತಿಲ್ಲ."})
            
    except Exception as e:
        # ಎರರ್ ಏನೆಂದು ತಿಳಿಯಲು ಪ್ರಿಂಟ್ ಮಾಡಿ (Render logs ನಲ್ಲಿ ನೋಡಬಹುದು)
        print(f"DEBUG ERROR: {str(e)}")
        
        # ಒಂದು ವೇಳೆ 404 ಅಥವಾ ವರ್ಷನ್ ಸಮಸ್ಯೆ ಇದ್ದರೆ ಈ ಕೆಳಗಿನ ಮೆಸೇಜ್ ತೋರಿಸುತ್ತದೆ
        if "404" in str(e):
            return jsonify({"reply": "API Key ವರ್ಷನ್ ಸಮಸ್ಯೆ ಇದೆ ಅಪ್ಪಾಜಿ. ದಯವಿಟ್ಟು ಹೊಸ API Key ಕ್ರಿಯೇಟ್ ಮಾಡಿ ಅಪ್‌ಡೇಟ್ ಮಾಡಿ."})
        
        return jsonify({"reply": "ಸರ್ವರ್ ಇನ್ನು ರೆಡಿ ಆಗಿಲ್ಲ ಅಪ್ಪಾಜಿ, 1 ನಿಮಿಷ ಬಿಟ್ಟು 'Refresh' ಮಾಡಿ ನೋಡಿ."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
