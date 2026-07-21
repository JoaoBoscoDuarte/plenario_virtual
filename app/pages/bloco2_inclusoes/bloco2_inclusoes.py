"""Página: Bloco 2 — Narrativa Estendida das Inclusões em Pauta (2016–2025)."""

import sys
from pathlib import Path

import streamlit as st

_here = Path(__file__).resolve()
_root = _here.parent.parent.parent  # /app
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from dados.loader import load_inclusoes_em_pauta
from pages.bloco2_inclusoes.layout import render_graficos

try:
    df = load_inclusoes_em_pauta()
except Exception as e:
    st.error(f"Erro ao carregar dataset de inclusões em pauta: {e}")
    st.stop()

st.title("Bloco 2 — Narrativa Estendida das Inclusões em Pauta")
st.markdown("""
Vinte gráficos que estendem a análise das inclusões em pauta à série completa **2016–2025**,
cobrindo o período pré-ESPIN (2016–2019) e o período de universalização do Plenário Virtual (2020–2025):
participação, composição por classe e tipo de questão, tramitação, desfecho e produtividade por ambiente.
""")
st.markdown("---")
render_graficos(df)
