
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# Helper functions for filters
from filters import apply_filter

st.set_page_config(page_title="Image Filter GUI", layout="centered")
st.title("🖼️ Image Filter GUI with Streamlit")

if "original_image" not in st.session_state:
    st.session_state.original_image = None
if "current_image" not in st.session_state:
    st.session_state.current_image = None

uploaded_file = st.file_uploader("Browse an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.session_state.original_image = np.array(image)
    st.session_state.current_image = np.array(image)

if st.session_state.current_image is not None:
    st.image(st.session_state.current_image, caption="Current Image", use_column_width=True)

    filters = [
        "None", "Add noise", "Remove noise", "Mean filter", "Median filter", "Gaussian filter",
        "Gaussian noise", "Erosion", "Dilation", "Opening", "Closing",
        "Boundary extraction", "Region filling", "Global threshold",
        "Adaptive threshold", "Otsu threshold", "Hough", "Watershed"
    ]

    selected_filter = st.selectbox("Choose a filter", filters)

    if selected_filter != "None":
        if st.button("Apply Filter"):
            st.session_state.current_image = apply_filter(st.session_state.current_image, selected_filter)
            st.experimental_rerun()


    # Allow user to download the current image
    img_pil = Image.fromarray(st.session_state.current_image)
    buf = io.BytesIO()
    img_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label="📥 Download Image",
        data=byte_im,
        file_name="filtered_image.png",
        mime="image/png"
    )


    if st.button("Reset Image"):
        st.session_state.current_image = st.session_state.original_image.copy()
        st.experimental_rerun()


    # Allow user to download the current image
    img_pil = Image.fromarray(st.session_state.current_image)
    buf = io.BytesIO()
    img_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label="📥 Download Image",
        data=byte_im,
        file_name="filtered_image.png",
        mime="image/png"
    )

