import os
import numpy as np

from .load_model import load_clip_model
from .image_embeddings import generate_image_embeddings
from .text_embeddings import generate_text_embedding
from .match import match_text_to_image

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

CSV_PATH = os.path.join(BASE_DIR, "..", "data", "autism_dataset.csv")
IMAGE_ROOT = os.path.join(BASE_DIR, "..", "data")
EMBEDDINGS_PATH = os.path.join(BASE_DIR, "..", "data", "image_embeddings.npy")
PATHS_PATH = os.path.join(BASE_DIR, "..", "data", "image_paths.npy")

print("🚀 Initializing Text-to-Image Service...")

model, preprocess, device = load_clip_model()
print(f"✅ CLIP Loaded on {device.upper()}")

# -------------------------
# CHECK IF EMBEDDINGS EXIST
# -------------------------

if os.path.exists(EMBEDDINGS_PATH) and os.path.exists(PATHS_PATH):
    print("⚡ Loading saved embeddings...")
    image_embeddings = np.load(EMBEDDINGS_PATH)
    image_paths = np.load(PATHS_PATH, allow_pickle=True)
else:
    print("⏳ Generating image embeddings (first time only)...")
    image_embeddings, image_paths = generate_image_embeddings(
        model=model,
        understand=preprocess,
        device=device,
        csv_path=CSV_PATH,
        image_root=IMAGE_ROOT
    )

    # Save for future use
    np.save(EMBEDDINGS_PATH, image_embeddings)
    np.save(PATHS_PATH, image_paths)

print(f"✅ {len(image_paths)} images ready")


# -------------------------
# API FUNCTION
# -------------------------

def generate_image_from_text(text_input: str):

    text_embedding = generate_text_embedding(
        model=model,
        device=device,
        text_list=[text_input]
    )

    best_image, score = match_text_to_image(
        text_embedding=text_embedding,
        image_embeddings=image_embeddings,
        image_paths=image_paths
    )

    return best_image, float(score)