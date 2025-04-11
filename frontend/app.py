import streamlit as st
from streamlit_webrtc import webrtc_streamer
import requests
import av

st.set_page_config(page_title="Voice Assistant", layout="centered")
st.title("🎙️ Talk to Your Assistant")

class AudioProcessor:
    def __init__(self) -> None:
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        self.frames.append(frame)
        return frame

ctx = webrtc_streamer(
    key="speech",
    mode="sendonly",
    audio_receiver_size=256,
    client_settings={"media_stream_constraints": {"audio": True, "video": False}},
    processor_factory=AudioProcessor,
)

if st.button("Submit Audio"):
    if ctx and ctx.processor and ctx.processor.frames:
        st.info("Submitting audio…")
        # Placeholder: You'd add logic here to send audio to your backend
    else:
        st.warning("No audio captured.")
