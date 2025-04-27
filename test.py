import streamlit as st
import os
from PIL import Image
import textwrap
import google.generativeai as genai
from IPython.display import Markdown


# Configure API key
os.environ['GMINI_API_KEY'] = "AIzaSyCwMJaaM9lBD-drd2nseUBjITJUW5LjzD4"
genai.configure(api_key=os.environ['GMINI_API_KEY'])

# Helper function to format text as Markdown
def to_markdown(text):
    """Display text as markdown."""
    text = text.replace('*', '  *')
    return textwrap.indent(text, ' >', predicate=lambda _: True)

# Streamlit app
st.title("Generative AI Content Generator")
st.sidebar.header("Options")

# Model selection
model_name = st.sidebar.selectbox(
    "Select Model",
    [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
)
model = genai.GenerativeModel(model_name)

# Input options
input_type = st.sidebar.radio("Input Type", ["Text Prompt", "Image Upload"])

if input_type == "Text Prompt":
    prompt = st.text_area("Enter your prompt:")
    if st.button("Generate Content"):
        with st.spinner("Generating content..."):
            response = model.generate_content(prompt)
            st.markdown(to_markdown(response.text))
elif input_type == "Image Upload":
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        img = Image.open(uploaded_image)
        st.image(img, caption="Uploaded Image", use_column_width=True)
        if st.button("Generate Content from Image"):
            with st.spinner("Generating content..."):
                response = model.generate_content(img)
                st.markdown(to_markdown(response.text))

# Footer
st.sidebar.info("Powered by Google Generative AI")