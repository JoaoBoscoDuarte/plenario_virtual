"""Figuras Plotly para a página de Tramitação por Ambiente."""

from __future__ import annotations
import plotly.graph_objects as go
import pandas as pd

CORES_TRAM = {
    "Ambos os ambientes": "#8b5cf6",
    "Só Virtual":         "#2563eb",
    "Só Físico":          "#f59e0b",
}
CORES_TIPO = {"PR": "#2563eb", "RC": "#f59e0b", "QI": "#16a34a"}

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
)


def gt1_tramitacao(df: pd.DataFrame) -> go.Figure:
    """Pizza: distribuição dos processos distintos por ambiente de tramitação."""
    serie = df.drop_duplicates("incidente")["tramitacao"].value_counts()
    cores = [CORES_TRAM.get(l, "#999") for l in serie.index]
    fig = go.Figure(go.Pie(
        labels=serie.index, values=serie.values,
        hole=0.4,
        marker=dict(colors=cores, line=dict(color="white", width=2)),
        textinfo="label+value+percent",
        textfont=dict(size=13),
        textposition="auto",
        insidetextorientation="radial",
    ))
    fig.update_layout(
        title_text="Tramitação por Ambiente — Processos CC (2020–2025)",
        **_LAYOUT_PIZZA,
    )
    return fig


def gt2_ambos_por_tipo(df: pd.DataFrame) -> go.Figure:
    """Barras: processos que tramitaram em ambos os ambientes, por tipo de questão."""
    ambos = (
        df[df["tramitou_ambos"]]
        .drop_duplicates("incidente")
        .copy()
    )
    ambos["tipo_questao"] = ambos["tipo_questao"].replace({"IJ": "QI"})
    tab = ambos["tipo_questao"].value_counts().reset_index()
    tab.columns = ["tipo_questao", "n"]
    tab = tab.sort_values("tipo_questao")

    fig = go.Figure()
    for _, row in tab.iterrows():
        fig.add_trace(go.Bar(
            x=[row["tipo_questao"]], y=[row["n"]],
            name=row["tipo_questao"],
            marker_color=CORES_TIPO.get(row["tipo_questao"], "#999"),
            text=[row["n"]], textposition="outside",
            cliponaxis=False,
        ))
    fig.update_layout(
        title_text="Processos em Ambos os Ambientes por Tipo de Questão (2020–2025)",
        barmode="group",
        xaxis=dict(title="Tipo de Questão"),
        yaxis=dict(title="Processos distintos"),
        **_LAYOUT_BAR,
    )
    return fig
