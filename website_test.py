
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
import openai
import matplotlib.pyplot as plt
import requests


# 1.2 Model Tasks
from main_2 import main # UPDATE TO MAIN

# 1.2 Input dictionaries
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
                        'Herbie Hancock' : 'resources/composer_images/herbie_hancock.png' ,
                        'Hillsong Worship': 'resources/composer_images/hillsong_worship.png' ,
                        'Joe Hisaishi' : 'resources/composer_images/joe_hisaishi.png' ,
                        'Ryuichy Sakamoto': 'resources/composer_images/ryuichi_sakamoto.png',
                        'Yiruma': 'resources/composer_images/yiruma.png'}

example_prediction = {  'Bethel Music': 0.8,
                        'Richard Clayderman' : 0.1,
                        'Ludovico Einaudy': 0.1}


# 2. Website

# 2.1 Website Function: typewriter - slow down typing speed
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
  <p>For the audiophiles,<br>the musical nomads,<br>the ones who never heard enough</p>
</div>
""", unsafe_allow_html=True)

if 'mp3_response' not in st.session_state:
    st.session_state['mp3_response'] = None

if 'artist_response' not in st.session_state:
    st.session_state['artist_response'] = None

# 2.3 Load MP3
input_file = st.file_uploader('',type=["mp3"]) # The st.file_uploader function returns a BytesIO object for the uploaded file.

if input_file is not None:
    if st.session_state['mp3_response'] is None:
        with st.spinner('Processing the mp3 file...'):
            url = "https://music-fbzdapc47q-ew.a.run.app" # change for API URL
            files = {'file': input_file}
            response = requests.post(url,files=files).json()
            st.session_state['mp3_response'] = response
    else:
            response = st.session_state['mp3_response']

    # 2.4 Buttons
    col1, col2, col3, col4 = st.columns(4)

    # Button 1: Suggest
    if col1.button('Artist similarity'):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(response.keys(), response.values(), color=['skyblue', 'orange', 'green'])
        ax.set_title('Similarity of artists')
        ax.set_yticks([0.2, 0.6, 0.8])
        ax.set_yticklabels(['low', 'medium', 'high'])
        ax.set_xlabel('Artists')
        ax.set_ylabel('Similarity Score')

        # Show the plot in the sidebar
        st.pyplot(fig)

    # Button 2: Inspire me
    if col2.button('Recomendation for Similar Artits'):
        st.write("Here are some artist recomendations based on the mp3 file that you selected!")
        api_key = st.secrets["openai"]["api_key"]
        client = openai.OpenAI(api_key=api_key)
        top_composer = max(response.items(), key = lambda x: x[1])[0]
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an informative and helpful assistant, skilled in explaining recommendations for composers in music."
                },
                {
                    "role": "user",
                    "content": "We already have a description like this: Bethel Music (Religious): Formed in 2001, Bethel Music emerged from the Bethel Church in Redding, California. [...] Yiruma (Born 1978): South Korean pianist and composer Yiruma (Lee Ru-ma) gained international fame in the early 2000s. His melodic and accessible compositions, often falling into the contemporary classical and pop genres, have made him popular among diverse audiences."
                },
                {
                    "role": "user",
                    "content": f"We have a composer that was predicted by a model which is {top_composer}. We want you to give recommendation similar artists. No description of {top_composer} but rather only the ones that are similar and why. we dont need the a introduction on the {top_composer}. just create the list of 4 similar composers. give me 3 songs for each artist afterwards"
                }
            ]
        )
        st.write(completion.choices[0].message.content)

    # Button 3: Info
    if col3.button('Top Artist Information'):
        top_composer = max(response.items(), key=lambda x: x[1])[0]

        #artist title
        st.markdown(f"<h1 style='text-align: center'>{top_composer} - {composer_genre_dict[top_composer]}</h1>", unsafe_allow_html=True)
        #artist image
        composer_image = composer_image_dict[top_composer]
        st.image(composer_image, use_column_width=True)
        #artist info text
        st.markdown(f"<div style='text-align: justify'>{composer_info_dict[top_composer]}</div>", unsafe_allow_html=True)

    if col4.button('Input another file'):
        st.session_state['mp3_response'] = None
