"""Funções de construção de figuras Plotly para a página de Acervo."""

from __future__ import annotations
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

_LABELS = {"ano": "Ano", "quantidade_ativos": "Processos Ativos", "classe": "Classe"}

_BASE_LAYOUT = dict(
    template="plotly_white",
    height=480,
    margin=dict(l=20, r=20, t=30, b=60),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

_XAXIS_YEAR = dict(dtick=1, tickangle=-45)
_YAXIS_YEAR = dict(dtick=1)


def _apply_text_per_trace(fig: go.Figure, df: pd.DataFrame, position: str) -> None:
    for trace in fig.data:
        mask = df["classe"] == trace.name
        vals = df.loc[mask, "quantidade_ativos"].tolist()
        trace.update(text=vals, textposition=position)


def fig_total_por_ano(
    df: pd.DataFrame,
    chart_type: str = "Linhas",
    show_values: bool = False,
) -> go.Figure:
    df_total = df.groupby("ano", as_index=False)["quantidade_ativos"].sum()

    if chart_type == "Barras":
        fig = px.bar(df_total, x="ano", y="quantidade_ativos", labels=_LABELS)
        if show_values:
            fig.update_traces(text=df_total["quantidade_ativos"], textposition="outside")
    else:  # Linhas
        fig = px.line(df_total, x="ano", y="quantidade_ativos", markers=True, labels=_LABELS)
        if show_values:
            fig.update_traces(
                mode="lines+markers+text",
                text=df_total["quantidade_ativos"],
                textposition="top center",
            )

    fig.update_layout(**_BASE_LAYOUT, xaxis=_XAXIS_YEAR)
    return fig


def fig_evolucao_acervo(
    df: pd.DataFrame,
    chart_type: str = "Linhas",
    show_values: bool = False,
) -> go.Figure:
    if chart_type == "Barras":
        fig = px.bar(
            df, x="ano", y="quantidade_ativos", color="classe",
            barmode="group", labels=_LABELS,
        )
        if show_values:
            _apply_text_per_trace(fig, df, "outside")
        fig.update_layout(**_BASE_LAYOUT, xaxis=_XAXIS_YEAR)

    elif chart_type == "Barras Empilhadas":
        fig = px.bar(
            df, x="ano", y="quantidade_ativos", color="classe",
            barmode="stack", labels=_LABELS,
        )
        if show_values:
            _apply_text_per_trace(fig, df, "inside")
        fig.update_layout(**_BASE_LAYOUT, xaxis=_XAXIS_YEAR)

    else:  # Linhas
        fig = px.line(
            df, x="ano", y="quantidade_ativos", color="classe",
            markers=True, labels=_LABELS,
        )
        if show_values:
            for trace in fig.data:
                mask = df["classe"] == trace.name
                vals = df.loc[mask, "quantidade_ativos"].tolist()
                trace.update(mode="lines+markers+text", text=vals, textposition="top center")
        fig.update_layout(**_BASE_LAYOUT, xaxis=_XAXIS_YEAR)

    return fig


def fig_composicao_proporcional(
    df: pd.DataFrame,
    show_values: bool = False,
) -> go.Figure:
    fig = px.bar(
        df, x="ano", y="quantidade_ativos", color="classe",
        barmode="stack", labels=_LABELS,
    )
    if show_values:
        _apply_text_per_trace(fig, df, "inside")
    fig.update_layout(**_BASE_LAYOUT, xaxis=_XAXIS_YEAR)
    return fig
