import streamlit as st

regions = ["América do Sul", "Europa", "Ásia", "África"]
cor_hex = "#0C2242"

# CSS: várias opções de seletor para diferentes versões/DOMs do Streamlit,
# e targeting específico do KaTeX (.katex)
css = f"""
<style>
.katex .katex-html,
.katex .katex-mathml,
.katex .katex-html * {{
    font-size: 15px !important;   /* ajuste fino */
    color: {cor_hex} !important;  /* já aplica cor dinâmica */
}}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

selected_region = st.radio(
    "Escolha uma região:",
    options=regions,
    index=1,
    # use apenas formatação KaTeX sem comandos de tamanho (\tiny, \scriptsize ...)
    format_func=lambda option: fr'$\textit{{{option}}}$'
)

st.write("Selecionado:", selected_region)