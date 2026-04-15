import streamlit as st
import google.generativeai as genai
import os

# Render ನಲ್ಲಿ ನಾವು ಸೆಟ್ ಮಾಡುವ API Key ಅನ್ನು ಇದು ಪಡೆದುಕೊಳ್ಳುತ್ತದೆ
API_KEY = os.environ.get("GEMINI_API_KEY")

# API ಕಾನ್ಫಿಗರೇಶನ್
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("API Key ಕಂಡುಬಂದಿಲ್ಲ. ದಯವಿಟ್ಟು Render Dashboard ನಲ್ಲಿ ಸೆಟ್ ಮಾಡಿ.")
    st.stop()

st.title("ಅಪ್ಪಾಜಿ ಮೆಮೊರಿ ಚಾಟ್‌ಬಾಟ್")

# ಪ್ರಮುಖ ಹಂತ: ಚಾಟ್ સેಷನ್ ಅನ್ನು ಮೆಮೊರಿಯಲ್ಲಿ ಉಳಿಸುವುದು
if "chat_session" not in st.session_state:
    # ಇದು ಮೊದಲ ಬಾರಿ ಮಾತ್ರ રನ್ ಆಗುತ್ತದೆ
    st.session_state.chat_session = model.start_chat(history=[])

# ಹಳೆಯ ಚಾಟ್ ಹಿಸ್ಟರಿಯನ್ನು ಪರದೆಯ ಮೇಲೆ ತೋರಿಸಲು
for message in st.session_state.chat_session.history:
    role = "User" if message.role == "user" else "Assistant"
    with st.chat_message(message.role):
        st.markdown(message.parts[0].text)

# ಬಳಕೆದಾರರಿಂದ ಹೊಸ ಪ್ರಶ್ನೆ ಪಡೆಯುವುದು
if prompt := st.chat_input("ಏನಾದರೂ ಕೇಳಿ..."):
    # ಯೂಸರ್ ಮೆಸೇಜ್ ತೋರಿಸು
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # ಹಳೆಯ ಹಿಸ್ಟರಿಯನ್ನು ಒಳಗೊಂಡಿರುವ સેಷನ್ ಮೂಲಕ ಮೆಸೇಜ್ ಕಳುಹಿಸುವುದು
    try:
        response = st.session_state.chat_session.send_message(prompt)
        # ಅಸಿಸ್ಟೆಂಟ್ ಉತ್ತರ ತೋರಿಸು
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
