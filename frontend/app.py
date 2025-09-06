import streamlit as st
import requests
from PIL import Image

st.set_page_config(page_title="🤖 Smart Chatbot", page_icon="🤖", layout="centered")

try:
    logo = Image.open("frontend/data/logo.png")
    st.image(logo, width=100)
except:
    pass

st.markdown("<h1 style='color:#0d6efd; text-align:center;'>🤖 Smart Customer Support Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#6c757d; text-align:center;'>Ask your questions and get instant AI-powered answers</h4>", unsafe_allow_html=True)
st.markdown("---")

mode = st.sidebar.selectbox("Choose Theme", ["Light", "Dark"])
if mode == "Dark":
    st.markdown("<style>body{background:#121212; color:white;}</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>body{background:white; color:black;}</style>", unsafe_allow_html=True)

st.markdown("""
<style>
#chat-area {
    max-height: 450px;
    overflow-y: auto;
    padding: 10px;
    background:#1e1e2f;
    border-radius: 15px;
    margin-bottom: 15px;
}
.user-message {
    background:#0d6efd;
    color:white;
    padding: 12px 20px;
    border-radius: 15px 15px 0 15px;
    max-width: 70%;
    margin-left:auto;
    margin-bottom:15px;
    font-weight: 600;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 16px;
}
.bot-message {
    background:#333;
    color:white;
    padding: 12px 20px;
    border-radius: 15px 15px 15px 0;
    max-width: 70%;
    margin-bottom:15px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 16px;
}
input.stTextInput>div>div>input {
    background: #2c2c2c;
    color: white;
    border-radius: 12px;
    padding: 12px;
    font-size: 16px;
}
div.stButton > button:first-child {
    width: 100%;
    background: #0d6efd;
    color: white;
    font-weight: 600;
    font-size: 16px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# Quick reply buttons
col1, col2, col3 = st.columns(3)

if col1.button("Track my order"):
    st.session_state.user_input = "Where is my order?"

if col2.button("Refund Policy"):
    st.session_state.user_input = "Tell me about refund policy"

if col3.button("Talk to Human"):
    st.session_state.user_input = "I want to talk to a human"

if "user_input" in st.session_state and st.session_state.user_input:
    user_input = st.session_state.pop("user_input")
else:
    user_input = st.text_input("Ask your question:", key="input", placeholder="Type your message here...")

if st.button("Send") and user_input:
    st.session_state.history.append(("You", user_input))
    with st.spinner("Bot is typing..."):
        try:
            response = requests.post(
                "http://localhost:5005/webhooks/rest/webhook",
                json={"message": user_input},
                timeout=20
            )
            response.raise_for_status()
            messages = response.json()
            bot_reply = " ".join([m.get("text", "") for m in messages]).strip()
            if not bot_reply:
                bot_reply = "Sorry, I didn't understand that. Please try again."
        except Exception as e:
            bot_reply = f"Error: {str(e)}"

    st.session_state.history.append(("Bot", bot_reply))

st.markdown('<div id="chat-area">', unsafe_allow_html=True)
for sender, msg in st.session_state.history:
    cls = "user-message" if sender == "You" else "bot-message"
    st.markdown(f'<div class="{cls}">{msg}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; font-size:14px; color:gray;">
    Made with ❤️ by Karan Sharma | <a href="https://github.com/yourgithub" target="_blank" style="color:#0d6efd;">GitHub</a> |
    <a href="https://linkedin.com/in/yourprofile" target="_blank" style="color:#0d6efd;">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True,
)
