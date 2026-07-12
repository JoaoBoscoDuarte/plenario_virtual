"""Figuras Plotly para a página de Reajuste de Voto."""

from __future__ import annotations
import plotly.graph_objects as go
import pandas as pd

CORES_CLASSE = {
    "ADI":  "#2563eb",
    "ADPF": "#f59e0b",
    "ADC":  "#16a34a",
    "ADO":  "#ef4444",
}
CORES_REAJUSTE = {
    "Com reajuste de voto": "#dc2626",
    "Sem reajuste de voto": "#e5e7eb",
}
_CLASSES = ["ADI", "ADPF", "ADC", "ADO"]
_ANOS    = list(range(2020, 2026))

_LEGEND = dict(
    orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
    font=dict(size=10, color="#333333"),
    bgcolor="#fcfcfc", bordercolor="#cccccc", borderwidth=1,
)
_LAYOUT_PIZZA = dict(
    template="plotly_white", height=420,
    margin=dict(t=80, b=60),
    legend=_LEGEND,
    showlegend=False,
)
_LAYOUT_BAR = dict(
    template="plotly_white", height=460,
    margin=dict(t=100, b=80, l=60, r=40),
    legend=_LEGEND,
    xaxis=dict(dtick=1, title="Ano", tickangle=-45),
    yaxis=dict(title="Inclusões com reajuste de voto"),
)


def _serie_reajuste(df_amb: pd.DataFrame) -> pd.Series:
    return df_amb["teve_reajuste"].map(
        {True: "Com reajuste de voto", False: "Sem reajuste de voto"}
    ).value_counts()


# ── G-R1 e G-R2 — Pizza período total (PV e PP) ───────────────────────────────

def gr1_pizza_pv(df: pd.DataFrame) -> go.Figure:
    return _pizza_reajuste(
        df[df["ambiente"] == "Plenário Virtual"],
        "Inclusões com Reajuste de Voto — Plenário Virtual (2020–2025)",
    )


def gr2_pizza_pp(df: pd.DataFrame) -> go.Figure:
    return _pizza_reajuste(
        df[df["ambiente"] == "Plenário Físico"],
        "Inclusões com Reajuste de Voto — Plenário Físico (2020–2025)",
    )


def _pizza_reajuste(df_amb: pd.DataFrame, titulo: str) -> go.Figure:
    serie = _serie_reajuste(df_amb)
    cores = [CORES_REAJUSTE.get(l, "#999") for l in serie.index]
    fig = go.Figure(go.Pie(
        labels=serie.index, values=serie.values,
        hole=0.4,
        marker=dict(colors=cores, line=dict(color="white", width=2)),
        textinfo="label+value+percent",
        textfont=dict(size=13),
    ))
    fig.update_layout(title_text=titulo, **_LAYOUT_PIZZA)
    return fig


# ── G-R3 e G-R4 — Barras anuais (PV e PP) ────────────────────────────────────

def gr3_anual_pv(df: pd.DataFrame) -> go.Figure:
    return _barras_anuais(
        df[df["ambiente"] == "Plenário Virtual"],
        "Reajuste de Voto por Ano — Plenário Virtual (2020–2025)",
    )


def gr4_anual_pp(df: pd.DataFrame) -> go.Figure:
    return _barras_anuais(
        df[df["ambiente"] == "Plenário Físico"],
        "Reajuste de Voto por Ano — Plenário Físico (2020–2025)",
    )


def _barras_anuais(df_amb: pd.DataFrame, titulo: str) -> go.Figure:
    tab = (df_amb[df_amb["teve_reajuste"]]
           .groupby("ano").size().reset_index(name="n"))
    tab = (tab.set_index("ano")
              .reindex(_ANOS, fill_value=0)
              .reset_index())
    fig = go.Figure(go.Bar(
        x=tab["ano"], y=tab["n"],
        marker_color="#dc2626",
        text=tab["n"], textposition="outside",
        cliponaxis=False,
        name="Com reajuste",
    ))
    fig.update_layout(title_text=titulo, **_LAYOUT_BAR)
    return fig


# ── G-R5 e G-R6 — Barras anuais por classe (PV e PP) ─────────────────────────

def gr5_classe_pv(df: pd.DataFrame) -> go.Figure:
    return _barras_classe(
        df[df["ambiente"] == "Plenário Virtual"],
        "Reajuste de Voto por Ano e Classe — Plenário Virtual (2020–2025)",
    )


def gr6_classe_pp(df: pd.DataFrame) -> go.Figure:
    return _barras_classe(
        df[df["ambiente"] == "Plenário Físico"],
        "Reajuste de Voto por Ano e Classe — Plenário Físico (2020–2025)",
    )


def _barras_classe(df_amb: pd.DataFrame, titulo: str) -> go.Figure:
    sub = df_amb[df_amb["teve_reajuste"]]
    tab = sub.groupby(["ano", "classe"]).size().reset_index(name="n")
    fig = go.Figure()
    for cls in _CLASSES:
        d = tab[tab["classe"] == cls]
        if d.empty:
            continue
        fig.add_trace(go.Bar(
            x=d["ano"], y=d["n"], name=cls,
            marker_color=CORES_CLASSE[cls],
            text=d["n"], textposition="outside",
            cliponaxis=False,
        ))
    fig.update_layout(
        title_text=titulo,
        barmode="group",
        **_LAYOUT_BAR,
    )
    return fig
