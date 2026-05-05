import os
import pandas as pd
from faster_whisper import WhisperModel

# -------------------------
# PATH SETUP
# -------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

DATA_PATH = os.path.join(BASE_DIR, "data", "sp_to_te_dataset.csv")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "data", "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------
# LOAD MODEL
# -------------------------

model = WhisperModel("base", device="cpu")

# -------------------------
# LOAD DATASET
# -------------------------

df = pd.read_csv(DATA_PATH)
df["text"] = df["text"].str.lower().str.strip()

# -------------------------
# FUNCTION
# -------------------------

def transcribe_audio(file):

    # ✅ FIX: use .name instead of .filename
    file_path = os.path.join(UPLOAD_FOLDER, file.name)

    # ✅ FIX: Streamlit file saving
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

    # 🔥 Transcribe
    segments, _ = model.transcribe(
        file_path,
        language="en",
        beam_size=5
    )

    transcript = ""
    for segment in segments:
        transcript += segment.text + " "

    transcript = transcript.strip().lower()

    # Match with dataset
    match = df[df["text"] == transcript]

    if not match.empty:
        corrected_text = match.iloc[0]["text"]
    else:
        corrected_text = transcript.capitalize()

    return transcript, corrected_text