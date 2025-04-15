import streamlit as st

# Mapeamento dos continentes para emojis e imagens
option_map = {
    "🌏 Ásia": "asia.png",
    "🌍 Europa": "europe.png",
    "🌍 África": "africa.png",
    "🌎 América do Sul": "south_america.png",
    "🌎 América do Norte e Central": "north_central_america.png",
    "🌏 Oceania": "oceania.png",
    "❄️ Antártica": "antarctica.png",
}

# Criar o controle segmentado
selection = st.segmented_control(
    "Escolha um continente:",
    options=list(option_map.keys()),
    selection_mode="single",
)

# Mostrar imagem correspondente à seleção
if selection:
    st.image(option_map[selection], caption=selection, width=150)