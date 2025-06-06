import streamlit as st

# CSS para aplicar APENAS nas colunas específicas
st.markdown(
    """
    <style>
    /* Criamos um identificador exclusivo para nossas colunas */
    .custom-columns {
        display: flex;
    }

    /* Apenas as colunas dentro do nosso container terão a altura fixa */
    .custom-columns > div {
        display: flex;
        flex-direction: column;
    }

    /* Definimos uma altura fixa para os elementos dentro das colunas */
    .custom-box {
        height: 100px; /* Altura fixa em pixels (ajuste conforme necessário) */
        display: flex;
        flex-direction: column;
        justify-content: center; /* Centraliza o conteúdo verticalmente */
        align-items: center;
        width: 100%;
        background-color: #f0f0f0; /* Apenas para visualização */
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Criando um container exclusivo para aplicar o CSS
with st.container():
    st.markdown('<div class="custom-columns">', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium", border=True)

    with col1:
        st.markdown('<div class="custom-box">', unsafe_allow_html=True)
        st.header("Título 1")
        st.write("Este é um conteúdo dentro da coluna 1.")
        st.write("Este é um conteúdo dentro da coluna 1.")
        st.write("Este é um conteúdo dentro da coluna 1.")
        st.write("Este é um conteúdo dentro da coluna 1.")
        st.button("Botão 1")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-box">', unsafe_allow_html=True)
        st.header("Título 2")
        st.write("Conteúdo curto na coluna 2.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
