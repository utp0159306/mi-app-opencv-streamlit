import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("Dibuja figuras sobre una imagen usando Streamlit")

# Carga la imagen
uploaded_file = st.file_uploader("Carga una imagen", type=["jpg", "png", "jpeg"])
if uploaded_file is None:
    st.warning("Por favor, sube una imagen para comenzar.")
    st.stop()

file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Copia para dibujar
img_draw = img.copy()

# Selección de figura
figura = st.selectbox("Selecciona la figura a dibujar", ("Círculo", "Rectángulo", "Línea", "Logo OpenCV"))

# Parámetros para dibujo
if figura == "Círculo":
    cx = st.number_input("Centro X", min_value=0, max_value=img.shape[1], value=img.shape[1]//2)
    cy = st.number_input("Centro Y", min_value=0, max_value=img.shape[0], value=img.shape[0]//2)
    radio = st.slider("Radio", 1, min(img.shape[0], img.shape[1])//2, 50)
    color = (255, 0, 0)  # Azul en RGB
    cv2.circle(img_draw, (cx, cy), radio, color, thickness=3)
elif figura == "Rectángulo":
    x1 = st.number_input("X1", min_value=0, max_value=img.shape[1], value=img.shape[1]//4)
    y1 = st.number_input("Y1", min_value=0, max_value=img.shape[0], value=img.shape[0]//4)
    x2 = st.number_input("X2", min_value=0, max_value=img.shape[1], value=3*img.shape[1]//4)
    y2 = st.number_input("Y2", min_value=0, max_value=img.shape[0], value=3*img.shape[0]//4)
    color = (0, 255, 0)  # Verde en RGB
    cv2.rectangle(img_draw, (x1, y1), (x2, y2), color, thickness=3)
elif figura == "Línea":
    x1 = st.number_input("X inicio", min_value=0, max_value=img.shape[1], value=0)
    y1 = st.number_input("Y inicio", min_value=0, max_value=img.shape[0], value=0)
    x2 = st.number_input("X fin", min_value=0, max_value=img.shape[1], value=img.shape[1])
    y2 = st.number_input("Y fin", min_value=0, max_value=img.shape[0], value=img.shape[0])
    color = (255, 255, 0)  # Cyan en RGB
    cv2.line(img_draw, (x1, y1), (x2, y2), color, thickness=3)
elif figura == "Logo OpenCV":
    # Dibuja logo OpenCV en esquina superior izquierda
    # Logo simplificado: tres círculos en línea
    radios = [30, 25, 20]
    posiciones = [(50, 50), (110, 50), (160, 50)]
    colores = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # RGB
    
    for r, pos, col in zip(radios, posiciones, colores):
        cv2.circle(img_draw, pos, r, col, thickness=-1)

# Mostrar imagen con dibujo
st.image(img_draw, caption="Imagen con figura dibujada", use_column_width=True)
