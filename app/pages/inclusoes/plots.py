"""Figuras Plotly para a página de Inclusões em Pauta."""

from __future__ import annotations
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

CORES_CLASSE = {
    "ADI":  "#2563eb",
    "ADPF": "#f59e0b",
    "ADC":  "#16a34a",
    "ADO":  "#ef4444",
}
CORES_MACRO = {
    "Concluído":     "#16a34a",
    "Não concluído": "#ef4444",
}
COR_LINHA = "#7f7f7f"
COR_PV    = "#2563eb"
COR_PP    = "#94a3b8"

_LEGEND = dict(
    orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
    font=dict(size=10, color="#333333"),
    bgcolor="#fcfcfc", bordercolor="#cccccc", borderwidth=1,
)
_LAYOUT = dict(
    template="plotly_white",
    height=500,
    margin=dict(t=120, b=80, l=60, r=60),
    legend=_LEGEND,
    xaxis=dict(dtick=1, title="Ano", tickangle=-45),
)
_CLASSES = ["ADI", "ADPF", "ADC", "ADO"]


def _bar_fig(barmode: str = "group") -> go.Figure:
    fig = go.Figure()
    fig.update_layout(**_LAYOUT, barmode=barmode)
    return fig


def _bar_com_linha(col_y_label: str, col_total_label: str) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.update_layout(**_LAYOUT, barmode="group")
    fig.update_yaxes(title_text=col_y_label, secondary_y=False)
    fig.update_yaxes(title_text=col_total_label, secondary_y=True)
    return fig


# ── Gráfico 5 ─────────────────────────────────────────────────────────────────

def g5_anual_ambiente(df: pd.DataFrame) -> tuple[go.Figure, go.Figure]:
    """Barras por ambiente + pizza PV vs PP."""
    tab = df.groupby(["ano", "ambiente"]).size().reset_index(name="n")
    fig = _bar_fig()
    for amb, cor in [("Plenário Virtual", COR_PV), ("Plenário Físico", COR_PP)]:
        d = tab[tab["ambiente"] == amb]
        fig.add_trace(go.Bar(
            x=d["ano"], y=d["n"], name=amb, marker_color=cor,
            text=d["n"], textposition="outside", cliponaxis=False,
        ))
    fig.update_layout(title_text="Inclusões em Pauta por Ano e Ambiente")

    pizza = df["ambiente"].value_counts()
    fig_p = go.Figure(go.Pie(
        labels=pizza.index, values=pizza.values, hole=0.4,
        textinfo="label+percent+value", textposition="outside",
        marker=dict(colors=[COR_PV, COR_PP], line=dict(color="white", width=2)),
    ))
    fig_p.update_layout(
        title_text="Proporção PV vs PP (período total)",
        template="plotly_white", height=420,
        margin=dict(t=80, b=60),
        legend=_LEGEND,
    )
    return fig, fig_p


# ── Gráfico 6 ─────────────────────────────────────────────────────────────────

def g6_pv_por_classe(df: pd.DataFrame) -> tuple[go.Figure, go.Figure]:
    """PV: barras por classe + linha total + pizza."""
    df_pv = df[df["ambiente"] == "Plenário Virtual"]
    tab = df_pv.groupby(["ano", "classe"]).size().reset_index(name="n")
    total = df_pv.groupby("ano").size().reset_index(name="n")

    fig = _bar_com_linha("Inclusões por classe", "Total PV (Linha)")
    for cls in _CLASSES:
        d = tab[tab["classe"] == cls]
        if d.empty:
            continue
        fig.add_trace(go.Bar(
            x=d["ano"], y=d["n"], name=cls,
            marker_color=CORES_CLASSE[cls],
            text=d["n"], textposition="outside", cliponaxis=False,
        ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=total["ano"], y=total["n"], mode="lines+markers",
        line=dict(color=COR_LINHA, width=2), marker=dict(size=5), name="Total PV",
    ), secondary_y=True)
    fig.update_layout(title_text="Inclusões por Classe e Ano — Plenário Virtual")

    pizza = df_pv["classe"].value_counts()
    fig_p = _pizza(pizza, "Proporção por Classe — PV (período total)")
    return fig, fig_p


