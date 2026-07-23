"""Figuras Plotly para a página de Reajuste de Voto."""

from __future__ import annotations
import plotly.graph_objects as go
import pandas as pd

from estilo import aplicar_padrao, add_er_marker, add_espin_shade, AZUL, CINZA, VERDE, ROXO, VERMELHO

CORES_CLASSE = {
    "ADI":  AZUL,
    "ADPF": "#f59e0b",
    "ADC":  VERDE,
    "ADO":  "#ef4444",
}
CORES_TRAM = {
    "Ambos os ambientes": ROXO,
    "Virtual":            AZUL,
    "Físico":             "#f59e0b",
}
CORES_TIPO = {"PR": AZUL, "RC": "#f59e0b", "QI": VERDE}
_CLASSES = ["ADI", "ADPF", "ADC", "ADO"]
_ANOS    = list(range(2020, 2026))


# ── G-R1 — % de inclusões com reajuste de voto, por ambiente ───────────────────

def gr1_reajuste_pct(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    ambientes = ["Plenário Virtual", "Plenário Presencial"]
    pcts = [100 * df[df["ambiente"] == a]["teve_reajuste"].mean() for a in ambientes]
    maior = "Plenário Presencial" if pcts[1] > pcts[0] else "Plenário Virtual"
    fig = go.Figure(go.Bar(
        x=[a.upper() for a in ambientes], y=pcts,
        marker_color=VERMELHO,
        text=[f"{v:.1f}%".replace(".", ",") for v in pcts] if show_values else None,
        textposition="outside", textfont=dict(family="Arial, sans-serif", size=20, color="black", weight="bold"),
        cliponaxis=False,
    ))
    aplicar_padrao(
        fig,
        f"Reajuste de voto é mais comum no {maior}",
        "% de inclusões com ao menos um reajuste de voto, por ambiente (2020–2025)",
        xaxis=dict(title=""), yaxis=dict(title="", range=[0, max(pcts) * 1.3]),
    )
    fig.update_yaxes(showline=False, showticklabels=False, ticks="")
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
    y_max = float(tab["n"].max() or 1)
    fig = go.Figure(go.Bar(
        x=tab["ano"], y=tab["n"],
        marker_color=VERMELHO,
        text=tab["n"] if show_values else None,
        textposition="outside",
        textfont=dict(family="Arial, sans-serif", size=17, color="black", weight="bold"),
        cliponaxis=False,
        name="COM REAJUSTE",
    ))
    aplicar_padrao(
        fig, titulo, "Volume anual de inclusões com reajuste de voto",
        xaxis=dict(dtick=1, title="Ano", tickangle=-45),
        yaxis=dict(title="Inclusões com reajuste de voto", range=[0, y_max * 1.3]),
    )
    add_espin_shade(fig, ano_base=0, y0=0, y1=y_max * 1.25, y_label=y_max * 1.18)
    add_er_marker(fig, ano_base=0, er=53, y0=0, y1=y_max * 1.25, y_label=y_max * 1.05)
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
    y_max = float(tab["n"].max() or 1)
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
            textfont=dict(family="Arial, sans-serif", size=17, color="black", weight="bold"),
            cliponaxis=False,
        ))
    aplicar_padrao(
        fig, titulo, "Distribuição por classe processual (ADI, ADPF, ADC, ADO)",
        barmode="group", showlegend=True,
        xaxis=dict(dtick=1, title="Ano", tickangle=-45),
        yaxis=dict(title="Inclusões com reajuste de voto", range=[0, y_max * 1.3]),
    )
    add_espin_shade(fig, ano_base=0, y0=0, y1=y_max * 1.25, y_label=y_max * 1.18)
    add_er_marker(fig, ano_base=0, er=53, y0=0, y1=y_max * 1.25, y_label=y_max * 1.05)
    return fig
