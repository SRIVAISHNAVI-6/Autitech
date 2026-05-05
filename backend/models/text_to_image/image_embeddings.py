import torch
import pandas as pd
from PIL import Image
import os

def generate_image_embeddings(model, understand, device, csv_path, image_root):
    df = pd.read_csv(csv_path)

    image_embeddings = []
    image_paths = []

    for _, row in df.iterrows():
        img_path = os.path.join(image_root, row["image_path"])

        if not os.path.exists(img_path):
            continue

        image = understand(Image.open(img_path).convert("RGB")).unsqueeze(0).to(device)

        with torch.no_grad():
            embedding = model.encode_image(image)
            embedding = embedding / embedding.norm(dim=-1, keepdim=True)

        image_embeddings.append(embedding)
        image_paths.append(img_path)

    return torch.cat(image_embeddings), image_paths

