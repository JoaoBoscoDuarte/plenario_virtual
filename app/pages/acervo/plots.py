"""Funções de construção de figuras Plotly para a página de Acervo."""

from __future__ import annotations
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def fig_evolucao_acervo(
    df: pd.DataFrame,
    use_bar: bool = False,
    show_values: bool = False,
) -> go.Figure:
    """Linha do tempo ou barras do acervo ativo por classe."""
    labels = {
        "ano": "Ano de Referência",
        "quantidade_ativos": "Processos Ativos",
        "classe": "Classe",
    }

    if use_bar:
        fig = px.bar(
            df,
            x="ano",
            y="quantidade_ativos",
            color="classe",
            labels=labels,
            title="Evolução anual do acervo – por classe / Geral",
        )

        if show_values:
            fig.update_traces(
                text=df["quantidade_ativos"],
                textposition="outside",
            )
    else:
        fig = px.line(
            df,
            x="ano",
            y="quantidade_ativos",
            color="classe",
            markers=True,
            labels=labels,
            title="Evolução anual do acervo ativo",
        )

        if show_values:
            fig.update_traces(
                text=df["quantidade_ativos"],
                textposition="top center",
            )

    fig.update_layout(
        template="plotly_white",
        xaxis=dict(dtick=1),
        yaxis=dict(autorange=True),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig


def fig_composicao_proporcional(
    df: pd.DataFrame,
    show_values: bool = False,
) -> go.Figure:
    """Barras empilhadas de composição proporcional do acervo."""
    fig = px.bar(
        df,
        x="ano",
        y="quantidade_ativos",
        color="classe",
        labels={
            "ano": "Ano",
            "quantidade_ativos": "Volume Total",
            "classe": "Classe",
        },
    )
    if show_values:
        fig.update_traces(
            text=df["quantidade_ativos"],
            textposition="outside",
        )
    fig.update_layout(
        template="plotly_white",
        xaxis=dict(dtick=4),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    return fig
