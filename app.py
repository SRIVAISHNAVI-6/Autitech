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
# BACKGROUND + GLOBAL STYLE
# -----------------------------
st.markdown("""
<style>

/* FULL PAGE BACKGROUND */
[data-testid="stAppViewContainer"] {
    background-color: #f3e9dc;
}

/* REMOVE HEADER WHITE */
[data-testid="stHeader"] {
    background: transparent;
}

/* MAIN TITLE */
.main-title {
    font-size: 55px;
    font-weight: 900;
    color: #5a2d1d;
    margin-bottom: 10px;
}

/* HERO TEXT */
.hero-title {
    font-size: 45px;
    font-weight: 800;
    color: #5a2d1d;
    line-height: 1.2;
}

.hero-desc {
    font-size: 18px;
    color: #5a2d1d;
    max-width: 700px;
}

/* CARD STYLE */
.card {
    background-color: #6b3b2a;
    padding: 20px;
    border-radius: 20px;
    color: white;
}

/* BUTTON STYLE */
button {
    background-color: #e6d5c3 !important;
    color: black !important;
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# MAIN TITLE
# -----------------------------
st.markdown("<div class='main-title'>AUTITECH </div>", unsafe_allow_html=True)

# -----------------------------
# HERO SECTION
# -----------------------------
col1, col2 = st.columns([2,1])

with col1:
    st.markdown("""
    <div class='hero-title'>
    Empowering Autism Through Intelligent Technology
    </div>

    <br>

    <div class='hero-desc'>
    AUTITECH is an AI-powered assistive platform designed to support children with Autism Spectrum Disorder (ASD) by enhancing their communication, learning, and cognitive abilities. Many children with autism face challenges in verbal expression, understanding visual cues, and interacting with their surroundings. AUTITECH addresses these challenges by providing intelligent tools that transform the way children perceive and communicate information. By combining artificial intelligence with user-friendly design, the platform creates an inclusive and engaging learning environment tailored to individual needs.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("assets/hero-boy.jpeg", use_container_width=True)

# SPACE
st.markdown("<br><br>", unsafe_allow_html=True)

# -----------------------------
# 3 COLUMN LAYOUT
# -----------------------------
col1, col2, col3 = st.columns(3)

# -----------------------------
# TEXT TO IMAGE
# -----------------------------
with col1:
    st.markdown("<div class='card'><h3>🖼️ Text to Image</h3></div>", unsafe_allow_html=True)

    text_input = st.text_input("Enter text", key="t2i")

    if st.button("Generate", key="btn1"):
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

    uploaded_image = st.file_uploader("Upload Image", type=["jpg","png","jpeg"], key="img")

    if uploaded_image:
        if st.button("Convert", key="btn2"):
            image_name, text, audio_file = process_image(uploaded_image)

            st.image(uploaded_image)
            st.write(f"Text: {text}")

            if audio_file and os.path.exists(audio_file):
                st.audio(audio_file)

# -----------------------------
# SPEECH TO TEXT
# -----------------------------
with col3:
    st.markdown("<div class='card'><h3>🎤 Speech to Text</h3></div>", unsafe_allow_html=True)

    uploaded_audio = st.file_uploader("Upload Audio", type=["wav","mp3"], key="aud")

    if uploaded_audio:
        if st.button("Transcribe", key="btn3"):
            original, corrected = transcribe_audio(uploaded_audio)

            st.write(f"Original: {original}")
            st.write(f"Corrected: {corrected}")