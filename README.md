# 🖼️ Image Filter GUI with Streamlit

This is a simple yet powerful image filtering GUI built using **Streamlit** and **OpenCV**.
It allows you to upload an image, apply various image processing filters, and download the result.

---

## 📁 Project Structure

```
image_filter_gui_streamlit/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Required Python packages
├── README.md               # Project documentation
│
├── filters/
│   ├── __init__.py
│   └── apply_filter.py     # All filter functions
│
└── images/                 # Optional image storage (currently empty)
```

---

## 🧪 Features

- ✅ Upload and preview images (JPG, PNG)
- ✅ Apply over 18 different filters including:
  - Add/Remove Noise
  - Mean, Median, Gaussian filters
  - Morphological operations: Erosion, Dilation, Opening, Closing
  - Thresholding: Global, Adaptive, Otsu
  - Advanced: Boundary Extraction, Region Filling, Hough Lines, Watershed
- ✅ Reset image to original
- ✅ Download the filtered image

---

## ▶️ How to Run

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the Streamlit app**:
```bash
streamlit run app.py
```

---

## 📥 Output

After applying a filter, a download button will appear allowing you to save the processed image.

---

## 📌 Notes

- All filters are applied sequentially. That means if you apply multiple filters one after another, each builds on the previous result.
- Use the **"Reset Image"** button to go back to the original image.

---

## 💡 Future Ideas

- Save image history
- Compare original vs filtered images side by side
- Add sliders for real-time tuning of filter parameters

Enjoy filtering! ✨