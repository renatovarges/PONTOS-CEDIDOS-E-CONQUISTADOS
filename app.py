import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Pontos Cedidos e Conquistados")

# Senha (PIN)
PIN_CORRETO = "1979"

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.markdown("<h1 style='text-align: center; color: #ceab42;'>Acesso Restrito</h1>", unsafe_allow_html=True)
    pin_digitado = st.text_input("Digite o PIN para acessar", type="password")
    
    if st.button("Entrar"):
        if pin_digitado == PIN_CORRETO:
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("PIN Incorreto.")
else:
    components.iframe("/app/static/index.html", height=1200, scrolling=True)
