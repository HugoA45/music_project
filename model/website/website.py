# 1. Import packages

# 1.1 Python packages
import streamlit as st
import numpy as np
import pandas as pd
from dinis_test import *

# 1.2 Model Features
'''
< Placeholder space for features to be imported >
from model.py import <CONVERSION_FUNCTION_PLACEHOLDER>
import
'''


# 2. Load data
st.markdown("""# FEED ME MUSIC""")


# 2.1 Load MP3
mp3_file = st.file_uploader("Upload an MP3 file", type=["mp3"])


# 3. Process data
# 3.2 Transform mp3 to midi
# 3.3 Tokenize the data
# 3.4 Transform Tokeens to CP


if mp3_file:
# Process the uploaded file from mp3 to CP
    cp = <CONVERSION_FUNCTION_PLACEHOLDER>(mp3_file)

if midi_to_CP:
    prediction = <MODEL_PLACEHOLDER>.predict(cp)
    st.write(prediction)


# Open items - How to
# Fetch model from container (Initiate model)
# 4. Generate image (Optional)
