"""Página de Decisões — virtual/presencial, unanimidade e tipo de órgão."""

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Bootstrap for pages (Cloud multipage + local): add root for 'src' top-level imports.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

__package__ = "app.pages"

from ..data_loader import load_decisoes
from src import filters as flt

st.title("⚖️ Decisões")

with st.spinner("Carregando decisões..."):
    df = load_decisoes()

# Filtros rápidos (defensivo com coerção)
if "dec_data" in df.columns:
    date_series = pd.to_datetime(df["dec_data"], errors="coerce")
    valid = date_series.dropna()
    if len(valid) > 0:
        dmin, dmax = valid.min().date(), valid.max().date()
        dr = st.date_input("Período das decisões", value=(dmin, dmax))
        if isinstance(dr, (list, tuple)) and len(dr) == 2:
            df = flt.filter_by_date_range(df, "dec_data", dr[0], dr[1])
    # caso contrário, não aplica filtro de período (evita crash em dados ruins)

col1, col2 = st.columns(2)
with col1:
    virtual = st.checkbox("Apenas decisões com menção a virtual", value=False)
    if virtual and "dec_virtual" in df.columns:
        df = df[df["dec_virtual"] == True]
with col2:
    unanime = st.checkbox("Apenas unânimes", value=False)
    if unanime and "dec_unanime" in df.columns:
        df = df[df["dec_unanime"] == True]

# Métricas
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total decisões", f"{len(df):,}")
if "dec_virtual" in df.columns:
    c2.metric("Com marca virtual", f"{df['dec_virtual'].sum():,}")

if "dec_unanime" in df.columns:
    c3.metric("Unânimes", f"{df['dec_unanime'].sum():,}")

if "dec_maioria" in df.columns:
    c4.metric("Por maioria", f"{df['dec_maioria'].sum():,}")

# Breakdown por tipo de órgão
st.subheader("Decisões por tipo de órgão julgador")
if "dec_tipo_orgao" in df.columns:
    org = df["dec_tipo_orgao"].value_counts(dropna=False).reset_index()
    org.columns = ["tipo_orgao", "quantidade"]
    
    fig = px.bar(org, x="tipo_orgao", y="quantidade", title="Tipo de órgão (pleno / turma / monocrática)")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Amostra")
show_cols = [c for c in ["incidente", "classe", "dec_data", "dec_nome", "dec_virtual", "dec_unanime", "dec_tipo_orgao"] if c in df.columns]
st.dataframe(df[show_cols].head(20), use_container_width=True, hide_index=True)
