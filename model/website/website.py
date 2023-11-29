# 1. Import packages

# 1.1 Python packages
import streamlit as st
import numpy as np
import pandas as pd

# 1.2 Model Features
from model_prediction.py import prediction


# 2. Website Structure
st.markdown("""# FEED ME MUSIC""")


# 2.1 Load MP3
mp3_file = st.file_uploader("Upload an MP3 file", type=["mp3"])

if mp3_file is not None:
    # Process the uploaded file (you can add your logic here)
    st.audio(mp3_file, format='audio/mp3', start_time=0)

# Process data
# 2.2 Transform mp3 to midi

# 2.3 Tokenize the data
# Fetch model from container


# 2.4 Predict composer
#composer = predict_composer(midi_file_path)

# 2.5 Generate image
