"""Página: Bloco 1 — Narrativa do Acervo (1988–2025)."""

import sys
from pathlib import Path

import streamlit as st

_here = Path(__file__).resolve()
_root = _here.parent.parent.parent  # /app
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from dados.loader import load_evolucao_acervo
from pages.bloco1_acervo.layout import render_graficos

try:
    df = load_evolucao_acervo()
except Exception as e:
    st.error(f"Erro ao conectar com o Data Lake do Hugging Face: {e}")
    st.stop()

st.title("Bloco 1 — Narrativa do Acervo")
st.markdown("""
Quatro gráficos que contam a história do **acervo de Controle Concentrado** do STF entre 1988 e 2025:
sua variação por triênio, sua composição por classe, o equilíbrio entre distribuições e baixas,
e a variação anual — com os marcos das Emendas Regimentais 51/52/53 e o período da ESPIN.
""")
st.markdown("---")
render_graficos(df)
