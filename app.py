import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ಇಲ್ಲಿ ಹೊಸದಾಗಿ ಕಾಪಿ ಮಾಡಿದ API Key ಪೇಸ್ಟ್ ಮಾಡಿ
API_KEY = os.environ.get("GEMINI_API_KEY") genai.configure(api_key=api_key)
genai.configure(api_key=API_KEY)

# ನಿಮ್ಮ ಸ್ಕ್ರೀನ್‌ನಲ್ಲಿ ತೋರಿಸುತ್ತಿರುವ ಮಾಡೆಲ್ ಹೆಸರು ಇಲ್ಲಿದೆ
model = genai.GenerativeModel('gemini-3-flash-preview')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    try:
        response = model.generate_content(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})

if __name__ == '__main__':
    app.run(debug=True)
