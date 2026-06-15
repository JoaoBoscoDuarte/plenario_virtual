"""Página de Deslocamentos — contagens e datas de tramitação."""

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Bootstrap for pages (Cloud multipage + local): add root for 'src' top-level imports.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

__package__ = "app.pages"

from ..data_loader import load_deslocamentos

st.title("🚚 Deslocamentos / Tramitação")

with st.spinner("Carregando deslocamentos..."):
    df = load_deslocamentos()

st.metric("Total de registros de deslocamento", f"{len(df):,}")

# Prefer columns explicitly created as datetime in the pipeline (sufixo _dt).
# The loose "data" filter was picking string columns like "desl_data_recebido".
date_cols = [c for c in df.columns if c.endswith("_dt")]

if date_cols:
    st.subheader("Distribuição mensal por coluna de data derivada")
    chosen = st.selectbox("Coluna de data", date_cols, index=0)
    
    if chosen:
        # Sempre converte de forma segura — parquets antigos ou de diferentes
        # versões do pipeline podem trazer a coluna como object/string.
        work = df.copy()
        work[chosen] = pd.to_datetime(work[chosen], errors="coerce")
        work = work.dropna(subset=[chosen])
        
        if len(work) == 0:
            st.info(f"Nenhuma data válida encontrada na coluna '{chosen}' após conversão.")
        else:
            work["mes"] = work[chosen].dt.to_period("M").astype(str)
            agg = work.groupby("mes").size().reset_index(name="qtd")
            fig = px.line(
                agg, 
                x="mes", 
                y="qtd", 
                markers=True, 
                title=f"Deslocamentos por mês ({chosen})"
            )
            st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Nenhuma coluna de data derivada (_dt) encontrada neste dataset. "
            "Tente regenerar os parquets com `python -m src.cleaning`.")

st.subheader("Amostra dos deslocamentos")
sample_cols = [c for c in ["incidente", "classe", "desl_data_recebido", "desl_data_recebido_dt", "desl_enviado", "desl_enviado_dt"] if c in df.columns]
st.dataframe(df[sample_cols].head(15), use_container_width=True, hide_index=True)

st.caption("Nota: os deslocamentos capturam movimentações físicas/eletrônicas entre unidades do tribunal.")
