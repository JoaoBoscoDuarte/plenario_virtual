"""Funções de construção de figuras Plotly para a página de Acervo."""

from __future__ import annotations
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

_CORES = {
    "ADI":  "#1f77b4",
    "ADPF": "#ff7f0e",
    "ADC":  "#2ca02c",
    "ADO":  "#d62728",
}

_LAYOUT_BASE = dict(
    template="plotly_white",
    height=480,
    xaxis=dict(dtick=1, tickangle=-45),
    hovermode="x unified",
    legend_title="Classe Processual",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=20, r=20, t=30, b=60),
)


def _apply_values_line(fig: go.Figure, show_values: bool) -> None:
    if show_values:
        fig.update_traces(mode="lines+markers+text", textposition="top center")


def _apply_values_bar(fig: go.Figure, df: pd.DataFrame, val_col: str, position: str, show_values: bool) -> None:
    if not show_values:
        return
    for trace in fig.data:
        mask = df["classe"] == trace.name if "classe" in df.columns else pd.Series([True] * len(df))
        vals = df.loc[mask, val_col].tolist()
        trace.update(text=vals, textposition=position)


def _bar_or_line(df, x, y, color=None, chart_type="Linhas", show_values=False,
                 color_map=None, single_color=None, labels=None):
    """Helper: constrói fig de linha, barra agrupada ou empilhada."""
    kw = dict(x=x, y=y, labels=labels or {})
    if color:
        kw["color"] = color
        kw["color_discrete_map"] = color_map or _CORES

    if chart_type == "Linhas":
        fig = px.line(df, markers=True, **kw)
        if single_color:
            fig.update_traces(line_color=single_color, line_width=2)
        _apply_values_line(fig, show_values)

    elif chart_type == "Barras Empilhadas":
        fig = px.bar(df, barmode="stack", **kw)
        if color:
            _apply_values_bar(fig, df, y, "inside", show_values)
        elif show_values:
            fig.update_traces(text=df[y], textposition="inside")

    else:  # Barras
        fig = px.bar(df, barmode="group", **kw)
        if color:
            _apply_values_bar(fig, df, y, "outside", show_values)
        elif show_values:
            fig.update_traces(text=df[y], textposition="outside")

    return fig


# ── Gráficos de TOTAL (df_totais: groupby ano) ────────────────────────────────

def fig_total_geral_por_ano(df: pd.DataFrame, chart_type="Linhas", show_values=False) -> go.Figure:
    """Fig 1 — evolução do total_geral (todas as classes somadas)."""
    df_t = df.groupby("ano", as_index=False)["total_geral"].sum()
    fig = _bar_or_line(df_t, "ano", "total_geral", chart_type=chart_type,
                       show_values=show_values, single_color="#4C72B0",
                       labels={"ano": "Ano de Referência", "total_geral": "Processos"})
    fig.update_layout(**_LAYOUT_BASE, yaxis_title="Quantidade de Processos")
    return fig


def fig_total_geral_por_classe(df: pd.DataFrame, chart_type="Linhas", show_values=False) -> go.Figure:
    """Fig 2 — evolução do total_geral por classe."""
    fig = _bar_or_line(df, "ano", "total_geral", color="classe",
                       chart_type=chart_type, show_values=show_values,
                       labels={"ano": "Ano de Referência", "total_geral": "Processos", "classe": "Classe Processual"})
    fig.update_layout(**_LAYOUT_BASE, yaxis_title="Quantidade de Processos")
    return fig


def fig_total_por_ano(df: pd.DataFrame, chart_type="Linhas", show_values=False) -> go.Figure:
    """Fig 3 — evolução do acervo ATIVO (todas as classes somadas)."""
    df_t = df.groupby("ano", as_index=False)["quantidade_ativos"].sum()
    fig = _bar_or_line(df_t, "ano", "quantidade_ativos", chart_type=chart_type,
                       show_values=show_values, single_color="#2ca02c",
                       labels={"ano": "Ano de Referência", "quantidade_ativos": "Processos Ativos"})
    fig.update_layout(**_LAYOUT_BASE, yaxis_title="Quantidade de Processos")
    return fig


def fig_evolucao_acervo(df: pd.DataFrame, chart_type="Linhas", show_values=False) -> go.Figure:
    """Fig 4 — evolução do acervo ATIVO por classe."""
    fig = _bar_or_line(df, "ano", "quantidade_ativos", color="classe",
                       chart_type=chart_type, show_values=show_values,
                       labels={"ano": "Ano de Referência", "quantidade_ativos": "Processos Ativos", "classe": "Classe Processual"})
    fig.update_layout(**_LAYOUT_BASE, yaxis_title="Quantidade de Processos")
    return fig


def fig_total_inativos_por_ano(df: pd.DataFrame, chart_type="Linhas", show_values=False) -> go.Figure:
    """Fig 5 — evolução do acervo INATIVO (todas as classes somadas)."""
    df_t = df.groupby("ano", as_index=False)["quantidade_inativos"].sum()
    fig = _bar_or_line(df_t, "ano", "quantidade_inativos", chart_type=chart_type,
                       show_values=show_values, single_color="#d62728",
                       labels={"ano": "Ano de Referência", "quantidade_inativos": "Processos Inativos"})
    fig.update_layout(**_LAYOUT_BASE, yaxis_title="Quantidade de Processos")
    return fig


def fig_inativos_por_classe(df: pd.DataFrame, chart_type="Linhas", show_values=False) -> go.Figure:
    """Fig 6 — evolução do acervo INATIVO por classe."""
    fig = _bar_or_line(df, "ano", "quantidade_inativos", color="classe",
                       chart_type=chart_type, show_values=show_values,
                       labels={"ano": "Ano de Referência", "quantidade_inativos": "Processos Inativos", "classe": "Classe Processual"})
    fig.update_layout(**_LAYOUT_BASE, yaxis_title="Quantidade de Processos")
    return fig


def fig_composicao_proporcional(df: pd.DataFrame, show_values=False) -> go.Figure:
    """Barras empilhadas de composição proporcional do acervo ativo."""
    fig = px.bar(df, x="ano", y="quantidade_ativos", color="classe",
                 barmode="stack", color_discrete_map=_CORES,
                 labels={"ano": "Ano", "quantidade_ativos": "Processos Ativos", "classe": "Classe Processual"})
    if show_values:
        _apply_values_bar(fig, df, "quantidade_ativos", "inside", True)
    fig.update_layout(**_LAYOUT_BASE, yaxis_title="Quantidade de Processos")
    return fig
