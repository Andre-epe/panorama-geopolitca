import streamlit as st

# CSS personalizado para o botão de feedback e dark mode
st.markdown(
    f"""
    <style>
        /* Aplica o mesmo estilo para DOIS botões com chaves diferentes */
        div.st-key-meu_botao_feedback, div.st-key-botao_dark_mode1 {{
            display: flex;
        }}

        div.st-key-meu_botao_feedback button, 
        div.st-key-botao_dark_mode1 button {{
            background-color: transparent !important;
            color: #0C2340 !important;
            border: 1px solid #0C2340 !important;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            width: 100%;
            height: 100%;
            padding: 0 !important;
            font-family: "Source Sans Pro", sans-serif !important;
            transition: all 0.3s ease;
        }}

        /* EFEITO HOVER */
        div.st-key-meu_botao_feedback button:hover, 
        div.st-key-botao_dark_mode1 button:hover {{
            background-color: #0C2340 !important;
            color: white !important;
            cursor: pointer;
        }}

        div.st-key-meu_botao_feedback button p, 
        div.st-key-botao_dark_mode1 button p {{
            font-size: 12px !important;
            font-weight: bold !important;
            line-height: 1.1 !important;
            margin: 0 !important;
            padding: 0 !important;
            width: 100%;
            text-align: center !important;
            font-family: "Source Sans Pro", sans-serif !important;
        }}

        div.st-key-meu_botao_feedback button span, 
        div.st-key-botao_dark_mode1 button span {{
            flex-grow: 1;
            text-align: center;
            display: block;
            font-family: "Source Sans Pro", sans-serif !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)


if not 'chave_botao_feedback' in st.session_state:
    st.session_state['chave_botao_feedback'] = 'meu_botao_feedback'

if st.button('💭Forneça um feedback!', key=st.session_state['chave_botao_feedback']):
    feedback_mensagem()