# ── Gráfico 7 ─────────────────────────────────────────────────────────────────

def g7_pp_por_classe(df: pd.DataFrame) -> tuple[go.Figure, go.Figure]:
    """PP: barras por classe + linha total + pizza."""
    df_pp = df[df["ambiente"] == "Plenário Físico"]
    tab = df_pp.groupby(["ano", "classe"]).size().reset_index(name="n")
    total = df_pp.groupby("ano").size().reset_index(name="n")

    fig = _bar_com_linha("Inclusões por classe", "Total PP (Linha)")
    for cls in _CLASSES:
        d = tab[tab["classe"] == cls]
        if d.empty:
            continue
        fig.add_trace(go.Bar(
            x=d["ano"], y=d["n"], name=cls,
            marker_color=CORES_CLASSE[cls],
            text=d["n"], textposition="outside", cliponaxis=False,
        ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=total["ano"], y=total["n"], mode="lines+markers",
        line=dict(color=COR_LINHA, width=2), marker=dict(size=5), name="Total PP",
    ), secondary_y=True)
    fig.update_layout(title_text="Inclusões por Classe e Ano — Plenário Físico")

    pizza = df_pp["classe"].value_counts()
    fig_p = _pizza(pizza, "Proporção por Classe — PP (período total)")
    return fig, fig_p


# ── Gráficos 8 e 9 ────────────────────────────────────────────────────────────

def g8_desfecho_pv(df: pd.DataFrame) -> tuple[go.Figure, go.Figure]:
    """PV: pizza macro + pizza desfecho detalhado."""
    df_pv = df[df["ambiente"] == "Plenário Virtual"]
    fig_macro = _pizza(df_pv["macro_desfecho"].value_counts(),
                       "Concluídos e Não Concluídos — PV (período total)",
                       cores=[CORES_MACRO.get(l, "#94a3b8") for l in df_pv["macro_desfecho"].value_counts().index])
    fig_det = _pizza(df_pv["desfecho"].value_counts(),
                     "Desfecho Detalhado — PV (período total)", buraco=0.3)
    return fig_macro, fig_det


def g9_desfecho_pp(df: pd.DataFrame) -> go.Figure:
    """PP: pizza macro."""
    df_pp = df[df["ambiente"] == "Plenário Físico"]
    return _pizza(df_pp["macro_desfecho"].value_counts(),
                  "Concluídos e Não Concluídos — PP (período total)",
                  cores=[CORES_MACRO.get(l, "#94a3b8") for l in df_pp["macro_desfecho"].value_counts().index])


# ── Gráficos 10 e 11 ──────────────────────────────────────────────────────────

def g10_macro_anual_pv(df: pd.DataFrame) -> go.Figure:
    return _macro_anual(df[df["ambiente"] == "Plenário Virtual"],
                        "Concluídos e Não Concluídos por Ano — PV")


def g11_macro_anual_pp(df: pd.DataFrame) -> go.Figure:
    return _macro_anual(df[df["ambiente"] == "Plenário Físico"],
                        "Concluídos e Não Concluídos por Ano — PP")


def _macro_anual(df_amb: pd.DataFrame, titulo: str) -> go.Figure:
    tab = df_amb.groupby(["ano", "macro_desfecho"]).size().reset_index(name="n")
    fig = _bar_fig()
    for macro in ["Concluído", "Não concluído"]:
        d = tab[tab["macro_desfecho"] == macro]
        if d.empty:
            continue
        fig.add_trace(go.Bar(
            x=d["ano"], y=d["n"], name=macro,
            marker_color=CORES_MACRO[macro],
            text=d["n"], textposition="outside", cliponaxis=False,
        ))
    fig.update_layout(title_text=titulo)
    return fig


# ── Gráficos 12 e 13 ──────────────────────────────────────────────────────────

def g12_concluidos_pv(df: pd.DataFrame) -> go.Figure:
    return _concluidos_anual(df[df["ambiente"] == "Plenário Virtual"],
                             "Concluídos por Ano — PV")


