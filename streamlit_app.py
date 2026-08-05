import streamlit as st


pg = st.navigation([
    st.Page("my_page.py", title="Página 1"),
    st.Page("page_1.py", title="Página 2"),
])

pg.run()