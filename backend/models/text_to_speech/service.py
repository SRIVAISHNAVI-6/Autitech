import os
import shutil
import pandas as pd
from gtts import gTTS

# Get MAJOR_PRO root directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

DATA_PATH = os.path.join(BASE_DIR, "data", "te_to_sp_dataset.csv")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "data", "uploads")
AUDIO_FOLDER = os.path.join(BASE_DIR, "data", "audio")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Load dataset
DATASET = pd.read_csv(DATA_PATH)
DATASET["image_path"] = DATASET["image_path"].str.strip()


def process_image(file):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save uploaded image
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_name = file.filename

    match = DATASET[DATASET["image_path"] == image_name]

    if match.empty:
        return None, None, None

    text = match.iloc[0]["text"]

    audio_path = os.path.join(AUDIO_FOLDER, "output.mp3")

    tts = gTTS(text=text, lang="en")
    tts.save(audio_path)

    return image_name, text, "output.mp3"