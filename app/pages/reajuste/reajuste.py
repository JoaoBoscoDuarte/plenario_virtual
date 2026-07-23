"""Página: Reajuste de Voto."""

import sys
from pathlib import Path

import streamlit as st

_here = Path(__file__).resolve()
_root = _here.parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from dados.loader import load_tramitacoes
from pages.reajuste.layout import render_graficos

try:
    df = load_tramitacoes()
except Exception as e:
    st.error(f"Erro ao carregar dataset de reajuste de voto: {e}")
    st.stop()

if df.empty:
    st.warning("O dataframe retornou vazio.")
    st.stop()

# ── Cabeçalho ─────────────────────────────────────────────────────────────────
st.title("Reajuste de Voto")
st.markdown("""
Esta seção analisa as **inclusões em pauta de Controle Concentrado** (ADI, ADC, ADO e ADPF)
no STF entre **2020 e 2025** sob a ótica do **reajuste de voto** — situação em que um ministro
altera sua posição após o início do julgamento.

A unidade de análise é a **inclusão em pauta**: cada linha representa uma inclusão, e a coluna
`teve_reajuste` indica se aquela inclusão registrou ao menos um andamento de reajuste de voto.

Os gráficos cobrem três dimensões:

- **Proporção** — percentual de inclusões com e sem reajuste no período total (PV e PP).
- **Evolução anual** — volume de reajustes por ano (PV e PP).
- **Por classe** — distribuição dos reajustes por classe processual e ano (PV e PP).
""")

st.markdown("---")

render_graficos(df)
