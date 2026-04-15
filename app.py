import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ನಿಮ್ಮ API Key ಅನ್ನು ಇಲ್ಲಿ ನೇರವಾಗಿ ನೀಡಲಾಗಿದೆ
API_KEY = "AIzaSyChCaYwSLX9umtNUETkflkdNtpGoyKjNoA"
genai.configure(api_key=API_KEY)

# ಮಾಡೆಲ್ ಸೆಟ್ಟಿಂಗ್ - ಇಲ್ಲಿ 'models/' ಸೇರಿಸುವುದು ಅತಿ ಮುಖ್ಯ
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# ಮೆಮೊರಿಗಾಗಿ ಚಾಟ್ ಸೆಷನ್
chat_session = model.start_chat(history=[])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global chat_session
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({"reply": "ಏನಾದರೂ ಟೈಪ್ ಮಾಡಿ ಅಪ್ಪಾಜಿ."})

    try:
        # ಹಳೆಯ ವಿಷಯ ನೆನಪಿಟ್ಟುಕೊಳ್ಳಲು send_message ಬಳಸಲಾಗಿದೆ
        response = chat_session.send_message(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        # ಎರರ್ ಬಂದರೆ ಸೆಷನ್ ರೀಸ್ಟಾರ್ಟ್ ಮಾಡಿ ಉತ್ತರ ಪಡೆಯಲು
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_message)
        return jsonify({"reply": response.text})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
