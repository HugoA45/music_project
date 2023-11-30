import streamlit as st
import numpy as np
from PIL import Image

# List of random image URLs (replace these with your own URLs)
image_urls = [
    "https://images.app.goo.gl/bQfXDKi2d2SPExdv5",
    "https://images.app.goo.gl/MxJFPvrvjjXgUrw57",
    "https://images.app.goo.gl/V6BEqKeLFNf7KwG8A"
    # Add more image URLs as needed
]

# Function to display a random image
def display_random_image():
    random_index = np.random.randint(0, len(image_urls))
    random_image_url = image_urls[random_index]

    # Display the image
    st.image(random_image_url, caption="Random Image", use_column_width=True)

# Streamlit app
def main():
    st.title("Random Image Viewer")

    # Display a random image when the site loads
    display_random_image()

# Run the Streamlit app
if __name__ == "__main__":
    main()
