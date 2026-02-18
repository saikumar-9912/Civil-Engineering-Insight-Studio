import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure API Key
genai.configure(api_key=os.getenv("AIzaSyBGCWjlQGpuqrN_BA0mAbDwzyKyhQ8gh8o"))

# Function to get Gemini response
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit UI
st.set_page_config(page_title="Civil Engineering Insight Studio")

st.header("Civil Engineering Insight Studio")

input_text = st.text_input("Input Prompt: ", key="input")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Describe Structure")

input_prompt = """
You are a Civil Engineering expert. Analyze the uploaded structure image and provide:
- Type of structure
- Materials used
- Construction method
- Dimensions (if visible)
- Engineering challenges
- Special features
"""

if submit:
    if uploaded_file is not None:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_text, image_data, input_prompt)
        st.subheader("Structure Description:")
        st.write(response)
    else:
        st.warning("Please upload an image.")
