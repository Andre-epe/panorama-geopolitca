import streamlit as st

# CSS personalizado para aumentar o tamanho da fonte do st.pills
st.markdown("""
    <style>
    [data-testid="stPills"] {
        font-size: px;
    }
    </style>
""", unsafe_allow_html=True)

# Seu código st.pills
options = ["Norte", "Leste", "Sul", "Oeste"]
selection = st.pills("Direções", options, selection_mode="multi")
st.markdown(f"Suas opções selecionadas: {selection}.")