def g13_concluidos_pp(df: pd.DataFrame) -> go.Figure:
    return _concluidos_anual(df[df["ambiente"] == "Plenário Físico"],
                             "Concluídos por Ano — PP")


def _concluidos_anual(df_amb: pd.DataFrame, titulo: str) -> go.Figure:
    tab = (df_amb[df_amb["macro_desfecho"] == "Concluído"]
           .groupby("ano").size().reset_index(name="n"))
    fig = _bar_fig()
    fig.add_trace(go.Bar(
        x=tab["ano"], y=tab["n"], name="Concluídos",
        marker_color=CORES_MACRO["Concluído"],
        text=tab["n"], textposition="outside", cliponaxis=False,
    ))
    fig.update_layout(title_text=titulo, yaxis_title="Inclusões concluídas")
    return fig


# ── Gráficos 14 e 15 ──────────────────────────────────────────────────────────

def g14_nao_concluidos_classe_pv(df: pd.DataFrame) -> go.Figure:
    return _por_classe_com_total(
        df[df["ambiente"] == "Plenário Virtual"],
        filtro_macro="Não concluído",
        titulo="Não Concluídos por Classe e Ano — PV",
        label_total="Total Não Concluídos PV",
    )


def g15_nao_concluidos_classe_pp(df: pd.DataFrame) -> go.Figure:
    return _por_classe_com_total(
        df[df["ambiente"] == "Plenário Físico"],
        filtro_macro="Não concluído",
        titulo="Não Concluídos por Classe e Ano — PP",
        label_total="Total Não Concluídos PP",
    )


# ── Gráficos 16 e 17 ──────────────────────────────────────────────────────────

def g16_concluidos_classe_pv(df: pd.DataFrame) -> go.Figure:
    return _por_classe_com_total(
        df[df["ambiente"] == "Plenário Virtual"],
        filtro_macro="Concluído",
        titulo="Concluídos por Classe e Ano — PV",
        label_total="Total Concluídos PV",
    )


def g17_concluidos_classe_pp(df: pd.DataFrame) -> go.Figure:
    return _por_classe_com_total(
        df[df["ambiente"] == "Plenário Físico"],
        filtro_macro="Concluído",
        titulo="Concluídos por Classe e Ano — PP",
        label_total="Total Concluídos PP",
    )


def _por_classe_com_total(df_amb: pd.DataFrame, filtro_macro: str,
                           titulo: str, label_total: str) -> go.Figure:
    df_f = df_amb[df_amb["macro_desfecho"] == filtro_macro]
    tab = df_f.groupby(["ano", "classe"]).size().reset_index(name="n")
    total = df_f.groupby("ano").size().reset_index(name="n")

    fig = _bar_com_linha("Inclusões por classe", label_total)
    for cls in _CLASSES:
        d = tab[tab["classe"] == cls]
        if d.empty:
            continue
        fig.add_trace(go.Bar(
            x=d["ano"], y=d["n"], name=cls,
            marker_color=CORES_CLASSE[cls],
            text=d["n"], textposition="outside", cliponaxis=False,
        ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=total["ano"], y=total["n"], mode="lines+markers",
        line=dict(color=COR_LINHA, width=2), marker=dict(size=5), name=label_total,
    ), secondary_y=True)
    fig.update_layout(title_text=titulo)
    return fig


# ── Utilitário pizza ──────────────────────────────────────────────────────────

def _pizza(series: pd.Series, titulo: str, buraco: float = 0.4,
           cores: list | None = None) -> go.Figure:
    kwargs = {}
    if cores:
        kwargs["marker"] = dict(colors=cores, line=dict(color="white", width=2))
    else:
        kwargs["marker"] = dict(line=dict(color="white", width=2))
    fig = go.Figure(go.Pie(
        labels=series.index, values=series.values, hole=buraco,
        textinfo="label+percent+value", textposition="outside",
        **kwargs,
    ))
    fig.update_layout(
        title_text=titulo, template="plotly_white", height=420,
        margin=dict(t=80, b=60), legend=_LEGEND,
    )
    return fig
