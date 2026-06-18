# pages/01_visao_geral.py
# Garante que "data" e "bootstrap" sejam importáveis no Streamlit Cloud
import sys
from pathlib import Path
_here = Path(__file__).resolve()
_root = _here.parent.parent if _here.parent.name == "pages" else _here.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import bootstrap
import streamlit as st
from data.loader import load_parquet
from components.filters import date_filter, multiselect_filter

# Usa o repositório real do projeto + caminho correto no HF
# (os arquivos estão em processed/ no repositório)
df = load_parquet("JoaoBoscoooo/plenario_virtual", "processed/arquivosConcatenados.parquet")

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