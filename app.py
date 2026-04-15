import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Render ನಿಂದ ಕೀ ಪಡೆಯುವುದು
key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# ಮಾಡೆಲ್ ಹೆಸರು ಇಲ್ಲಿ ಬದಲಾಗಿದೆ - ಇದು ಅತ್ಯಂತ ಲೇಟೆಸ್ಟ್
model = genai.GenerativeModel('gemini-1.5-flash-8b')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message')
    try:
        # ನೇರವಾಗಿ ಉತ್ತರ ಪಡೆಯುವುದು
        response = model.generate_content(user_msg)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "ಅಪ್ಪಾಜಿ, ಹೊಸ API Key ನೊಂದಿಗೆ 1 ನಿಮಿಷ ಬಿಟ್ಟು 'Refresh' ಮಾಡಿ ನೋಡಿ."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
