import os
import pandas as pd
from gtts import gTTS

# -------------------------
# PATH SETUP
# -------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

DATA_PATH = os.path.join(BASE_DIR, "data", "te_to_sp_dataset.csv")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "data", "uploads")
AUDIO_FOLDER = os.path.join(BASE_DIR, "data", "audio")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# -------------------------
# LOAD DATASET
# -------------------------

DATASET = pd.read_csv(DATA_PATH)
DATASET["image_path"] = DATASET["image_path"].str.strip()

# -------------------------
# FUNCTION
# -------------------------

def process_image(file):

    # ✅ FIX: use .name
    file_path = os.path.join(UPLOAD_FOLDER, file.name)

    # ✅ FIX: save file correctly
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

    image_name = file.name

    # Match dataset
    match = DATASET[DATASET["image_path"] == image_name]

    if match.empty:
        return None, None, None

    text = match.iloc[0]["text"]

    # Save audio
    audio_path = os.path.join(AUDIO_FOLDER, "output.mp3")

    tts = gTTS(text=text, lang="en")
    tts.save(audio_path)

    return image_name, text, audio_path