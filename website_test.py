
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
  <p>For the audiophiles,<br>the musical nomads,<br>the ones who never heard enough</p>
</div>
""", unsafe_allow_html=True)

# banner_image = "resources/Images of Composers/bethel_church.png"  # Replace with image URL
# st.image(banner_image, use_column_width=True)

# st.markdown("""# FEED ME MUSIC""")



# 2.1 Load MP3
input_file = st.file_uploader('',type=["mp3"]) # The st.file_uploader function returns a BytesIO object for the uploaded file.

composer_info_dict = {
                        'Bethel Music': ' Formed in 2001, Bethel Music emerged from Bethel Church in California, specializes in contemporary Christian and worship music. Their style is characterized by modern, dynamic worship songs that blend pop and rock elements with religious themes.',
                        'Richard Clayderman' : 'French pianist Richard Clayderman (born 1953), known for his melodic and romantic style, is a leading figure in new age and pop-classical music. His renditions often feature a blend of popular songs, movie soundtracks, and classical pieces.',
                        'Ludovico Einaudy': 'Italian pianist and composer Ludovico Einaudi (born 1955) is renowned for his contemporary classical music, which incorporates elements of minimalism, ambient, and pop music. His compositions are known for their emotional depth and simplicity.',
                        'Herbie Hancock' : 'American musician Herbie Hancock (born 1940) is a legendary figure in jazz, particularly known for his contributions to jazz fusion. His work incorporates elements of funk, soul, and electronic music, showcasing his innovative approach to jazz.' ,
                        'Hillsong Worship': 'Hillsong Worship, from Australia (formed 1983), is synonymous with contemporary Christian music. Their style combines Christian worship with contemporary music elements, influencing the genre globally with their modern worship anthems.' ,
                        'Joe Hisaishi' : 'Japanese composer Joe Hisaishi (born 1950), is celebrated for his film scores, particularly for Studio Ghibli. His style, while primarily contemporary, seamlessly blends orchestral and minimalist elements, creating emotionally resonant soundtracks.' ,
                        'Ryuichy Sakamoto': 'Ryuichi Sakamoto (born 1952), initially part of Yellow Magic Orchestra, has a diverse musical style encompassing electronic, experimental, and classical music. His innovative compositions often feature a mix of traditional instruments and electronic sounds.',
                        'Yiruma': 'South Korean pianist Yiruma (born 1978) is known for his contemporary classical music that often crosses into the pop genre. His compositions, typically for solo piano, are characterized by their emotive melodies and accessible style.'
}

composer_genre_dict = { 'Bethel Music': 'Religious',
                        'Richard Clayderman' : 'New Age/Pop-Classical',
                        'Ludovico Einaudy': 'Contemporary Classical',
                        'Herbie Hancock' : 'Jazz' ,
                        'Hillsong Worship': 'Contemporary Christian' ,
                        'Joe Hisaishi' : 'Film Music/Contemporary' ,
                        'Ryuichy Sakamoto': 'Electronic/Experimental',
                        'Yiruma': 'Contemporary Classical/Pop'}

composer_image_dict = {'Bethel Music': 'resources/composer_images/bethel_church.png',
                        'Richard Clayderman' : 'resources/composer_images/clayderman.png',
                        'Ludovico Einaudy': 'resources/composer_images/einaudi.png',
                        'Herbie Hancock' : 'resources/composer_images/hearbie_hancock.png' ,
                        'Hillsong Worship': 'resources/composer_images/hillsong_worship.png' ,
                        'Joe Hisaishi' : 'resources/composer_images/joe_hisaishi.png' ,
                        'Ryuichy Sakamoto': 'resources/composer_images/ryuichi_sakamoto.png',
                        'Yiruma': 'resources/composer_images/yiruma.png'}

example_prediction = {  'Bethel Music': 0.8,
                        'Richard Clayderman' : 0.1,
                        'Ludovico Einaudy': 0.1}

#if input_file is not None:
if True:
    #with st.spinner('Processing the mp3 file...'):
        #import requests
        #url = "https://music-fbzdapc47q-ew.a.run.app" # change for API URL
        #files = {'file': input_file}
        #response = requests.post(url,files=files).json()

        #making layout of the prediction
        response = example_prediction
        top_composer = max(response.items(), key=lambda x: x[1])[0]

        #artist title
        st.markdown(f"<h1 style='text-align: center'>{top_composer} - {composer_genre_dict[top_composer]}</h1>", unsafe_allow_html=True)
        #artist image
        composer_image = composer_image_dict[top_composer]
        st.image(composer_image, use_column_width=True)
        #artist info text
        st.markdown(f"<div style='text-align: justify'>{composer_info_dict[top_composer]}</div>", unsafe_allow_html=True)


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
