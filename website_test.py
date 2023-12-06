
'''
Streamlit function
'''

# 1. Import packages
# 1.1 Python packages

import streamlit as st
import numpy as np
import pandas as pd
import time


# 1.2 Model Tasks
from main_2 import main # UPDATE TO MAIN

# 2. Website

# 2.1 Website Function: typewriter
def typewriter(text: str, speed=10):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)


 # 2.2 Website Layout: banner & header
st.markdown("""
<style>
.banner {
  background: #000000;
  color: white;
  padding: 10px;
  position: relative;
  text-align: center;
  border-radius: 10px;
  max-height: 400px;  /* Set the maximum height of the banner */
  overflow: hidden;  /* Hide the excess part of the image */
}
</style>

<div class="banner">
  <h1>TuneScout</h1>
  <img src="https://via.placeholder.com/150" "">
  <p>For the audiophiles,<br>the minstrels of melody,<br>the ones that never heard enough</p>
</div>
""", unsafe_allow_html=True)

# banner_image = "resources/Images of Composers/bethel_church.png"  # Replace with image URL
# st.image(banner_image, use_column_width=True)

# st.markdown("""# FEED ME MUSIC""")



# 2.1 Load MP3
input_file = st.file_uploader('',type=["mp3"]) # The st.file_uploader function returns a BytesIO object for the uploaded file.

composer = None

if input_file is not None:
    import requests
    url = "https://music-fbzdapc47q-ew.a.run.app" # change for API URL
    files = {'file': input_file}
    response = requests.post(url,files=files).json()
    for i, (composer, percentage) in enumerate(response.items()): #ensure correct output
        if i == 0:
            typewriter(f'I think the composer is {composer}')
        else:
            typewriter(f'But it could alse be {composer}')


# 2.2 run input_file thru main function to predict composer

# if composer is not None:
#     for i, row in composer.iterrows():
#         if row is not None:
#             image_path = "/Users/d.haverkort/code/HugoA45/music_project/music_project/temp/bethel_church.png"

#             st.image(image_path, caption={row["Composer"]}, use_column_width=True)

#     for i, row in composer.iterrows():
#         if i == 0:
#             typewriter(f'I think the composer is {row["Composer"]}')
#         else:
#             typewriter(f'But it could alse be {row["Composer"]}')
# else:
#     st.write("Composer not found or input file not provided.")
