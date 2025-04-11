import whisper
import tempfile
import numpy as np
import soundfile as sf

model = whisper.load_model("base")

def transcribe_audio(audio_bytes):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        sf.write(tmp.name, np.frombuffer(audio_bytes, dtype=np.int16), 16000)
        result = model.transcribe(tmp.name)
    return result["text"]