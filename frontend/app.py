import streamlit as st
import requests

st.set_page_config(page_title="Voice Assistant", layout="wide")
st.title("🎤 Voice Assistant (GPT-4 Turbo)")

uploaded_file = st.file_uploader("Upload your voice (.wav, 16kHz mono)", type=["wav"])

if uploaded_file is not None:
    with st.spinner("Sending to assistant..."):
        response = requests.post("https://your-backend-url.onrender.com/listen/", files={"file": uploaded_file})
        data = response.json()
        st.markdown(f"**🗣️ You:** {data['you']}")
        st.markdown(f"**🤖 GPT:** {data['gpt']}")