import streamlit as st
import requests
import tempfile
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import av

st.title("🎙️ Pandu's AI Voice Assistant")

st.markdown("Click below and speak. We'll transcribe and respond using GPT.")

class AudioProcessor(AudioProcessorBase):
    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray().flatten().tobytes()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio)
            f.flush()

            # Send to backend API
            files = {'file': open(f.name, 'rb')}
            response = requests.post("http://35.239.162.91:8000/listen/", files=files)
            data = response.json()

            st.session_state["last"] = data
        return frame

webrtc_streamer(
    key="mic",
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False}
)

if "last" in st.session_state:
    st.subheader("You said:")
    st.write(st.session_state["last"]["you"])

    st.subheader("GPT responded:")
    st.write(st.session_state["last"]["gpt"])