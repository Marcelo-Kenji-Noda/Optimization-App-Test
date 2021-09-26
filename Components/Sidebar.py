import streamlit as st

def Sidebar():
    st.sidebar.markdown("## Selecione a página")
    select_page = st.sidebar.radio('Métodos de Aproximação', ["Distância Mínima","Newton","Nada"])
    return select_page