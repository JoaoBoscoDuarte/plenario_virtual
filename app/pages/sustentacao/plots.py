"""Figuras Plotly para a página de Sustentação Oral."""

from __future__ import annotations
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

CORES_SUST = {
    "Com sustentação oral": "#0891b2",
    "Sem sustentação oral": "#e5e7eb",
}
CORES_CLASSE = {
    "ADI":  "#2563eb",
    "ADPF": "#f59e0b",
    "ADC":  "#16a34a",
    "ADO":  "#ef4444",
}
CORES_TIPO  = {"PR": "#2563eb", "RC": "#f59e0b", "QI": "#16a34a"}
CORES_AMB   = {"Plenário Virtual": "#2563eb", "Plenário Físico": "#94a3b8"}
COR_LINHA   = "#7f7f7f"
_CLASSES    = ["ADI", "ADPF", "ADC", "ADO"]
_TIPOS      = ["PR", "RC", "QI"]
_ANOS       = list(range(2020, 2026))

_LEGEND = dict(
    orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
    font=dict(size=10, color="#333333"),
    bgcolor="#fcfcfc", bordercolor="#cccccc", borderwidth=1,
)
_LAYOUT = dict(
    template="plotly_white", height=500,
    margin=dict(t=120, b=80, l=60, r=60),
    legend=_LEGEND,
)
_LAYOUT_PIZZA = dict(
    template="plotly_white", height=500,
    margin=dict(t=120, b=80, l=60, r=60),
    showlegend=False,
)


# ── helpers ───────────────────────────────────────────────────────────────────

def _pizza(serie: pd.Series, titulo: str, cores: list) -> go.Figure:
    fig = go.Figure(go.Pie(
        labels=serie.index, values=serie.values,
        hole=0.4,
        marker=dict(colors=cores, line=dict(color="white", width=2)),
        textinfo="label+value+percent",
        textfont=dict(size=13),
        textposition="auto",
        insidetextorientation="radial",
    ))
    fig.update_layout(title_text=titulo, **_LAYOUT_PIZZA)
    return fig


def _serie_sust(df_amb: pd.DataFrame) -> pd.Series:
    return df_amb["teve_sustentacao"].map(
        {True: "Com sustentação oral", False: "Sem sustentação oral"}
    ).value_counts()


def _barras_anuais(df_amb: pd.DataFrame, titulo: str) -> go.Figure:
    tab = (df_amb[df_amb["teve_sustentacao"]]
           .groupby("ano").size().reset_index(name="n"))
    tab = tab.set_index("ano").reindex(_ANOS, fill_value=0).reset_index()
    fig = go.Figure(go.Bar(
        x=tab["ano"], y=tab["n"],
        marker_color="#0891b2",
        text=tab["n"], textposition="outside", cliponaxis=False,
        name="Com sustentação",
    ))
    fig.update_layout(
        title_text=titulo,
        xaxis=dict(dtick=1, title="Ano", tickangle=-45),
        yaxis=dict(title="Inclusões com sustentação oral"),
        **_LAYOUT,
    )
    return fig


def _barras_grupo(df_sub: pd.DataFrame, col_grupo: str,
                  cores: dict, titulo: str, x_title: str = "Ano") -> go.Figure:
    tab   = df_sub.groupby(["ano", col_grupo]).size().reset_index(name="n")
    total = df_sub.groupby("ano").size().reset_index(name="n")
    fig   = make_subplots(specs=[[{"secondary_y": True}]])
    fig.update_layout(
        **_LAYOUT, barmode="group",
        xaxis=dict(dtick=1, title=x_title, tickangle=-45),
    )
    fig.update_yaxes(title_text="Inclusões com sustentação", secondary_y=False)
    fig.update_yaxes(title_text="Total (Linha)", secondary_y=True)
    grupos = [g for g in cores if g in tab[col_grupo].unique()]
    for g in grupos:
        d = tab[tab[col_grupo] == g]
        fig.add_trace(go.Bar(
            x=d["ano"], y=d["n"], name=g,
            marker_color=cores[g],
            text=d["n"], textposition="outside", cliponaxis=False,
        ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=total["ano"], y=total["n"], mode="lines+markers",
        line=dict(color=COR_LINHA, width=2), marker=dict(size=5),
        name="Total",
    ), secondary_y=True)
    fig.update_layout(title_text=titulo)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# S1–S2 — Pizza período total (PV e PP)
