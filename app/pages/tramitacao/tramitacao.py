"""Página: Tramitação por Ambiente."""

import sys
from pathlib import Path

import streamlit as st

_here = Path(__file__).resolve()
_root = _here.parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from data.loader import load_inclusoes_com_pauta
from pages.tramitacao.layout import render_graficos

try:
    df = load_inclusoes_com_pauta()
except Exception as e:
    st.error(f"Erro ao carregar dataset: {e}")
    st.stop()

if df.empty:
    st.warning("O dataframe retornou vazio.")
    st.stop()

st.title("Tramitação por Ambiente")
st.markdown("""
Esta seção analisa em quais **ambientes de julgamento** os processos de Controle Concentrado
(ADI, ADC, ADO e ADPF) tramitaram entre **2020 e 2025**.

A unidade de análise aqui é o **processo** (incidente único) — diferente das demais páginas,
que contam inclusões em pauta. Um processo pode ter sido incluído múltiplas vezes, mas é
contado uma única vez para determinar se tramitou só no Plenário Virtual, só no Plenário
Físico, ou em ambos os ambientes.
""")

st.markdown("---")

render_graficos(df)
