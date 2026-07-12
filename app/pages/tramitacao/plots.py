"""Figuras Plotly para a página de Tramitação por Ambiente."""

from __future__ import annotations
import plotly.graph_objects as go
import pandas as pd

CORES_TRAM = {
    "Ambos os ambientes": "#8b5cf6",
    "Só Virtual":         "#2563eb",
    "Só Físico":          "#f59e0b",
}
CORES_CLASSE = {
    "ADI":  "#2563eb",
    "ADPF": "#f59e0b",
    "ADC":  "#16a34a",
    "ADO":  "#ef4444",
}
CORES_TIPO = {"PR": "#2563eb", "RC": "#f59e0b", "QI": "#16a34a"}
CORES_MACRO = {
    "Concluído":     "#16a34a",
    "Não concluído": "#ef4444",
}
CORES_DESFECHO = {
    "Concluído - decisão unânime":                       "#16a34a",
    "Concluído - decisão maioria com o relator":         "#2563eb",
    "Concluído - decisão maioria, vencido o relator":    "#f59e0b",
    "Não concluído - pedido de vista":                   "#8b5cf6",
    "Não concluído - destaque":                          "#ec4899",
    "Não concluído - retirado de pauta":                 "#f97316",
    "Não concluído - motivos diversos":                  "#9ca3af",
}
_CLASSES = ["ADI", "ADPF", "ADC", "ADO"]
_TIPOS   = ["PR", "RC", "QI"]
_TRAMS   = ["Só Virtual", "Só Físico", "Ambos os ambientes"]

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


def _barras_grupo(tab: pd.DataFrame, col_x: str, col_grupo: str,
                  cores: dict, titulo: str,
                  label_y: str, x_title: str) -> go.Figure:
    fig = go.Figure()
    grupos = [g for g in cores if g in tab[col_grupo].unique()]
    for g in grupos:
        d = tab[tab[col_grupo] == g]
        fig.add_trace(go.Bar(
            x=d[col_x], y=d["n"], name=g,
            marker_color=cores[g],
            text=d["n"], textposition="outside", cliponaxis=False,
        ))
    fig.update_layout(
        title_text=titulo, barmode="group",
        xaxis=dict(title=x_title),
        yaxis=dict(title=label_y),
        **_LAYOUT,
    )
    return fig


