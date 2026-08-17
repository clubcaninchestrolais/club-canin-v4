import streamlit as st

def hide_streamlit_menu():
    css = """
    <style>
    /* Masque uniquement le menu automatique de Streamlit */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
