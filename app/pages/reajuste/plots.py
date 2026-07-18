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
    "Virtual":            "#2563eb",
    "Físico":             "#f59e0b",
}
CORES_TIPO = {"PR": "#2563eb", "RC": "#f59e0b", "QI": "#16a34a"}
_CLASSES = ["ADI", "ADPF", "ADC", "ADO"]
_ANOS    = list(range(2020, 2026))

_LEGEND = dict(
    orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
    font=dict(family="Arial, sans-serif", size=17, color="black"),
)
_LAYOUT_BAR = dict(
    template="plotly_white", height=500,
    margin=dict(t=120, b=80, l=60, r=60),
    legend=_LEGEND,
    title_font=dict(family="Arial, sans-serif", size=26, color="black"),
    xaxis=dict(dtick=1, title="Ano", tickangle=-45,
               title_font=dict(family="Arial, sans-serif", size=18, color="black"),
               tickfont=dict(family="Arial, sans-serif", size=17, color="black"),
               showline=True, linewidth=2, linecolor="black",
               showgrid=True, gridwidth=1, gridcolor="#d0d0d0"),
    yaxis=dict(title="Inclusões com reajuste de voto",
               title_font=dict(family="Arial, sans-serif", size=18, color="black"),
               tickfont=dict(family="Arial, sans-serif", size=17, color="black"),
               showline=True, linewidth=2, linecolor="black",
               showgrid=True, gridwidth=1, gridcolor="#d0d0d0"),
)
_AXIS = dict(
    showline=True, linewidth=2, linecolor="black",
    showgrid=True, gridwidth=1, gridcolor="#d0d0d0",
    title_font=dict(family="Arial, sans-serif", size=18, color="black"),
    tickfont=dict(family="Arial, sans-serif", size=17, color="black"),
)
def _serie_reajuste(df_amb: pd.DataFrame) -> pd.Series:
    return df_amb["teve_reajuste"].map(
        {True: "Com reajuste de voto", False: "Sem reajuste de voto"}
    ).value_counts()
# ── G-R1 — Pizza reajuste por ambiente (lado a lado) ───────────────────────────

def gr1_reajuste_filtravel(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    from plotly.subplots import make_subplots
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'pie'}, {'type': 'pie'}]],
        subplot_titles=["Plenário Virtual", "Plenário Presencial"],
    )
    for i, amb in enumerate(["Plenário Virtual", "Plenário Presencial"]):
        d = df[df["ambiente"] == amb]
        serie = _serie_reajuste(d)
        cores = [CORES_REAJUSTE.get(l, "#999") for l in serie.index]
        fig.add_trace(go.Pie(
            labels=[str(l).upper() for l in serie.index], values=serie.values,
            hole=0.4,
            marker=dict(colors=cores, line=dict(color="white", width=2)),
            textinfo="percent" if show_values else "none",
            textfont=dict(family="Arial, sans-serif", size=14, color="black"),
            textposition="inside",
            insidetextorientation="radial",
            showlegend=True,
            legendgroup="group",
        ), row=1, col=i + 1)
    fig.update_layout(
        title_text="Inclusões com reajuste de voto — período total (2020–2025)",
        template="plotly_white", height=500,
        margin=dict(t=120, b=120, l=60, r=60),
        title_font=dict(family="Arial, sans-serif", size=26, color="black"),
        legend=dict(
            orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5,
            font=dict(family="Arial, sans-serif", size=17, color="black"),
        ),
    )
    fig.update_annotations(
        font=dict(family="Arial, sans-serif", size=18, color="black"),
    )
    return fig
# ── G-R3 — Barras anuais por ambiente (selecionável) ───────────────────────────

def gr3_anual_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                        ambiente: str = "Plenário Virtual") -> go.Figure:
    return _barras_anuais(
        df[df["ambiente"] == ambiente],
        f"Reajuste de voto por ano — {ambiente} (2020–2025)",
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
        name="COM REAJUSTE",
    ))
    fig.update_layout(title_text=titulo, **_LAYOUT_BAR)
    fig.update_xaxes(**_AXIS)
    fig.update_yaxes(**_AXIS)
    return fig
# ── G-R5 — Barras anuais por classe por ambiente (selecionável) ────────────────

def gr5_classe_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                         ambiente: str = "Plenário Virtual") -> go.Figure:
    return _barras_classe(
        df[df["ambiente"] == ambiente],
        f"Reajuste de voto por ano e classe — {ambiente} (2020–2025)",
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
            x=d["ano"], y=d["n"], name=cls.upper(),
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
    fig.update_xaxes(**_AXIS)
    fig.update_yaxes(**_AXIS)
    return fig
