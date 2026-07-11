"""Página: Inclusões em Pauta."""

import sys
from pathlib import Path

import streamlit as st

_here = Path(__file__).resolve()
_root = _here.parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from data.loader import load_inclusoes_em_pauta
from pages.inclusoes.layout import render_graficos

try:
    df = load_inclusoes_em_pauta()
except Exception as e:
    st.error(f"Erro ao carregar dataset de inclusões em pauta: {e}")
    st.stop()

if df.empty:
    st.warning("O dataframe retornou vazio.")
    st.stop()

st.title("Inclusões em Pauta")
st.markdown(
    "Análise das inclusões em pauta de **Controle Concentrado** (ADI, ADC, ADO, ADPF) "
    "no STF entre 2020 e 2025, comparando o **Plenário Virtual** e o **Plenário Físico** "
    "e detalhando os desfechos (concluído / não concluído) por classe e por ano."
)

render_graficos(df)
