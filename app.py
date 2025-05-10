import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
from filters.apply_filter import apply_filter

# إعداد صفحة Streamlit مع تنسيق أصغر
st.set_page_config(page_title="Image Filter GUI")
st.markdown("<style>body {font-size: 14px;}</style>", unsafe_allow_html=True)  # تقليل حجم النصوص
st.title("🖼️ Image Filter GUI")

# تهيئة الحالة إذا لم تكن موجودة
if "original_image" not in st.session_state:
    st.session_state.original_image = None
if "current_image" not in st.session_state:
    st.session_state.current_image = None

# رفع الصورة من المستخدم
st.subheader("Upload Image")
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"], key="uploader")

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        st.session_state.original_image = np.array(image)
        st.session_state.current_image = np.array(image)
        st.success("Image loaded successfully!")
    except Exception as e:
        st.error(f"Error loading image: {e}")

# عرض الصورة الحالية
if st.session_state.current_image is not None:
    st.subheader("Current Image")
    st.image(st.session_state.current_image, caption="Current Image", use_column_width=True)

    # قسم الأزرار لتطبيق الفلاتر
    st.subheader("Apply Filters")
    cols = st.columns(3)  # تقليل عدد الأعمدة إلى 3 لتوفير المساحة

    # قائمة الفلاتر
    filters = [
        "Add noise", "Remove noise", "Mean filter", "Median filter", "Gaussian filter",
        "Gaussian noise", "Erosion", "Dilation", "Opening", "Closing",
        "Boundary extraction", "Region filling", "Global threshold",
        "Adaptive threshold", "Otsu threshold", "Hough", "Watershed"
    ]

    # إنشاء زر لكل فلتر
    for idx, filter_name in enumerate(filters):
        col = cols[idx % 3]  # توزيع الأزرار على 3 أعمدة
        with col:
            if st.button(filter_name, key=f"btn_{filter_name}"):
                try:
                    img_bgr = cv2.cvtColor(st.session_state.current_image, cv2.COLOR_RGB2BGR)
                    filtered_img = apply_filter(img_bgr, filter_name)
                    st.session_state.current_image = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)
                    st.success(f"{filter_name} applied successfully!")
                    st.image(st.session_state.current_image, caption=f"Image after {filter_name}", use_column_width=True)
                except Exception as e:
                    st.error(f"Error applying {filter_name}: {e}")

    # زر إعادة الضبط
    st.subheader("Reset")
    if st.button("Reset to Original", key="reset_btn"):
        if st.session_state.original_image is not None:
            st.session_state.current_image = st.session_state.original_image.copy()
            st.success("Image reset to original!")
            st.image(st.session_state.current_image, caption="Reset Image", use_column_width=True)

    # زر التحميل
    st.subheader("Download")
    try:
        if st.session_state.current_image is not None:
            img_pil = Image.fromarray(st.session_state.current_image)
            buf = io.BytesIO()
            img_pil.save(buf, format="PNG")
            byte_im = buf.getvalue()
            st.download_button(
                label="📥 Download Filtered Image",
                data=byte_im,
                file_name="filtered_image.png",
                mime="image/png",
                key="download_btn"
            )
        else:
            st.warning("No image to download. Please apply a filter first.")
    except Exception as e:
        st.error(f"Error preparing download: {e}")
else:
    st.info("Please upload an image to start.")
