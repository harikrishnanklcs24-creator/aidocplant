import streamlit as st
import base64
import google.generativeai as genai
from gtts import gTTS
import os

# -----------------------------
# Configure Gemini
# -----------------------------
API_KEY = "AIzaSyBHiuLjXp3gtW8QK6xqfJgaHtL4APKfGaQ"   # your key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="🌱 Farmer Plant Doctor", layout="centered")
st.title("🌱 Farmer Plant Doctor")
st.write("Upload or capture a photo of your plant leaf, and AI will detect disease & suggest remedies.")

# Upload / Capture image (mobile camera supported)
uploaded_file = st.file_uploader("📷 Capture or Upload Plant Image", type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=False)

if uploaded_file:
    # Show smaller preview
    st.image(uploaded_file, caption="Plant Image", width=250)

    if st.button("🔍 Analyze Plant"):
        try:
            # Read and send to Gemini
            image_data = uploaded_file.read()
            prompt = """
            You are an expert plant pathologist.
            1. Identify if the plant has any disease (if healthy, say Healthy Plant).
            2. If diseased, name the disease.
            3. Give a short list of recommendations farmers can follow to fix the issue.
            Keep answer simple and useful for farmers.
            """
            response = model.generate_content([
                {"role": "user", "parts": [{"text": prompt}]},
                {"role": "user", "parts": [{
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": base64.b64encode(image_data).decode()
                    }
                }]}
            ])

            result = response.text
            st.subheader("🌿 Diagnosis & Recommendations")
            st.write(result)

            # Google TTS
            tts = gTTS(result, lang='en')
            audio_path = "output.mp3"
            tts.save(audio_path)

            # Play Audio
            audio_file = open(audio_path, "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")

            # Clean file
            audio_file.close()
            os.remove(audio_path)

        except Exception as e:
            st.error(f"❌ Error: {e}")
