import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# API Key ಸೆಟಪ್
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    # Render ನಲ್ಲಿ ಕೀ ಸಿಗದಿದ್ದರೆ ಇಲ್ಲಿರುವ ನಿಮ್ಮ ಕೀ ಬಳಸುತ್ತದೆ
    API_KEY = "AIzaSyAQdnlD-kue71dYUH1o7U0QXEbEmM-mcj4"

# ಲೇಟೆಸ್ಟ್ API ವರ್ಷನ್ ಬಳಸಲು ಕಾನ್ಫಿಗರೇಶನ್
genai.configure(api_key=API_KEY)

# ಮಾಡೆಲ್ ಸೆಟ್ಟಿಂಗ್ - ಇಲ್ಲಿ ನಿಖರವಾದ ಲೇಟೆಸ್ಟ್ ಹೆಸರು ನೀಡಲಾಗಿದೆ
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
        # ನೇರವಾಗಿ ಉತ್ತರ ಪಡೆಯುವ ಸರಳ ವಿಧಾನ
        response = model.generate_content(user_message)
        
        # ಸರಿಯಾದ ಉತ್ತರ ಬಂದಿದೆಯೇ ಎಂದು ಪರೀಕ್ಷಿಸುವುದು
        if response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "ಕ್ಷಮಿಸಿ ಅಪ್ಪಾಜಿ, ಉತ್ತರ ನೀಡಲು ಸಾಧ್ಯವಾಗುತ್ತಿಲ್ಲ."})
            
    except Exception as e:
        print(f"Error logic: {e}")
        # ಎರರ್ ಬಂದಾಗ ಬಳಕೆದಾರರಿಗೆ ಸುಲಭವಾಗಿ ಅರ್ಥವಾಗುವ ಸಂದೇಶ
        return jsonify({"reply": "ಸರ್ವರ್ ಸಂಪರ್ಕದಲ್ಲಿ ತೊಂದರೆಯಾಗಿದೆ, ದಯವಿಟ್ಟು 1 ನಿಮಿಷ ಬಿಟ್ಟು ಪ್ರಯತ್ನಿಸಿ ಅಪ್ಪಾಜಿ."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
