import streamlit as st
import base64
# Função para converter imagem PNG para Base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Converte a imagem
img_base64 = image_to_base64("africa.png")

# Cria o HTML da imagem
img_html = f'<img src="data:image/png;base64,{img_base64}" width="30"/>'

# Exibe como Markdown para simular um "emoji"
st.markdown(f"{img_html} **Selecione uma Região**", unsafe_allow_html=True)