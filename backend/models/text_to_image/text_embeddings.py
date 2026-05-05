import torch
import clip

def generate_text_embedding(model, device, text_list):
    tokens = clip.tokenize(text_list).to(device)

    with torch.no_grad():
        text_embeddings = model.encode_text(tokens)
        text_embeddings = text_embeddings / text_embeddings.norm(dim=-1, keepdim=True)

    return text_embeddings
