import streamlit as st
import streamlit.components.v1 as components
import os
import json
import re

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
    base_dir = os.path.dirname(__file__)
    cache_path = os.path.join(base_dir, "cartola_mercado.json")
    cache_info = {}
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as cache_file:
                cache_info = json.load(cache_file)
        except Exception:
            cache_info = {}

    col_status, col_update = st.columns([4, 1])
    with col_status:
        rodada_cache = cache_info.get("round", "não identificada")
        atualizado_em = cache_info.get("fetched_at", "cache anterior")
        st.caption(f"API oficial do Cartola: rodada {rodada_cache} · consulta {atualizado_em} · status 7 provável / 2 dúvida")
    with col_update:
        atualizar = st.button("Atualizar mercado Cartola", use_container_width=True)

    if atualizar:
        try:
            with st.spinner("Atualizando prováveis e dúvidas na API oficial do Cartola..."):
                from atualizar_cartola import atualizar as atualizar_lista
                dados_mercado = atualizar_lista()
                # Faz um patch cirurgico apenas do bloco CARTOLA_MERCADO dentro do
                # static/index.html ja publicado, em vez de rodar gerar_site.py
                # inteiro no servidor. gerar_site.py depende de uma pasta irma
                # ("COMPARATIVOS JOGADORES") que so existe na maquina local do
                # autor — no servidor publicado ela nao existe, e uma regeneracao
                # completa aqui apagaria o banco de fotos dos jogadores ja embutido.
                html_path_patch = os.path.join(base_dir, "static", "index.html")
                with open(html_path_patch, "r", encoding="utf-8") as f_html:
                    html_patch = f_html.read()
                novo_bloco = "var CARTOLA_MERCADO = " + json.dumps(dados_mercado, ensure_ascii=False) + ";"
                html_patch, n_subs = re.subn(
                    r"var CARTOLA_MERCADO = \{.*?\};",
                    lambda _m: novo_bloco,
                    html_patch,
                    count=1,
                    flags=re.DOTALL,
                )
                if n_subs != 1:
                    raise RuntimeError("Bloco CARTOLA_MERCADO nao encontrado em static/index.html")
                with open(html_path_patch, "w", encoding="utf-8") as f_html:
                    f_html.write(html_patch)
            st.success("Mercado oficial do Cartola atualizado.")
            st.rerun()
        except Exception as exc:
            st.error(f"Não foi possível atualizar a API do Cartola: {exc}")

    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    # Injeta base href para que URLs relativas (./assets/...) resolvam via
    # o servidor estático do Streamlit (/app/static/assets/...)
    html = html.replace("<head>", '<head>\n<base href="/app/static/">', 1)
    components.html(html, height=1200, scrolling=True)
