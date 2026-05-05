import streamlit as st
from backend.models.text_to_image.service import generate_image_from_text
from backend.models.text_to_speech.service import process_image
from backend.models.speech_to_text.service import transcribe_audio

st.title("AutiTech 🚀")

# -----------------------------
# 1️⃣ TEXT TO IMAGE
# -----------------------------
st.header("Text to Image")

text_input = st.text_input("Enter text")

if st.button("Generate Image"):
    if text_input:
        image_path, score = generate_image_from_text(text_input)
        st.image(image_path)
        st.write(f"Similarity Score: {score}")
    else:
        st.warning("Please enter text")


# -----------------------------
# 2️⃣ IMAGE TO SPEECH
# -----------------------------
st.header("Image to Speech")

uploaded_image = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    if st.button("Process Image"):
        image_name, text, audio_file = process_image(uploaded_image)

        if image_name is None:
            st.error("Image not found in dataset")
        else:
            st.image(uploaded_image)
            st.write(f"Extracted Text: {text}")
            st.audio(audio_file)


# -----------------------------
# 3️⃣ SPEECH TO TEXT
# -----------------------------
st.header("Speech to Text")

uploaded_audio = st.file_uploader("Upload Audio", type=["wav", "mp3"])

if uploaded_audio is not None:
    if st.button("Convert Speech"):
        original, corrected = transcribe_audio(uploaded_audio)

        st.write(f"Original: {original}")
        st.write(f"Corrected: {corrected}")