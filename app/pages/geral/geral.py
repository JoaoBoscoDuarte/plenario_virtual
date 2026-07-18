"""Página: Visão Geral."""

import sys
from pathlib import Path

import streamlit as st

_here = Path(__file__).resolve()
_root = _here.parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from dados.loader import load_parquet
from components.filters import render_sidebar_filters
from dados.filters import filter_by_values, filter_by_year_range
from pages.geral.layout import render_metricas, render_timeline, render_tabela_processos

from config import HF_REPO_ID

df = load_parquet(HF_REPO_ID, "processed/arquivosConcatenados.parquet")

st.title("Visão Geral")
st.markdown(
    "Panorama dos processos do **Plenário Virtual** do STF. "
    "Use os filtros no sidebar para recortar por classe, tipo e período."
)

# ── Filtros ───────────────────────────────────────────────────────────────────
filtros = render_sidebar_filters(df)
ai, af = filtros["periodo"]

df_f = df
if filtros["classes"]:
    df_f = filter_by_values(df_f, "classe", filtros["classes"])
if ai and af:
    df_f = filter_by_year_range(df_f, start=ai, end=af)

if df_f.empty and not df.empty:
    st.warning("Nenhum registro após os filtros atuais.")
    df_f = df.head(0)

# ── Métricas ──────────────────────────────────────────────────────────────────
render_metricas(df_f)

st.markdown("---")
render_tabela_processos(df_f)

with st.expander("Colunas disponíveis no dataset", expanded=False):
    st.write(list(df.columns))

st.markdown("---")

# ── Linha do tempo ────────────────────────────────────────────────────────────
render_timeline()
