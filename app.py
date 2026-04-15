import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Render ನಿಂದ API Key ಪಡೆದುಕೊಳ್ಳುವುದು
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# ಮಾಡೆಲ್ ಸೆಟ್ ಮಾಡುವುದು
model = genai.GenerativeModel('gemini-1.5-flash')

# ಮೆಮೊರಿ ಅಥವಾ ಹಿಸ್ಟರಿ ಉಳಿಸಿಕೊಳ್ಳಲು ಗ್ಲೋಬಲ್ ಚಾಟ್ ಸೆಷನ್
# (ಗಮನಿಸಿ: ಇದು ಸರ್ವರ್ ರನ್ ಆಗುವವರೆಗೆ ಮಾತ್ರ ನೆನಪಿಟ್ಟುಕೊಳ್ಳುತ್ತದೆ)
chat_session = model.start_chat(history=[])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({"reply": "ದಯವಿಟ್ಟು ಏನಾದರೂ ಟೈಪ್ ಮಾಡಿ ಅಪ್ಪಾಜಿ."})

    try:
        # generate_content ಬದಲಿಗೆ send_message ಬಳಸಲಾಗಿದೆ (ಇದೇ ಮೆಮೊರಿಗೆ ಮುಖ್ಯ)
        response = chat_session.send_message(user_message)
        return jsonify({"reply": response.text})
    
    except Exception as e:
        # ಒಂದು ವೇಳೆ ಸೆಷನ್ ಎರರ್ ಬಂದರೆ ಹೊಸದಾಗಿ ರೀಸ್ಟಾರ್ಟ್ ಮಾಡಲು
        try:
            global chat_session
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(user_message)
            return jsonify({"reply": response.text})
        except Exception as inner_e:
            return jsonify({"reply": "ಕ್ಷಮಿಸಿ ಅಪ್ಪಾಜಿ, ಸಣ್ಣ ತಾಂತ್ರಿಕ ತೊಂದರೆ ಆಗಿದೆ: " + str(inner_e)})

if __name__ == '__main__':
    # Render ನಲ್ಲಿ ಪೋರ್ಟ್ ಸಮಸ್ಯೆ ಆಗದಂತೆ ಸೆಟ್ಟಿಂಗ್
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
