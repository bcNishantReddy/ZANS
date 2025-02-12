import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
from gtts import gTTS
import base64

# Set your Gemini API key (Use st.secrets for better security)
GEMINI_API_KEY = "AIzaSyCkucQ1Egsn0uSr-1FxMYe7BZW4Pp0Ktr8"

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Dice options
DICE_OPTIONS = [
    "Tree", "Crown", "Scorpio", "Feet", "Bee", "Cat",
    "Rocket", "Flower", "Heart", "Castle", "Wolf", "Duck",
    "Star", "Dinosaur", "Aeroplane", "Snake", "Crab"
]

# Ensure images are directly accessed from "images/item.png"
IMAGE_PATHS = {item: f"images/{item.lower()}.png" for item in DICE_OPTIONS}

# Custom CSS for better UI
st.markdown("""
    <style>
        .stApp {
            background: #fdfdfd;
            font-family: Arial, sans-serif;
        }
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #4CAF50;
        }
        .subtitle {
            text-align: center;
            font-size: 22px;
            color: #333;
            margin-bottom: 20px;
        }
        .stButton > button {
            background: #4CAF50;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            padding: 12px 24px;
        }
        .story-box {
            background: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Function to generate a precise prompt for Gemini 1.5
def generate_prompt(selected_items):
    prompt = f"""
    You are a storytelling AI that generates fun, adventurous, and engaging stories for children aged 4-10.
    Use simple yet immersive language that encourages parents to interact with their children while narrating.

    **Story Elements**:
    - Include the following elements in the story: {', '.join(selected_items)}.
    - The story should be **imaginative**, **exciting**, and **child-friendly**.
    - Keep the story **300-500 words**.
    - Include a **moral lesson** at the end to make the story meaningful for kids.

    Format:
    - Title
    - Engaging introduction
    - Adventure with all selected elements
    - Climax with excitement
    - Conclusion with a moral lesson

    The goal is to enrich children's creativity while making storytelling enjoyable for parents.
    """
    return prompt

# Function to fetch story from Gemini 1.5 API
def get_story_from_gemini(prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text if response else "Error generating story."

# Function to convert text to speech (TTS) and provide a download link
def text_to_speech(text):
    tts = gTTS(text, lang="en")
    tts.save("story.mp3")

    with open("story.mp3", "rb") as audio_file:
        audio_bytes = audio_file.read()
        encoded_audio = base64.b64encode(audio_bytes).decode()
        audio_html = f'<audio controls autoplay><source src="data:audio/mp3;base64,{encoded_audio}" type="audio/mp3"></audio>'
        return audio_html

# 🎉 Branding Header
st.markdown("<h1 class='title'>🌟 Welcome to Zans StoryCraft! 🎲</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>A magical world of storytelling and adventure! 🏰📖✨</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📖 Generate Story", "📜 Dice Itinerary"])

# 🎭 Story Generation Tab
with tab1:
    st.header("🎲 Select the dice outcomes:")
    selected_items = [st.selectbox(f"🎲 Dice {i+1}", DICE_OPTIONS, key=f"dice_{i}") for i in range(4)]

    story = ""
    if st.button("📝 Generate Story"):
        with st.spinner("✨ Creating a magical adventure..."):
            prompt = generate_prompt(selected_items)
            story = get_story_from_gemini(prompt)
            st.markdown("<div class='story-box'>", unsafe_allow_html=True)
            st.subheader("📖 Your Story:")
            st.write(story)
            st.markdown("</div>", unsafe_allow_html=True)

    if story:
        if st.button("🔊 Read Aloud"):
            audio_html = text_to_speech(story)
            st.markdown(audio_html, unsafe_allow_html=True)

# 🎨 Itinerary Page with Playful Image Display
with tab2:
    st.header("🎨 Dice Faces & Images")
    col1, col2, col3, col4 = st.columns(4)

    for idx, item in enumerate(DICE_OPTIONS):
        image_path = IMAGE_PATHS.get(item)

        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img.verify()
                img = Image.open(image_path)
                with (col1 if idx % 4 == 0 else col2 if idx % 4 == 1 else col3 if idx % 4 == 2 else col4):
                    st.image(img, caption=item, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading image {image_path}: {str(e)}")
        else:
            st.error(f"Image not found: {image_path}")

st.info("💡 Zans StoryCraft is designed to inspire creativity in children while making storytelling a delightful experience for parents. Have fun! 🎉")
