import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
from filters.apply_filter import apply_filter

# إعداد صفحة Streamlit
st.set_page_config(page_title="Image Filter GUI", layout="centered")
st.title("🖼️ Image Filter GUI with Streamlit")

# تهيئة الحالة إذا لم تكن موجودة
if "original_image" not in st.session_state:
    st.session_state.original_image = None
if "current_image" not in st.session_state:
    st.session_state.current_image = None

# رفع الصورة من المستخدم
uploaded_file = st.file_uploader("Browse an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        st.session_state.original_image = np.array(image)
        st.session_state.current_image = np.array(image)
    except Exception as e:
        st.error(f"Error loading image: {e}")

# عرض الصورة الحالية
if st.session_state.current_image is not None:
    st.image(st.session_state.current_image, caption="Current Image", use_column_width=True)

    # قائمة الفلاتر المتاحة
    filters = [
        "None", "Add noise", "Remove noise", "Mean filter", "Median filter", "Gaussian filter",
        "Gaussian noise", "Erosion", "Dilation", "Opening", "Closing",
        "Boundary extraction", "Region filling", "Global threshold",
        "Adaptive threshold", "Otsu threshold", "Hough", "Watershed"
    ]

    # اختيار فلتر من القائمة المنسدلة
    selected_filter = st.selectbox("Choose a filter", filters)

    # تطبيق الفلتر عند النقر على الزر
    if selected_filter != "None":
        if st.button("Apply Filter"):
            try:
                # تحويل الصورة إلى BGR لأن OpenCV يستخدم BGR
                img_bgr = cv2.cvtColor(st.session_state.current_image, cv2.COLOR_RGB2BGR)
                filtered_img = apply_filter(img_bgr, selected_filter)
                # تحويل الصورة مرة أخرى إلى RGB للعرض
                st.session_state.current_image = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)
                st.rerun()
            except Exception as e:
                st.error(f"Error applying filter: {e}")

    # زر إعادة الضبط لاستعادة الصورة الأصلية
    if st.button("Reset Image"):
        if st.session_state.original_image is not None:
            st.session_state.current_image = st.session_state.original_image.copy()
            st.rerun()

    # زر التحميل لحفظ الصورة المعدلة
    if st.session_state.current_image is not None:
        try:
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
        except Exception as e:
            st.error(f"Error preparing download: {e}")
else:
    st.info("Please upload an image to start.")

