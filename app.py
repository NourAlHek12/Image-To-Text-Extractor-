import os
import openai
from dotenv import load_dotenv
from PIL import Image
import pytesseract as tess
import streamlit as st
tess.pytesseract.tesseract_cmd = r'C:\Users\HP\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Load environment variables from .env file
load_dotenv()

# Set the API key from the environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Function to perform OCR on the image
def perform_ocr(image):
    try:
        text = tess.image_to_string(image)
        return text
    except Exception as e:
        st.error(f"Error during OCR: {e}")
        return None

# Function to upload image to OpenAI
def upload_to_openai(image_path):
    with open(image_path, "rb") as image_file:
        response = openai.File.create(
            file=image_file,
            purpose="answers"
        )
    return response['id']

# Function to extract text from an uploaded image
def extract_text(image):
    extracted_text = perform_ocr(image)
    if extracted_text:
        st.write(f"Extracted Text: {extracted_text}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts text from images and provides relevant information."},
                {"role": "user", "content": f"Extracted text: {extracted_text}\n\nProvide a summary or relevant information."}
            ],
            max_tokens=100
        )
        return response.choices[0]['message']['content'].strip()
    else:
        return "Failed to extract text from image"

# Streamlit App
st.title("Image To Text Extractor")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_path = f"temp_image.{uploaded_file.name.split('.')[-1]}"
    image.save(image_path)

    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Extracting text...")

    extracted_text = extract_text(image)
    st.write("Extracted Text from Image:")
    st.write(extracted_text)

    # Upload image to OpenAI
    file_id = upload_to_openai(image_path)
    st.write(f"Uploaded Image ID: {file_id}")

    # Clean up temporary image file
    os.remove(image_path)
