import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("Demo de OpenCV con Streamlit")

# Subir imagen
uploaded_file = st.file_uploader("Carga una imagen", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Leer imagen con OpenCV
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convertir BGR a RGB para mostrar en Streamlit
    
    st.image(img, caption='Imagen cargada', use_column_width=True)
    
    # Operación sencilla de OpenCV: conversión a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    st.image(gray, caption='Imagen en escala de grises', use_column_width=True, channels="GRAY")
    
    # Evento simulado: umbralización controlada por slider
    threshold = st.slider('Valor de umbral', 0, 255, 127)
    _, thresh_img = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    st.image(thresh_img, caption='Imagen umbralizada', use_column_width=True, channels="GRAY")
