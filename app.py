import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 1. API Key ಸೆಟಪ್
# Render ನ Environment Variable ನಿಂದ ಕೀ ಪಡೆಯುತ್ತದೆ. 
# ಒಂದು ವೇಳೆ ಅಲ್ಲಿ ಸಿಗದಿದ್ದರೆ ನೀವು ನೇರವಾಗಿ ಕೊಟ್ಟಿರುವ ಕೀ ಬಳಸುತ್ತದೆ.
# Render ನಿಂದ ಕೀ ಪಡೆಯುವ ಸರಿಯಾದ ದಾರಿ
API_KEY = os.environ.get("GEMINI_API_KEY")

# ಒಂದು ವೇಳೆ ಮೇಲೆ ಕೀ ಸಿಗದಿದ್ದರೆ, ಈ ಕೆಳಗಿನ ಸಾಲಿನಲ್ಲಿ ನೇರವಾಗಿ ನಿಮ್ಮ ಕೀ ಪೇಸ್ಟ್ ಮಾಡಿ
if not API_KEY:
    API_KEY = "AQ.Ab8RN6JTJYXaAT5mdW5KFdUHfY2iEMQc_zhf_iFQz0wPJ1krXA"

genai.configure(api_key=API_KEY)

# 2. Gemini ಮಾಡೆಲ್ ಸೆಟಪ್ (Latest Version)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    # ನಿಮ್ಮ index.html ಫೈಲ್ ಅನ್ನು ಇದು ಲೋಡ್ ಮಾಡುತ್ತದೆ
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({"reply": "ಏನಾದರೂ ಟೈಪ್ ಮಾಡಿ ಅಪ್ಪಾಜಿ."})

    try:
        # Gemini ನಿಂದ ಉತ್ತರ ಪಡೆಯುವ ದಾರಿ
        response = model.generate_content(user_message)
        
        if response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "ಕ್ಷಮಿಸಿ ಅಪ್ಪaಜಿ, ಉತ್ತರ ನೀಡಲು ಸಾಧ್ಯವಾಗುತ್ತಿಲ್ಲ."})
            
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "ಸರ್ವರ್ ಸಂಪರ್ಕದಲ್ಲಿ ಸಣ್ಣ ತೊಂದರೆಯಾಗಿದೆ, ದಯವಿಟ್ಟು 1 ನಿಮಿಷ ಬಿಟ್ಟು ಪ್ರಯತ್ನಿಸಿ."})

# 3. Render ಗಾಗಿ ಪೋರ್ಟ್ ಸೆಟ್ಟಿಂಗ್ (ಅತಿ ಮುಖ್ಯ)
if __name__ == '__main__':
    # Render ತನ್ನದೇ ಆದ ಪೋರ್ಟ್ ನೀಡುತ್ತದೆ, ಅದನ್ನು ಇಲ್ಲಿ ಬಳಸಲಾಗಿದೆ
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
