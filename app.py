import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API Key not found")

genai.configure(api_key=API_KEY)

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
        response = model.generate_content(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"reply": "Error ಬಂದಿದೆ. Logs check ಮಾಡಿ."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
