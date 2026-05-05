import os
import numpy as np

from .load_model import load_clip_model
from .image_embeddings import generate_image_embeddings
from .text_embeddings import generate_text_embedding
from .match import match_text_to_image

# -------------------------
# PATH SETUP (FIXED ✅)
# -------------------------

# Absolute path to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go to project root (autitech/)
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../../"))

# Correct paths
DATA_DIR = os.path.join(ROOT_DIR, "data")

CSV_PATH = os.path.join(DATA_DIR, "autism_dataset.csv")
IMAGE_ROOT = DATA_DIR
EMBEDDINGS_PATH = os.path.join(DATA_DIR, "image_embeddings.npy")
PATHS_PATH = os.path.join(DATA_DIR, "image_paths.npy")

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
# MAIN FUNCTION
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

    # -------------------------
    # 🔥 FIX PATH HERE
    # -------------------------

    # Convert to absolute path if needed
    if not os.path.isabs(best_image):
        best_image = os.path.join(ROOT_DIR, best_image)

    # Normalize path (important for Linux)
    best_image = os.path.normpath(best_image)

    return best_image, float(score)