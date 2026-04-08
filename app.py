import streamlit as st

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
    st.markdown("""
        <style>
        .main .block-container { padding: 0 !important; max-width: 100% !important; }
        iframe#site { width: 100%; height: calc(100vh - 56px); border: none; display: block; }
        </style>
        <iframe id="site" src="/app/static/index.html" scrolling="yes"></iframe>
    """, unsafe_allow_html=True)
