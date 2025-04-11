import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import numpy as np
import queue
import requests
import tempfile
import soundfile as sf

BACKEND_URL = "http://<YOUR-BACKEND-IP>:8000/listen/"  # Replace with your backend IP

# === Streamlit UI ===
st.set_page_config(page_title="Voice Assistant", layout="wide")
st.title("🧠 Real-time Voice Assistant")
st.markdown("🎙️ Speak into your mic, and get GPT responses in real-time.")

# === Audio Capture Queue ===
audio_queue = queue.Queue()

# === Custom Audio Processor ===
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recorded_frames = []
        self.counter = 0

    def recv(self, frame):
        audio = frame.to_ndarray()
        audio_queue.put(audio)
        self.counter += 1

        # Collect 3 seconds of audio before sending
        if self.counter >= 60:  # 20 fps * 3 sec
            self.save_and_process_audio()
            self.counter = 0
            self.recorded_frames.clear()
        else:
            self.recorded_frames.append(audio)

        return frame

    def save_and_process_audio(self):
        audio_data = np.concatenate(self.recorded_frames, axis=0)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            sf.write(tmpfile.name, audio_data, samplerate=16000)
            files = {'file': open(tmpfile.name, 'rb')}

            try:
                response = requests.post(BACKEND_URL, files=files)
                if response.status_code == 200:
                    result = response.json()
                    with st.expander(f"🗣️ You: {result.get('you', '[No transcription]')}", expanded=True):
                        st.markdown(f"🤖 GPT: {result.get('gpt', '[No response]')}")
                else:
                    st.error("❌ Failed to get response from backend")
            except Exception as e:
                st.error(f"⚠️ Exception: {e}")

# === WebRTC Streamer ===
webrtc_streamer(
    key="gpt_voice_stream",
    mode=WebRtcMode.SENDRECV,  # ✅ use enum instead of string
    ...
)