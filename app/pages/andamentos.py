"""Página de Andamentos — volume, virtual flag e timeline básica."""

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Bootstrap for pages: Streamlit can load pages in separate contexts.
# Must be before any 'app.' or 'src' import.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.data_loader import load_andamentos
from src import filters as flt, viz as vz  # reusable

st.title("📋 Andamentos")

with st.spinner("Carregando andamentos..."):
    df = load_andamentos()

# Filtros locais simples (MVP)
col1, col2 = st.columns(2)
with col1:
    if "and_data" in df.columns:
        # Coerção defensiva + uso de .min()/.max() após garantir datetime
        date_series = pd.to_datetime(df["and_data"], errors="coerce")
        valid = date_series.dropna()
        if len(valid) > 0:
            dmin, dmax = valid.min().date(), valid.max().date()
            dr = st.date_input(
                "Período dos andamentos",
                value=(dmin, dmax),
            )
            if isinstance(dr, (list, tuple)) and len(dr) == 2:
                df = flt.filter_by_date_range(df, "and_data", dr[0], dr[1])
        # se não houver datas válidas, simplesmente não aplica filtro de data local

with col2:
    virtual_only = st.checkbox("Apenas andamentos virtuais", value=False)
    if virtual_only and "and_is_virtual" in df.columns:
        df = df[df["and_is_virtual"] == True]

# Métricas
c1, c2, c3 = st.columns(3)
c1.metric("Total de andamentos", f"{len(df):,}")
if "and_is_virtual" in df.columns:
    virt = int(df["and_is_virtual"].sum())
    c2.metric("Andamentos virtuais", f"{virt:,}")
    c3.metric("% Virtual", f"{(virt / len(df) * 100):.1f}%" if len(df) else "0%")

st.subheader("Volume mensal de andamentos")
fig = vz.bar_volume_by_month(df, "and_data", color_col="and_is_virtual", title="Andamentos por mês (virtual vs não)")
st.plotly_chart(fig, use_container_width=True)

# Amostra
st.subheader("Amostra dos dados")
cols = [c for c in ["incidente", "classe", "and_data", "and_index", "and_nome", "and_is_virtual"] if c in df.columns]
st.dataframe(df[cols].head(25), use_container_width=True, hide_index=True)
