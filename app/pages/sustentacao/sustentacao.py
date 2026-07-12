"""Página: Sustentação Oral."""

import sys
from pathlib import Path

import streamlit as st

_here = Path(__file__).resolve()
_root = _here.parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from data.loader import load_inclusoes_em_pauta
from pages.sustentacao.layout import render_graficos

try:
    df = load_inclusoes_em_pauta()
except Exception as e:
    st.error(f"Erro ao carregar dataset: {e}")
    st.stop()

if df.empty:
    st.warning("O dataframe retornou vazio.")
    st.stop()

st.title("Sustentação Oral")
st.markdown("""
Esta seção analisa a ocorrência de **sustentação oral** nas inclusões em pauta de
Controle Concentrado (ADI, ADC, ADO e ADPF) no STF entre **2020 e 2025**.

A unidade de análise é a **inclusão em pauta** — cada vez que um processo foi colocado
em pauta, verificou-se se houve sustentação oral realizada naquela ocasião.

A detecção considera andamentos com nome `Sustentação Oral` ou com menção ao padrão
no complemento do andamento (necessário para capturar o Plenário Físico, onde o registro
é menos padronizado). Sustentações indeferidas ou não realizadas são excluídas.
""")

st.markdown("---")

render_graficos(df)
