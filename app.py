import os
import pathlib
import torch
import streamlit as st
from fastai.vision.all import load_learner, PILImage
import numpy as np
from PIL import Image
import io

# -----------------------------
# Model loading
# -----------------------------
MODEL_FILENAME = "waste_classifier_resnet50.pkl"
MODEL_PATH = os.path.join(os.path.dirname(__file__), MODEL_FILENAME)

if not os.path.exists(MODEL_PATH):
    alt_path = os.path.join(os.getcwd(), MODEL_FILENAME)
    if os.path.exists(alt_path):
        MODEL_PATH = alt_path
    else:
        st.error(f"Model file '{MODEL_FILENAME}' not found.")
        st.stop()

# Workaround for Linux-exported models on Windows
if os.name == "nt":
    try:
        pathlib.PosixPath = pathlib.WindowsPath  # type: ignore
    except Exception:
        pass

learn = load_learner(MODEL_PATH, cpu=not torch.cuda.is_available())

# -----------------------------
# Binary mapping logic
# -----------------------------
BIODEGRADABLE_SET = {"Biodegradable"}
NON_BIODEGRADABLE_SET = {"Non Biodegradable", "Glass", "Metal", "Hazardous"}

def map_to_binary(class_name: str) -> str:
    return "Biodegradable" if class_name in BIODEGRADABLE_SET else "Non Biodegradable"

def predict_binary(img_bytes):
    # Always convert to PILImage
    pil = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = PILImage.create(pil)

    pred, pred_idx, probs = learn.predict(img)

    vocab = list(map(str, learn.dls.vocab))
    prob_by_class = {vocab[i]: float(probs[i]) for i in range(len(vocab))}
    prob_bio = sum(prob_by_class.get(c, 0.0) for c in BIODEGRADABLE_SET)
    prob_non = sum(prob_by_class.get(c, 0.0) for c in NON_BIODEGRADABLE_SET)

    return {
        "fine_label": str(pred),
        "binary_label": map_to_binary(str(pred)),
        "probabilities": {
            "Biodegradable": prob_bio,
            "Non Biodegradable": prob_non,
        },
    }

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("♻️ Waste Classifier")
st.write("Upload a waste image to classify as **Biodegradable** or **Non Biodegradable**.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read file once into bytes
    image_bytes = uploaded_file.read()

    # Show preview
    st.image(image_bytes, caption="Uploaded Image", use_column_width=True)

    if st.button("Predict"):
        result = predict_binary(image_bytes)
        st.subheader("Prediction")
        st.write(f"**Binary Label:** {result['binary_label']}")
        st.write(f"**Fine Class:** {result['fine_label']}")

        # Progress bar for biodegradable probability
        st.write("Biodegradable Probability")
        st.progress(result["probabilities"]["Biodegradable"])

        st.write(f"Biodegradable: {result['probabilities']['Biodegradable']:.3f}")
        st.write(f"Non Biodegradable: {result['probabilities']['Non Biodegradable']:.3f}")