"""Figuras Plotly para a página de Reajuste de Voto."""

from __future__ import annotations
import plotly.graph_objects as go
import pandas as pd

from estilo import aplicar_padrao, AZUL, CINZA, VERDE, ROXO, VERMELHO

CORES_CLASSE = {
    "ADI":  AZUL,
    "ADPF": "#f59e0b",
    "ADC":  VERDE,
    "ADO":  "#ef4444",
}
CORES_REAJUSTE = {
    "Com reajuste de voto": VERMELHO,
    "Sem reajuste de voto": CINZA,
}
CORES_TRAM = {
    "Ambos os ambientes": ROXO,
    "Virtual":            AZUL,
    "Físico":             "#f59e0b",
}
CORES_TIPO = {"PR": AZUL, "RC": "#f59e0b", "QI": VERDE}
_CLASSES = ["ADI", "ADPF", "ADC", "ADO"]
_ANOS    = list(range(2020, 2026))


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
    aplicar_padrao(
        fig,
        "Inclusões com reajuste de voto — período total (2020–2025)",
        "Proporção por ambiente (Plenário Virtual e Plenário Presencial)",
        height=500, showlegend=True,
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
        marker_color=VERMELHO,
        text=tab["n"] if show_values else None,
        textposition="outside",
        cliponaxis=False,
        name="COM REAJUSTE",
    ))
    aplicar_padrao(
        fig, titulo, "Volume anual de inclusões com reajuste de voto",
        xaxis=dict(dtick=1, title="Ano", tickangle=-45),
        yaxis=dict(title="Inclusões com reajuste de voto"),
    )
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
    aplicar_padrao(
        fig, titulo, "Distribuição por classe processual (ADI, ADPF, ADC, ADO)",
        barmode="group", showlegend=True,
        xaxis=dict(dtick=1, title="Ano", tickangle=-45),
        yaxis=dict(title="Inclusões com reajuste de voto"),
    )
    return fig
