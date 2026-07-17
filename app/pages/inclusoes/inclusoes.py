"""Página: Inclusões em Pauta."""

import sys
from pathlib import Path

import streamlit as st

_here = Path(__file__).resolve()
_root = _here.parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from pathlib import Path
import pandas as pd
from dados.loader import load_inclusoes_em_pauta
from pages.inclusoes.layout import render_graficos

_here = Path(__file__).resolve()
_root = _here.parent.parent.parent
_data = _root / "data" / "processed"

try:
    df = load_inclusoes_em_pauta()
except Exception as e:
    st.error(f"Erro ao carregar dataset de inclusões em pauta: {e}")
    st.stop()

if df.empty:
    st.warning("O dataframe retornou vazio.")
    st.stop()

try:
    df_dec = pd.read_parquet(_data / "dim_decisoes.parquet")
except Exception as e:
    st.warning(f"Não foi possível carregar decisões para refinamento: {e}")
    df_dec = pd.DataFrame()

# ── Cabeçalho ─────────────────────────────────────────────────────────────────
st.title("Inclusões em Pauta")
st.markdown("""
Esta seção analisa as **inclusões em pauta de Controle Concentrado** (ADI, ADC, ADO e ADPF)
no STF entre **2020 e 2025**, comparando o **Plenário Virtual** e o **Plenário Presencial**.

A unidade de análise é a **inclusão em pauta** — cada vez que um processo é colocado em pauta
para julgamento, independentemente de ter sido julgado antes. Um mesmo processo pode aparecer
múltiplas vezes se foi incluído em sessões distintas.

Os gráficos cobrem quatro dimensões de análise:

- **Volume** — quantas inclusões ocorreram por ano, por ambiente e por classe processual.
- **Desfecho macro** — se a inclusão resultou em julgamento concluído ou não concluído.
- **Categoria de desfecho concluído** — se a decisão foi unânime, por maioria com o relator
  ou por maioria com o relator vencido.
- **Categoria de não conclusão** — pedido de vista, destaque, retirado de pauta ou motivos diversos.
""")

st.markdown("---")

# ── Renderização ──────────────────────────────────────────────────────────────
render_graficos(df, df_dec)
