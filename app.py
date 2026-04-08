import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(layout="wide", page_title="Pontos Cedidos e Conquistados")

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
    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    # Injeta base href para que URLs relativas (./assets/...) resolvam via
    # o servidor estático do Streamlit (/app/static/assets/...)
    html = html.replace("<head>", '<head>\n<base href="/app/static/">', 1)
    components.html(html, height=1200, scrolling=True)
