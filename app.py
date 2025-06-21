import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("Dibuja figuras sobre una imagen usando Streamlit")

# Carga la imagen base
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

# Selector de color con nombre y su valor RGB
color_names = ['Rojo', 'Verde', 'Azul', 'Amarillo', 'Cian', 'Magenta', 'Negro', 'Blanco']
color_values = {
    'Rojo': (255, 0, 0),
    'Verde': (0, 255, 0),
    'Azul': (0, 0, 255),
    'Amarillo': (255, 255, 0),
    'Cian': (0, 255, 255),
    'Magenta': (255, 0, 255),
    'Negro': (0, 0, 0),
    'Blanco': (255, 255, 255)
}
color_name = st.selectbox("Selecciona el color", color_names)
color = color_values[color_name]

# Slider grosor línea
grosor = st.slider("Grosor de línea", 1, 20, 3)

if figura == "Círculo":
    cx = st.slider("Centro X", 0, img.shape[1], img.shape[1] // 2)
    cy = st.slider("Centro Y", 0, img.shape[0], img.shape[0] // 2)
    radio = st.slider("Radio", 1, min(img.shape[0], img.shape[1]) // 2, 50)
    cv2.circle(img_draw, (cx, cy), radio, color, thickness=grosor)

elif figura == "Rectángulo":
    x1 = st.slider("X1", 0, img.shape[1], img.shape[1] // 4)
    y1 = st.slider("Y1", 0, img.shape[0], img.shape[0] // 4)
    x2 = st.slider("X2", 0, img.shape[1], 3 * img.shape[1] // 4)
    y2 = st.slider("Y2", 0, img.shape[0], 3 * img.shape[0] // 4)
    cv2.rectangle(img_draw, (x1, y1), (x2, y2), color, thickness=grosor)

elif figura == "Línea":
    x1 = st.slider("X inicio", 0, img.shape[1], 0)
    y1 = st.slider("Y inicio", 0, img.shape[0], 0)
    x2 = st.slider("X fin", 0, img.shape[1], img.shape[1])
    y2 = st.slider("Y fin", 0, img.shape[0], img.shape[0])
    cv2.line(img_draw, (x1, y1), (x2, y2), color, thickness=grosor)

elif figura == "Logo OpenCV":
    logo_file = st.file_uploader("Carga el logo OpenCV (PNG con fondo transparente recomendado)", type=["png", "jpg", "jpeg"])
    if logo_file is not None:
        logo = Image.open(logo_file).convert("RGBA")
        logo_np = np.array(logo)

        max_width = img.shape[1]
        max_height = img.shape[0]
        logo_width = st.slider("Ancho del logo", 10, max_width, min(logo.width, max_width))
        logo_height = st.slider("Alto del logo", 10, max_height, min(logo.height, max_height))
        pos_x = st.slider("Posición X (izquierda)", 0, max_width - logo_width, 0)
        pos_y = st.slider("Posición Y (arriba)", 0, max_height - logo_height, 0)

        logo_resized = cv2.resize(logo_np, (logo_width, logo_height), interpolation=cv2.INTER_AREA)

        b, g, r, a = cv2.split(logo_resized)
        overlay_color = cv2.merge((b, g, r))
        roi = img_draw[pos_y:pos_y + logo_height, pos_x:pos_x + logo_width]

        mask = a / 255.0
        inv_mask = 1.0 - mask

        for c in range(3):
            roi[:, :, c] = (mask * overlay_color[:, :, c] + inv_mask * roi[:, :, c])

        img_draw[pos_y:pos_y + logo_height, pos_x:pos_x + logo_width] = roi
    else:
        st.info("Por favor, carga una imagen para el logo.")

st.image(img_draw, caption="Imagen con figura dibujada", use_column_width=True)
