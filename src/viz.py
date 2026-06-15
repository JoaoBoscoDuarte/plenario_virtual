"""Funções de visualização reutilizáveis (principalmente Plotly).

Centraliza criação de figuras para manter as páginas do Streamlit limpas
e permitir reuso em notebooks de análise.
"""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def bar_volume_by_month(df: pd.DataFrame, date_col: str, color_col: str | None = None, title: str = "") -> go.Figure:
    """Barra empilhada ou simples de volume mensal (usa Period M).
    
    É defensivo: faz coerção para datetime porque dados carregados de parquets
    (especialmente versões antigas ou vindos do HF) podem vir com dtype object.
    """

    if df.empty or date_col not in df.columns:
        return go.Figure()
    
    work = df.copy()
    # Coerção segura — essencial para evitar "Can only use .dt accessor with datetimelike values"
    work[date_col] = pd.to_datetime(work[date_col], errors="coerce")
    work = work.dropna(subset=[date_col])
    
    if work.empty:
        return go.Figure()
    
    work["mes"] = work[date_col].dt.to_period("M").astype(str)
    grp = ["mes"]

    if color_col and color_col in work.columns:
        grp.append(color_col)
    agg = work.groupby(grp).size().reset_index(name="quantidade")
    fig = px.bar(
        agg,
        x="mes",
        y="quantidade",
        color=color_col if color_col in agg.columns else None,
        title=title or "Volume por mês",
        barmode="stack" if color_col else "relative",
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def metric_cards(df: pd.DataFrame, total_label: str = "Total", **extra) -> dict:
    """Retorna dict simples de métricas para st.metric (pode ser extendido)."""
    out = {total_label: len(df)}
    
    for k, v in extra.items():
        out[k] = v
    return out
