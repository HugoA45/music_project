
'''
Streamlit function
UNTIL CKPT IS ON CLOUD, THIS CAN CURRENTLY ONLY BE RUN LOCALLY
'''

import sys
sys.path.insert(0, '../')

# 1. Import packages

# 1.1 Python packages
import streamlit as st
import numpy as np
import pandas as pd

# 1.2 Model Tasks
from main import main # Coding in progress



# 2. Website
st.markdown("""# FEED ME MUSIC""")


# 2.1 Load MP3
input_file = st.file_uploader("Upload an MP3 file", type=["mp3"]) # The st.file_uploader function returns a BytesIO object for the uploaded file.

# 2.2 run input_file thru main function to predict composer
if input_file is not None:
    # Process the input_file as needed for your main() function
    # 2.2 Run prediction
    composer = main(input_file)


# 2.3 While prediction is running, generate 'possible' composers
guess1, guess2, guess3 = 'guess' #create function for random composer output?

st.write(f'The composer of this song is..')

image_path = "path/to/your/image.jpg"  # Replace with img path (save in file_paths)
st.image(image_path, caption={guess1}, use_column_width=True)


st.write(f'but perhaps it could also be {guess2}')

st.write(f'Well, actually, the composer is {composer}')
