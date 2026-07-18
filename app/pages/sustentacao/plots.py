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
CORES_AMB   = {"Plenário Virtual": "#2563eb", "Plenário Presencial": "#94a3b8"}
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

def _pizza(serie: pd.Series, titulo: str, cores: list, show_values: bool = True) -> go.Figure:
    fig = go.Figure(go.Pie(
        labels=serie.index, values=serie.values,
        hole=0.4,
        marker=dict(colors=cores, line=dict(color="white", width=2)),
        textinfo="label+value+percent" if show_values else "label",
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


def _pizza_sust(df_amb: pd.DataFrame, titulo: str, show_values: bool = True) -> go.Figure:
    return _pizza(_serie_sust(df_amb), titulo,
                  [CORES_SUST.get(l, "#999") for l in _serie_sust(df_amb).index],
                  show_values=show_values)


def _barras_anuais(df_amb: pd.DataFrame, titulo: str, show_values: bool = True) -> go.Figure:
    tab = (df_amb[df_amb["teve_sustentacao"]]
           .groupby("ano").size().reset_index(name="n"))
    tab = tab.set_index("ano").reindex(_ANOS, fill_value=0).reset_index()
    fig = go.Figure(go.Bar(
        x=tab["ano"], y=tab["n"],
        marker_color="#0891b2",
        text=tab["n"] if show_values else None,
        textposition="outside", cliponaxis=False,
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
                  cores: dict, titulo: str, x_title: str = "Ano",
                  show_values: bool = True) -> go.Figure:
    tab   = df_sub.groupby(["ano", col_grupo], observed=True).size().reset_index(name="n")
    total = df_sub.groupby("ano", observed=True).size().reset_index(name="n")
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
            text=d["n"] if show_values else None,
            textposition="outside", cliponaxis=False,
        ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=total["ano"], y=total["n"], mode="lines+markers",
        line=dict(color=COR_LINHA, width=2), marker=dict(size=5),
        name="Total",
    ), secondary_y=True)
    fig.update_layout(title_text=titulo)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# S1/S2 — Pizza período total (PV/PP selecionável)
# ═══════════════════════════════════════════════════════════════════════════════

def gs1_sust_filtravel(df: pd.DataFrame, show_values: bool = True,
                       ambiente: str = "Plenário Virtual") -> go.Figure:
    return _pizza_sust(
        df[df["ambiente"] == ambiente],
        f"Inclusões com Sustentação Oral — {ambiente} (2020–2025)",
        show_values=show_values,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# S3/S4 — Barras anuais (PV/PP selecionável)
# ═══════════════════════════════════════════════════════════════════════════════

def gs3_sust_anual_filtravel(df: pd.DataFrame, show_values: bool = True,
                             ambiente: str = "Plenário Virtual") -> go.Figure:
    return _barras_anuais(
        df[df["ambiente"] == ambiente],
        f"Sustentação Oral por Ano — {ambiente} (2020–2025)",
        show_values=show_values,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# S5/S6 — Por ano e classe (PV/PP selecionável)
# ═══════════════════════════════════════════════════════════════════════════════

def gs5_sust_classe_filtravel(df: pd.DataFrame, show_values: bool = True,
                              ambiente: str = "Plenário Virtual") -> go.Figure:
    sub = df[(df["ambiente"] == ambiente) & df["teve_sustentacao"]]
    return _barras_grupo(sub, "classe", CORES_CLASSE,
                         f"Sustentação Oral por Ano e Classe — {ambiente} (2020–2025)",
                         show_values=show_values)


# ═══════════════════════════════════════════════════════════════════════════════
# S7 — Por ano e tipo de questão (PV/PP selecionável)
# ═══════════════════════════════════════════════════════════════════════════════

def gs7_sust_tipo_filtravel(df: pd.DataFrame, show_values: bool = True,
                            ambiente: str = "Plenário Virtual") -> go.Figure:
    sub = df[(df["ambiente"] == ambiente) & df["teve_sustentacao"]].copy()
    sub["tipo_questao"] = sub["tipo_questao"].replace({"IJ": "QI"})
    return _barras_grupo(sub, "tipo_questao", CORES_TIPO,
                         f"Sustentação Oral por Ano e Tipo de Questão — {ambiente} (2020–2025)",
                         show_values=show_values)


# ═══════════════════════════════════════════════════════════════════════════════
# S8 — Taxa de sustentação por ano e ambiente (%)
# ═══════════════════════════════════════════════════════════════════════════════

def gs8_taxa_ambiente(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    tab = (df.groupby(["ano", "ambiente"], observed=True)["teve_sustentacao"]
           .mean().mul(100).reset_index(name="n"))
    fig = go.Figure()
    for amb, cor in CORES_AMB.items():
        d = tab[tab["ambiente"] == amb]
        vals = d["n"].round(1)
        fig.add_trace(go.Bar(
            x=d["ano"], y=vals, name=amb,
            marker_color=cor,
            text=(vals.astype(str) + "%") if show_values else None,
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
