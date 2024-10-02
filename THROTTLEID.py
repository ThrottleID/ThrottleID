import os
import keras
from keras.models import load_model
import streamlit as st
import tensorflow as tf
import numpy as np

st.header('ThrottleID')
bike_names = ['KTM duke 390', 'R 15', 'RX 100', 'Splendor']

model = load_model('ThrottleID.keras')

def classify_images(image_path):
    try:
        input_image = tf.keras.utils.load_img(image_path, target_size=(180, 180))
        input_image_array = tf.keras.utils.img_to_array(input_image) / 255.0  # Normalize
        input_image_exp_dim = tf.expand_dims(input_image_array, 0)

        predications = model.predict(input_image_exp_dim)
        result = tf.nn.softmax(predications[0])
        outcome = "The uploaded image is " + bike_names[np.argmax(result)] + " with a score of " + str(np.max(result)*100)
        return outcome
    except Exception as e:
        st.error(f"Error: {e}")
        return None

uploaded_file = st.file_uploader('Upload an Image')
if uploaded_file is not None:
    with open(os.path.join('upload', uploaded_file.name), 'wb') as f:
        f.write(uploaded_file.getbuffer())

    st.image(uploaded_file, width=200)

    result = classify_images(uploaded_file)
    if result is not None:
        st.markdown(result)
    else:
        st.error("An error occurred during classification. Please try again.")