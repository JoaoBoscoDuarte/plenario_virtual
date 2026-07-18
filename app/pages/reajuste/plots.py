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
CORES_TRAM = {
    "Ambos os ambientes": "#8b5cf6",
    "Só Virtual":         "#2563eb",
    "Só Físico":          "#f59e0b",
}
CORES_TIPO = {"PR": "#2563eb", "RC": "#f59e0b", "QI": "#16a34a"}
_CLASSES = ["ADI", "ADPF", "ADC", "ADO"]
_ANOS    = list(range(2020, 2026))

_LEGEND = dict(
    orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
    font=dict(size=10, color="#333333"),
    bgcolor="#fcfcfc", bordercolor="#cccccc", borderwidth=1,
)
_LAYOUT_PIZZA = dict(
    template="plotly_white", height=500,
    margin=dict(t=120, b=80, l=60, r=60),
    showlegend=False,
)
_LAYOUT_BAR = dict(
    template="plotly_white", height=500,
    margin=dict(t=120, b=80, l=60, r=60),
    legend=_LEGEND,
    xaxis=dict(dtick=1, title="Ano", tickangle=-45),
    yaxis=dict(title="Inclusões com reajuste de voto"),
)


def _serie_reajuste(df_amb: pd.DataFrame) -> pd.Series:
    return df_amb["teve_reajuste"].map(
        {True: "Com reajuste de voto", False: "Sem reajuste de voto"}
    ).value_counts()


def _pizza_reajuste(df_amb: pd.DataFrame, titulo: str, show_values: bool = True) -> go.Figure:
    serie = _serie_reajuste(df_amb)
    cores = [CORES_REAJUSTE.get(l, "#999") for l in serie.index]
    textinfo = "label+value+percent" if show_values else "label+percent"
    fig = go.Figure(go.Pie(
        labels=serie.index, values=serie.values,
        hole=0.4,
        marker=dict(colors=cores, line=dict(color="white", width=2)),
        textinfo=textinfo,
        textfont=dict(size=13),
        textposition="auto",
        insidetextorientation="radial",
    ))
    fig.update_layout(title_text=titulo, **_LAYOUT_PIZZA)
    return fig


# ── G-R1 — Pizza reajuste por ambiente (selecionável) ──────────────────────────

def gr1_reajuste_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                           ambiente: str = "Plenário Virtual") -> go.Figure:
    return _pizza_reajuste(
        df[df["ambiente"] == ambiente],
        f"Inclusões com Reajuste de Voto — {ambiente} (2020–2025)",
        show_values=show_values,
    )


# ── G-R3 — Barras anuais por ambiente (selecionável) ───────────────────────────

def gr3_anual_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                        ambiente: str = "Plenário Virtual") -> go.Figure:
    return _barras_anuais(
        df[df["ambiente"] == ambiente],
        f"Reajuste de Voto por Ano — {ambiente} (2020–2025)",
        show_values=show_values,
    )


def _barras_anuais(df_amb: pd.DataFrame, titulo: str, show_values: bool = True) -> go.Figure:
    tab = (df_amb[df_amb["teve_reajuste"]]
           .groupby("ano").size().reset_index(name="n"))
    tab = (tab.set_index("ano")
              .reindex(_ANOS, fill_value=0)
              .reset_index())
    fig = go.Figure(go.Bar(
        x=tab["ano"], y=tab["n"],
        marker_color="#dc2626",
        text=tab["n"] if show_values else None,
        textposition="outside",
        cliponaxis=False,
        name="Com reajuste",
    ))
    fig.update_layout(title_text=titulo, **_LAYOUT_BAR)
    return fig


# ── G-R5 — Barras anuais por classe por ambiente (selecionável) ────────────────

def gr5_classe_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                         ambiente: str = "Plenário Virtual") -> go.Figure:
    return _barras_classe(
        df[df["ambiente"] == ambiente],
        f"Reajuste de Voto por Ano e Classe — {ambiente} (2020–2025)",
        show_values=show_values,
    )


def _barras_classe(df_amb: pd.DataFrame, titulo: str, show_values: bool = True) -> go.Figure:
    sub = df_amb[df_amb["teve_reajuste"]]
    tab = sub.groupby(["ano", "classe"], observed=True).size().reset_index(name="n")
    fig = go.Figure()
    for cls in _CLASSES:
        d = tab[tab["classe"] == cls]
        if d.empty:
            continue
        fig.add_trace(go.Bar(
            x=d["ano"], y=d["n"], name=cls,
            marker_color=CORES_CLASSE[cls],
            text=d["n"] if show_values else None,
            textposition="outside",
            cliponaxis=False,
        ))
    fig.update_layout(
        title_text=titulo,
        barmode="group",
        **_LAYOUT_BAR,
    )
    return fig
