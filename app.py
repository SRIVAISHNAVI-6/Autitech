import streamlit as st
import os
from PIL import Image

from backend.models.text_to_image.service import generate_image_from_text
from backend.models.text_to_speech.service import process_image
from backend.models.speech_to_text.service import transcribe_audio

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AutiTech", layout="wide")

# -----------------------------
# CUSTOM UI STYLE
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #f5efe6;
}
.title {
    font-size: 40px;
    font-weight: bold;
    color: #5a2d1d;
}
.card {
    background-color: #6b3b2a;
    padding: 20px;
    border-radius: 20px;
    color: white;
}
button {
    background-color: #e6d5c3 !important;
    color: black !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.markdown("<h1 class='title'>AUTITECH 🚀</h1>", unsafe_allow_html=True)

# -----------------------------
# 3 COLUMN LAYOUT
# -----------------------------
col1, col2, col3 = st.columns(3)

# -----------------------------
# TEXT TO IMAGE
# -----------------------------
with col1:
    st.markdown("<div class='card'><h3>🖼️ Text to Image</h3></div>", unsafe_allow_html=True)

    text_input = st.text_input("Enter text")

    if st.button("Generate"):
        if text_input:
            image_path, score = generate_image_from_text(text_input)

            if os.path.exists(image_path):
                st.image(Image.open(image_path))

            st.write(f"Similarity Score: {score}")

# -----------------------------
# IMAGE TO SPEECH
# -----------------------------
with col2:
    st.markdown("<div class='card'><h3>👦 Image to Speech</h3></div>", unsafe_allow_html=True)

    uploaded_image = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

    if uploaded_image:
        if st.button("Convert"):
            image_name, text, audio_file = process_image(uploaded_image)

            st.image(uploaded_image)
            st.write(f"Text: {text}")

            if os.path.exists(audio_file):
                st.audio(audio_file)

# -----------------------------
# SPEECH TO TEXT
# -----------------------------
with col3:
    st.markdown("<div class='card'><h3>🎤 Speech to Text</h3></div>", unsafe_allow_html=True)

    uploaded_audio = st.file_uploader("Upload Audio", type=["wav","mp3"])

    if uploaded_audio:
        if st.button("Transcribe"):
            original, corrected = transcribe_audio(uploaded_audio)

            st.write(f"Original: {original}")
            st.write(f"Corrected: {corrected}")