import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

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

# Get absolute path for images
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "images")
IMAGE_PATHS = {item: os.path.join(IMAGE_FOLDER, f"{item.lower()}.png") for item in DICE_OPTIONS}

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

# Streamlit UI
st.title("🎲 StoryCraft: Collaborative Storytelling with Dice")

tab1, tab2 = st.tabs(["Generate Story", "Itinerary"])

# Story Generation Tab
with tab1:
    st.header("Select the dice outcomes:")
    selected_items = [st.selectbox(f"Dice {i+1}", DICE_OPTIONS, key=f"dice_{i}") for i in range(4)]

    if st.button("Generate Story"):
        with st.spinner("Generating your story..."):
            prompt = generate_prompt(selected_items)
            story = get_story_from_gemini(prompt)
            st.subheader("Your Story:")
            st.write(story)

# Itinerary Page
with tab2:
    st.header("Dice Faces & Images")
    col1, col2, col3, col4 = st.columns(4)

    for idx, item in enumerate(DICE_OPTIONS):
        image_path = IMAGE_PATHS.get(item, None)
        if image_path and os.path.exists(image_path):
            with (col1 if idx % 4 == 0 else col2 if idx % 4 == 1 else col3 if idx % 4 == 2 else col4):
                st.image(image_path, caption=item, use_column_width=True)
        else:
            st.error(f"Image not found: {image_path}")

st.info("This tool encourages parents to create meaningful stories with their children while fostering creativity and imagination.")