def _proc(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por processo (incidente único)."""
    d = df.drop_duplicates("incidente").copy()
    d["tipo_questao"] = d["tipo_questao"].replace({"IJ": "QI"})
    return d


# ═══════════════════════════════════════════════════════════════════════════════
# T1 — Pizza geral por ambiente
# ═══════════════════════════════════════════════════════════════════════════════

def gt1_tramitacao(df: pd.DataFrame) -> go.Figure:
    serie = _proc(df)["tramitacao"].value_counts()
    return _pizza(
        serie,
        "Tramitação por Ambiente — Processos CC (2020–2025)",
        [CORES_TRAM.get(l, "#999") for l in serie.index],
    )


# ═══════════════════════════════════════════════════════════════════════════════
# T2 — Tramitação por classe (barras agrupadas)
# ═══════════════════════════════════════════════════════════════════════════════

def gt2_tram_por_classe(df: pd.DataFrame) -> go.Figure:
    proc = _proc(df)
    tab = proc.groupby(["classe", "tramitacao"]).size().reset_index(name="n")
    return _barras_grupo(
        tab, "classe", "tramitacao", CORES_TRAM,
        "Tramitação por Ambiente e Classe — Processos CC (2020–2025)",
        "Processos distintos", "Classe",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# T3 — Tramitação por tipo de questão (barras agrupadas)
# ═══════════════════════════════════════════════════════════════════════════════

def gt3_tram_por_tipo(df: pd.DataFrame) -> go.Figure:
    proc = _proc(df)
    proc = proc[proc["tipo_questao"].isin(_TIPOS)]
    tab = proc.groupby(["tipo_questao", "tramitacao"]).size().reset_index(name="n")
    return _barras_grupo(
        tab, "tipo_questao", "tramitacao", CORES_TRAM,
        "Tramitação por Ambiente e Tipo de Questão — Processos CC (2020–2025)",
        "Processos distintos", "Tipo de Questão",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# T4 — Processos em ambos os ambientes por tipo de questão
# ═══════════════════════════════════════════════════════════════════════════════

def gt4_ambos_por_tipo(df: pd.DataFrame) -> go.Figure:
    proc = _proc(df[df["tramitou_ambos"]])
    tab = proc["tipo_questao"].value_counts().reset_index()
    tab.columns = ["tipo_questao", "n"]
    tab = tab[tab["tipo_questao"].isin(_TIPOS)].sort_values("tipo_questao")
    fig = go.Figure()
    for _, row in tab.iterrows():
        fig.add_trace(go.Bar(
            x=[row["tipo_questao"]], y=[row["n"]],
            name=row["tipo_questao"],
            marker_color=CORES_TIPO.get(row["tipo_questao"], "#999"),
            text=[row["n"]], textposition="outside", cliponaxis=False,
        ))
    fig.update_layout(
        title_text="Processos em Ambos os Ambientes por Tipo de Questão (2020–2025)",
        barmode="group",
        xaxis=dict(title="Tipo de Questão"),
        yaxis=dict(title="Processos distintos"),
        **_LAYOUT,
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# T5 — Macro-desfecho por ambiente de tramitação (inclusões)
# ═══════════════════════════════════════════════════════════════════════════════

def gt5_macro_por_tram(df: pd.DataFrame) -> go.Figure:
    tab = df.groupby(["tramitacao", "macro_desfecho"]).size().reset_index(name="n")
    return _barras_grupo(
        tab, "tramitacao", "macro_desfecho", CORES_MACRO,
        "Macro-Desfecho por Ambiente de Tramitação — Inclusões (2020–2025)",
        "Inclusões em pauta", "Tramitação",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# T6 — Desfecho detalhado por ambiente de tramitação (inclusões)
# ═══════════════════════════════════════════════════════════════════════════════

def gt6_desfecho_por_tram(df: pd.DataFrame) -> go.Figure:
    tab = df.groupby(["tramitacao", "desfecho"]).size().reset_index(name="n")
    return _barras_grupo(
        tab, "tramitacao", "desfecho", CORES_DESFECHO,
        "Desfecho Detalhado por Ambiente de Tramitação — Inclusões (2020–2025)",
        "Inclusões em pauta", "Tramitação",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# T7 — Classe por ambiente de tramitação — pizza por ambiente (dict de figuras)
# ═══════════════════════════════════════════════════════════════════════════════

def gt7_classe_por_tram(df: pd.DataFrame) -> dict[str, go.Figure]:
    proc = _proc(df)
    result = {}
    for tram in _TRAMS:
        sub = proc[proc["tramitacao"] == tram]
        if sub.empty:
            continue
        serie = sub["classe"].value_counts()
        result[tram] = _pizza(
            serie,
            f"Distribuição por Classe — {tram} (2020–2025)",
            [CORES_CLASSE.get(l, "#999") for l in serie.index],
        )
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# T8 — Tipo de questão por ambiente de tramitação (dict de figuras)
# ═══════════════════════════════════════════════════════════════════════════════

def gt8_tipo_por_tram(df: pd.DataFrame) -> dict[str, go.Figure]:
    proc = _proc(df)
    proc = proc[proc["tipo_questao"].isin(_TIPOS)]
    result = {}
    for tram in _TRAMS:
        sub = proc[proc["tramitacao"] == tram]
        if sub.empty:
            continue
        serie = sub["tipo_questao"].value_counts()
        result[tram] = _pizza(
            serie,
            f"Distribuição por Tipo de Questão — {tram} (2020–2025)",
            [CORES_TIPO.get(l, "#999") for l in serie.index],
        )
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# T9 — Taxa de conclusão por ambiente de tramitação e classe
# ═══════════════════════════════════════════════════════════════════════════════

def gt9_taxa_conclusao(df: pd.DataFrame) -> go.Figure:
    tab = (
        df.groupby(["tramitacao", "classe"])["macro_desfecho"]
        .apply(lambda s: (s == "Concluído").mean() * 100)
        .reset_index(name="n")
    )
    tab["n"] = tab["n"].round(1)
    return _barras_grupo(
        tab, "tramitacao", "classe", CORES_CLASSE,
        "Taxa de Conclusão (%) por Ambiente de Tramitação e Classe (2020–2025)",
        "% de inclusões concluídas", "Tramitação",
    )
