"""Página: Bloco 3 — Persistência Pós-Pandêmica."""

import sys
from pathlib import Path

import streamlit as st

_here = Path(__file__).resolve()
_root = _here.parent.parent.parent  # /app
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from dados.loader import load_inclusoes_em_pauta
from pages.bloco3_pandemia.layout import render_graficos

try:
    df = load_inclusoes_em_pauta()
except Exception as e:
    st.error(f"Erro ao carregar dataset de inclusões em pauta: {e}")
    st.stop()

st.title("Bloco 3 — Persistência Pós-Pandêmica")
st.markdown("""
Este bloco não introduz gráficos novos: reaproveita **2.a** e **2.m** (Bloco 2) sob uma
leitura específica — testar se o fim da emergência sanitária (ESPIN, abril de 2022) produziu
alguma inflexão na participação ou no desfecho do Plenário Virtual. Não produz.
""")
st.markdown("---")
render_graficos(df)