# ═══════════════════════════════════════════════════════════════════════════════

def gs1_pizza_pv(df: pd.DataFrame) -> go.Figure:
    sub = df[df["ambiente"] == "Plenário Virtual"]
    return _pizza(
        _serie_sust(sub),
        "Inclusões com Sustentação Oral — Plenário Virtual (2020–2025)",
        [CORES_SUST.get(l, "#999") for l in _serie_sust(sub).index],
    )


def gs2_pizza_pp(df: pd.DataFrame) -> go.Figure:
    sub = df[df["ambiente"] == "Plenário Físico"]
    return _pizza(
        _serie_sust(sub),
        "Inclusões com Sustentação Oral — Plenário Físico (2020–2025)",
        [CORES_SUST.get(l, "#999") for l in _serie_sust(sub).index],
    )


# ═══════════════════════════════════════════════════════════════════════════════
# S3–S4 — Barras anuais (PV e PP)
# ═══════════════════════════════════════════════════════════════════════════════

def gs3_anual_pv(df: pd.DataFrame) -> go.Figure:
    return _barras_anuais(
        df[df["ambiente"] == "Plenário Virtual"],
        "Sustentação Oral por Ano — Plenário Virtual (2020–2025)",
    )


def gs4_anual_pp(df: pd.DataFrame) -> go.Figure:
    return _barras_anuais(
        df[df["ambiente"] == "Plenário Físico"],
        "Sustentação Oral por Ano — Plenário Físico (2020–2025)",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# S5–S6 — Por ano e classe (PV e PP)
# ═══════════════════════════════════════════════════════════════════════════════

def gs5_classe_pv(df: pd.DataFrame) -> go.Figure:
    sub = df[(df["ambiente"] == "Plenário Virtual") & df["teve_sustentacao"]]
    return _barras_grupo(sub, "classe", CORES_CLASSE,
                         "Sustentação Oral por Ano e Classe — Plenário Virtual (2020–2025)")


def gs6_classe_pp(df: pd.DataFrame) -> go.Figure:
    sub = df[(df["ambiente"] == "Plenário Físico") & df["teve_sustentacao"]]
    return _barras_grupo(sub, "classe", CORES_CLASSE,
                         "Sustentação Oral por Ano e Classe — Plenário Físico (2020–2025)")


# ═══════════════════════════════════════════════════════════════════════════════
# S7 — Por ano e tipo de questão (PV)
# ═══════════════════════════════════════════════════════════════════════════════

def gs7_tipo_pv(df: pd.DataFrame) -> go.Figure:
    sub = df[(df["ambiente"] == "Plenário Virtual") & df["teve_sustentacao"]].copy()
    sub["tipo_questao"] = sub["tipo_questao"].replace({"IJ": "QI"})
    return _barras_grupo(sub, "tipo_questao", CORES_TIPO,
                         "Sustentação Oral por Ano e Tipo de Questão — Plenário Virtual (2020–2025)")


# ═══════════════════════════════════════════════════════════════════════════════
# S8 — Taxa de sustentação por ano e ambiente (%)
# ═══════════════════════════════════════════════════════════════════════════════

def gs8_taxa_ambiente(df: pd.DataFrame) -> go.Figure:
    tab = (df.groupby(["ano", "ambiente"])["teve_sustentacao"]
           .mean().mul(100).reset_index(name="n"))
    fig = go.Figure()
    for amb, cor in CORES_AMB.items():
        d = tab[tab["ambiente"] == amb]
        fig.add_trace(go.Bar(
            x=d["ano"], y=d["n"].round(1), name=amb,
            marker_color=cor,
            text=d["n"].round(1).astype(str) + "%",
            textposition="outside", cliponaxis=False,
        ))
    fig.update_layout(
        title_text="Taxa de Sustentação Oral por Ano e Ambiente (%) (2020–2025)",
        barmode="group",
        xaxis=dict(dtick=1, title="Ano", tickangle=-45),
        yaxis=dict(title="% de inclusões com sustentação"),
        **_LAYOUT,
    )
    return fig
