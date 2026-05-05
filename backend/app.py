from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from models.text_to_image.service import generate_image_from_text
from models.text_to_speech.service import process_image
from models.speech_to_text.service import transcribe_audio
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 FIXED STATIC PATH (VERY IMPORTANT)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")

app.mount("/data", StaticFiles(directory=DATA_DIR), name="data")


@app.get("/")
async def home():
    return {"message": "AutiTech Backend Running 🚀"}


# -----------------------------
# 1️⃣ TEXT TO IMAGE
# -----------------------------
@app.post("/text-to-image/")
async def text_to_image(text: str):

    image_path, score = generate_image_from_text(text)
    filename = os.path.basename(image_path)

    image_url = f"http://127.0.0.1:8000/data/val2017/{filename}"

    return {
        "image_url": image_url,
        "similarity_score": score
    }


# -----------------------------
# 2️⃣ IMAGE TO SPEECH
# -----------------------------
@app.post("/autism-speech/")
async def autism_speech(file: UploadFile = File(...)):

    image_name, text, audio_file = process_image(file)

    if image_name is None:
        return {"error": "Image not found in dataset"}

    image_url = f"http://127.0.0.1:8000/data/uploads/{image_name}"
    audio_url = f"http://127.0.0.1:8000/data/audio/{audio_file}"

    return {
        "image_url": image_url,
        "extracted_text": text,
        "audio_url": audio_url
    }


# -----------------------------
# 3️⃣ SPEECH TO TEXT
# -----------------------------
@app.post("/speech-to-text/")
async def speech_to_text(file: UploadFile = File(...)):

    original, corrected = transcribe_audio(file)

    return {
        "original_text": original,
        "corrected_text": corrected
    }