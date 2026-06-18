# pages/01_visao_geral.py
import streamlit as st
from data.loader import load_parquet
from components.filters import date_filter, multiselect_filter

df = load_parquet("org/meu-dataset", "dados.parquet")

st.header("Visão Geral")

# Filtros
with st.sidebar:
    st.subheader("Filtros")
    df = multiselect_filter(df, "categoria", "Categoria")

# Layout em colunas
col1, col2, col3 = st.columns(3)
col1.metric("Total", len(df))
col2.metric("Média", df["valor"].mean().round(2))
col3.metric("Máximo", df["valor"].max())