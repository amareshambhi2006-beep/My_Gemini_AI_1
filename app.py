import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Render ನಿಂದ API Key ಪಡೆದುಕೊಳ್ಳುವುದು
API_KEY = os.environ.get("GEMINI API KEY")
genai.configure(api_key=API_KEY)

# ಮಾಡೆಲ್ ಸೆಟ್ ಮಾಡುವುದು
model = genai.GenerativeModel('gemini-1.5-flash')

# ಮೆಮೊರಿಗಾಗಿ ಗ್ಲೋಬಲ್ ಚಾಟ್ ಸೆಷನ್ ಆರಂಭಿಸುವುದು
chat_session = model.start_chat(history=[])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # ಇಲ್ಲಿ ಗ್ಲೋಬಲ್ ಎಂದು ಘೋಷಿಸುವುದನ್ನು ಮೊದಲೇ ಮಾಡಬೇಕು
    global chat_session
    
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({"reply": "ದಯವಿಟ್ಟು ಏನಾದರೂ ಟೈಪ್ ಮಾಡಿ ಅಪ್ಪಾಜಿ."})

    try:
        # Gemini ಗೆ ಮೆಸೇಜ್ ಕಳುಹಿಸುವುದು
        response = chat_session.send_message(user_message)
        return jsonify({"reply": response.text})
    
    except Exception as e:
        # ಏನಾದರೂ ತೊಂದರೆ ಆದರೆ ಸೆಷನ್ ರೀಸ್ಟಾರ್ಟ್ ಮಾಡುವುದು
        try:
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(user_message)
            return jsonify({"reply": response.text})
        except Exception as inner_e:
            return jsonify({"reply": "Error: " + str(inner_e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
