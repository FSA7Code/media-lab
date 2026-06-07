import streamlit as st
from rembg import remove, new_session
from PIL import Image
import io

# Caching the model so it loads only once into memory
@st.cache_resource
def get_model():
    return new_session("u2net")

# Initialize the session
session = get_model()

# Custom Styling
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: #e3e3e3; font-family: 'Google Sans', sans-serif; }
    h1, h2, h3 { color: #e3e3e3; }
    div[data-testid="stFileUploader"] { background-color: #1e1f20; border: 1px solid #3c4043; border-radius: 20px; }
    div.stButton > button { border-radius: 24px; background-color: #a8c7fa; color: #051e49; font-weight: 600; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("AI Background Remover")
st.write("Clean. Simple. AI-Powered.")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original")
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("Processed")
        with st.spinner('Removing background...'):
            output = remove(image, session=session)
            st.image(output, use_container_width=True)
            
            buf = io.BytesIO()
            output.save(buf, format="PNG")
            
            st.download_button(
                label="Download Result",
                data=buf.getvalue(),
                file_name="processed_image.png",
                mime="image/png"
            )