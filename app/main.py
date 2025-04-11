from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.whisper_handler import transcribe_audio
from app.gpt_handler import get_gpt_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/listen/")
async def listen(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    transcription = transcribe_audio(audio_bytes)
    response = get_gpt_response(transcription)
    return {
        "you": transcription,
        "gpt": response
    }