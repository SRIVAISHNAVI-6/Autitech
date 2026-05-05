def match_text_to_image(text_embedding, image_embeddings, image_paths):
    similarity = (text_embedding @ image_embeddings.T).squeeze(0)
    best_index = similarity.argmax().item()
    return image_paths[best_index], similarity[best_index].item()
