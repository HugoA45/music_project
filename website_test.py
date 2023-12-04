
'''
Streamlit function
UNTIL CKPT IS ON CLOUD, THIS CAN CURRENTLY ONLY BE RUN LOCALLY
'''

# 1. Import packages
# 1.1 Python packages
import streamlit as st
import numpy as np
import pandas as pd
import time

# 1.2 Model Tasks
from deb_main_test import main # UPDATE TO MAIN

def typewriter(text: str, speed=10):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)

# 2. Website
st.markdown("""# FEED ME MUSIC""")

composer = None

# 2.1 Load MP3
input_file = st.file_uploader("Upload an MP3 file", type=["mp3"]) # The st.file_uploader function returns a BytesIO object for the uploaded file.

# 2.2 run input_file thru main function to predict composer
if input_file is not None:
    with open("file.mp3", "wb") as f:
        f.write(input_file.getbuffer())
    # Process the input_file as needed for your main() function
    # 2.2 Run prediction
    composer = pd.DataFrame(main("file.mp3")).reset_index()
    composer.columns = ["Composer", "Prediction"]

if composer is not None:
    for i, row in composer.iterrows():
        if row is not None:
            image_path = "/Users/d.haverkort/code/HugoA45/music_project/music_project/temp/bethel_church.png"

            st.image(image_path, caption={row["Composer"]}, use_column_width=True)

    for i, row in composer.iterrows():
        if i == 0:
            typewriter(f'I think the composer is {row["Composer"]}')
        else:
            typewriter(f'But it could alse be {row["Composer"]}')
else:
    st.write("Composer not found or input file not provided.")
