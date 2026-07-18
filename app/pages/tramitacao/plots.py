"""Figuras Plotly para a página de Tramitação por Ambiente."""

from __future__ import annotations
import plotly.graph_objects as go
import pandas as pd

CORES_TRAM = {
    "Ambos os ambientes": "#8b5cf6",
    "Só Virtual":         "#2563eb",
    "Só Físico":          "#f59e0b",
}
CORES_AMBIENTE = {
    "Plenário Virtual":   "#2563eb",
    "Plenário Físico":    "#f59e0b",
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
                  label_y: str, x_title: str,
                  show_values: bool = True) -> go.Figure:
    fig = go.Figure()
    grupos = [g for g in cores if g in tab[col_grupo].unique()]
    for g in grupos:
        d = tab[tab[col_grupo] == g]
        fig.add_trace(go.Bar(
            x=d[col_x], y=d["n"], name=g,
            marker_color=cores[g],
            text=d["n"] if show_values else None,
            textposition="outside", cliponaxis=False,
        ))
    fig.update_layout(
        title_text=titulo, barmode="group",
        xaxis=dict(title=x_title),
        yaxis=dict(title=label_y),
        **_LAYOUT,
    )
    return fig


def _barras_com_total(tab: pd.DataFrame, total: pd.DataFrame,
                      col_x: str, col_grupo: str,
                      cores: dict, titulo: str, label_y: str,
                      show_values: bool = True,
                      y_max: int | None = None) -> go.Figure:
    from plotly.subplots import make_subplots
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    grupos = [g for g in cores if g in tab[col_grupo].unique()]
    for g in grupos:
        d = tab[tab[col_grupo] == g]
        fig.add_trace(go.Bar(
            x=d[col_x], y=d["n"], name=g,
            marker_color=cores[g],
            text=d["n"] if show_values else None,
            textposition="outside", cliponaxis=False,
        ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=total[col_x], y=total["n"], name="Total",
        mode="lines+markers", line=dict(color="#333", width=2),
        marker=dict(size=6),
    ), secondary_y=True)
    fig.update_layout(
        title_text=titulo, barmode="group",
        xaxis=dict(title=col_x.capitalize()),
        yaxis=dict(title=label_y),
        yaxis2=dict(title="Total", overlaying="y", side="right"),
        **_LAYOUT,
    )
    if y_max:
        fig.update_yaxes(range=[0, y_max])
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

def gt2_tram_por_classe(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    proc = _proc(df)
    tab = proc.groupby(["classe", "tramitacao"], observed=True).size().reset_index(name="n")
    return _barras_grupo(
        tab, "classe", "tramitacao", CORES_TRAM,
        "Tramitação por Ambiente e Classe — Processos CC (2020–2025)",
        "Processos distintos", "Classe", show_values=show_values,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# T3 — Tramitação por tipo de questão (barras agrupadas)
# ═══════════════════════════════════════════════════════════════════════════════

def gt3_tram_por_tipo(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    proc = _proc(df)
    proc = proc[proc["tipo_questao"].isin(_TIPOS)]
    tab = proc.groupby(["tipo_questao", "tramitacao"], observed=True).size().reset_index(name="n")
    return _barras_grupo(
        tab, "tipo_questao", "tramitacao", CORES_TRAM,
        "Tramitação por Ambiente e Tipo de Questão — Processos CC (2020–2025)",
        "Processos distintos", "Tipo de Questão", show_values=show_values,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# T4 — Processos em ambos os ambientes por tipo de questão
# ═══════════════════════════════════════════════════════════════════════════════

def gt4_ambos_por_tipo(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
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
            text=[row["n"]] if show_values else None,
            textposition="outside", cliponaxis=False,
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

def gt5_macro_por_tram(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    tab = df.groupby(["tramitacao", "macro_desfecho"], observed=True).size().reset_index(name="n")
    return _barras_grupo(
        tab, "tramitacao", "macro_desfecho", CORES_MACRO,
        "Macro-Desfecho por Ambiente de Tramitação — Inclusões (2020–2025)",
        "Inclusões em pauta", "Tramitação", show_values=show_values,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# T6 — Desfecho detalhado por ambiente de tramitação (inclusões)
# ═══════════════════════════════════════════════════════════════════════════════

def gt6_desfecho_por_tram(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    tab = df.groupby(["tramitacao", "desfecho"], observed=True).size().reset_index(name="n")
    return _barras_grupo(
        tab, "tramitacao", "desfecho", CORES_DESFECHO,
        "Desfecho Detalhado por Ambiente de Tramitação — Inclusões (2020–2025)",
        "Inclusões em pauta", "Tramitação", show_values=show_values,
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

def gt9_taxa_conclusao(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    tab = (
        df.groupby(["tramitacao", "classe"], observed=True)["macro_desfecho"]
        .apply(lambda s: (s == "Concluído").mean() * 100)
        .reset_index(name="n")
    )
    tab["n"] = tab["n"].round(1)
    tab = tab[tab["n"] > 0]
    return _barras_grupo(
        tab, "tramitacao", "classe", CORES_CLASSE,
        "Taxa de Conclusão (%) por Ambiente de Tramitação e Classe (2020–2025)",
        "% de inclusões concluídas", "Tramitação", show_values=show_values,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# T10 — Tabulador interativo
# ═══════════════════════════════════════════════════════════════════════════════

# Mapeamento legível das dimensões disponíveis
DIMENSOES: dict[str, str] = {
    "Ambiente de Tramitação": "tramitacao",
    "Classe":                 "classe",
    "Tipo de Questão":        "tipo_questao",
    "Ambiente (PV/PP)":       "ambiente",
    "Macro-Desfecho":         "macro_desfecho",
    "Desfecho Detalhado":     "desfecho",
    "Ano":                    "ano",
    "Reajuste de Voto":       "teve_reajuste",
    "Sustentação Oral":       "teve_sustentacao",
}

# Paleta de fallback para dimensões sem cor definida
_PALETA_FALLBACK = [
    "#2563eb", "#f59e0b", "#16a34a", "#ef4444",
    "#8b5cf6", "#ec4899", "#f97316", "#9ca3af",
    "#0ea5e9", "#84cc16",
]

_CORES_POR_COLUNA: dict[str, dict] = {
    "tramitacao":    CORES_TRAM,
    "classe":        CORES_CLASSE,
    "tipo_questao":  CORES_TIPO,
    "macro_desfecho": CORES_MACRO,
    "desfecho":      CORES_DESFECHO,
    "ambiente":      {"Plenário Virtual": "#2563eb", "Plenário Presencial": "#f59e0b"},
    "teve_reajuste": {"Com reajuste": "#ef4444", "Sem reajuste": "#9ca3af"},
    "teve_sustentacao": {True: "#2563eb", False: "#9ca3af"},
}


def _cores_para(coluna: str, valores: list) -> list[str]:
    mapa = _CORES_POR_COLUNA.get(coluna, {})
    return [mapa.get(v, _PALETA_FALLBACK[i % len(_PALETA_FALLBACK)])
            for i, v in enumerate(valores)]


def gt10_tabulador(
    df: pd.DataFrame,
    eixo_x: str,
    grupo: str,
    metrica: str = "inclusoes",
    barmode: str = "group",
    show_values: bool = True,
) -> go.Figure:
    """Gráfico de barras reconfigurável: eixo X, grupo/cor e métrica livres."""
    d = df.copy()
    d["tipo_questao"] = d["tipo_questao"].replace({"IJ": "QI"})
    if "teve_reajuste" in (eixo_x, grupo):
        d["teve_reajuste"] = d["teve_reajuste"].map(
            {True: "Com reajuste", False: "Sem reajuste"}
        )

    if metrica == "processos":
        d = d.drop_duplicates("incidente")
        label_y = "Processos distintos"
    else:
        label_y = "Inclusões em pauta"

    tab = d.groupby([eixo_x, grupo], observed=True).size().reset_index(name="n")

    if barmode == "100%":
        totais = tab.groupby(eixo_x)["n"].transform("sum")
        tab["n"] = (tab["n"] / totais * 100).round(1)
        label_y = "% do total"
        bm = "stack"
    else:
        bm = barmode

    grupos = tab[grupo].unique().tolist()
    cores = _cores_para(grupo, grupos)

    fig = go.Figure()
    for g, cor in zip(grupos, cores):
        d_g = tab[tab[grupo] == g]
        fig.add_trace(go.Bar(
            x=d_g[eixo_x].astype(str),
            y=d_g["n"],
            name=str(g),
            marker_color=cor,
            text=d_g["n"].apply(lambda v: f"{v:.1f}%" if barmode == "100%" else str(int(v))) if show_values else None,
            textposition="outside" if bm != "stack" else "inside",
            cliponaxis=False,
        ))

    # rótulos legíveis para título
    inv = {v: k for k, v in DIMENSOES.items()}
    titulo = (
        f"{inv.get(eixo_x, eixo_x)} × {inv.get(grupo, grupo)} "
        f"({'processos' if metrica == 'processos' else 'inclusões'}) — 2020–2025"
    )

    fig.update_layout(
        title_text=titulo,
        barmode=bm,
        xaxis=dict(title=inv.get(eixo_x, eixo_x)),
        yaxis=dict(title=label_y),
        **_LAYOUT,
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# T11 — Processos distintos por ano e ambiente
# ═══════════════════════════════════════════════════════════════════════════════

def gt11_proc_ano_ambiente(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    """Processos distintos por ano e ambiente (drop_duplicates incidente+ano+ambiente)."""
    d = df.copy()
    d["ambiente"] = d["ambiente"].replace({"Plenário Presencial": "Plenário Físico"})
    tab = (
        d.drop_duplicates(subset=["incidente", "ano", "ambiente"])
        .groupby(["ano", "ambiente"], observed=True).size()
        .reset_index(name="n")
    )
    total = (
        d.drop_duplicates(subset=["incidente", "ano"])
        .groupby("ano", observed=True).size()
        .reset_index(name="n")
    )
    return _barras_com_total(
        tab, total, "ano", "ambiente", CORES_AMBIENTE,
        "Processos distintos por ano e ambiente (2020–2025)",
        "Processos (incidentes distintos)",
        show_values=show_values, y_max=800,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# T12 — Processos por tipo de tramitação, sem repetição
# ═══════════════════════════════════════════════════════════════════════════════

def _classificar_tramitacao(ambientes: set) -> str:
    tem_v = "Plenário Virtual" in ambientes
    tem_f = "Plenário Físico" in ambientes
    if tem_v and tem_f:
        return "Ambos os ambientes"
    return "Só Virtual" if tem_v else "Só Físico"


def gt12_proc_tramitacao_primeiro_ano(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    """Cada processo UMA vez: ano = primeira inclusão, tipo = histórico completo."""
    d = df.copy()
    d["ambiente"] = d["ambiente"].replace({"Plenário Presencial": "Plenário Físico"})
    proc = (
        d.groupby("incidente")
        .agg(
            ambientes=("ambiente", set),
            ano_primeira=("data_inclusao_dt", "min"),
        )
        .reset_index()
    )
    proc["tramitacao"] = proc["ambientes"].apply(_classificar_tramitacao)
    proc["ano"] = proc["ano_primeira"].dt.year
    tab = proc.groupby(["ano", "tramitacao"], observed=True).size().reset_index(name="n")
    total = proc.groupby("ano", observed=True).size().reset_index(name="n")
    return _barras_com_total(
        tab, total, "ano", "tramitacao", CORES_TRAM,
        "Processos por tipo de tramitação, por ano sem repetição (2020–2025)",
        "Processos (incidentes distintos)",
        show_values=show_values,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# T13 — Processos por tipo de tramitação (período total, sem quebra anual)
# ═══════════════════════════════════════════════════════════════════════════════

CORES_TRAMITACAO = {
    "Só Virtual":         "#2563eb",
    "Só Presencial":      "#f59e0b",
    "Ambos os ambientes": "#16a34a",
}


def _classificar_tramitacao_t13(ambientes: set) -> str:
    tem_v = "Plenário Virtual" in ambientes
    tem_p = "Plenário Presencial" in ambientes
    if tem_v and tem_p:
        return "Ambos os ambientes"
    return "Só Virtual" if tem_v else "Só Presencial"


def gt13_tramitacao_periodo(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    proc = (
        df.groupby("incidente")["ambiente"]
        .apply(set)
        .reset_index(name="ambientes")
    )
    proc["tramitacao"] = proc["ambientes"].apply(_classificar_tramitacao_t13)
    proc["periodo"] = "2020–2025"

    tab = proc.groupby(["periodo", "tramitacao"], observed=True).size().reset_index(name="n")

    fig = go.Figure()
    ord_tram = ["Só Virtual", "Só Presencial", "Ambos os ambientes"]
    for tr in ord_tram:
        d = tab[tab["tramitacao"] == tr]
        fig.add_trace(go.Bar(
            x=d["periodo"], y=d["n"], name=tr,
            marker_color=CORES_TRAMITACAO[tr],
            text=d["n"] if show_values else None,
            textposition="outside", cliponaxis=False,
            textfont=dict(family="Arial, sans-serif", size=15, color="black"),
        ))
    fig.update_layout(
        title=dict(text="Processos por tipo de tramitação — 2020–2025",
                   font=dict(family="Arial, sans-serif", size=22, color="black")),
        barmode="group",
        xaxis=dict(title=dict(text="Período", font=dict(family="Arial, sans-serif", size=16, color="black")),
                   tickfont=dict(family="Arial, sans-serif", size=15, color="black")),
        yaxis=dict(title=dict(text="Processos (incidentes distintos)", font=dict(family="Arial, sans-serif", size=16, color="black")),
                   tickfont=dict(family="Arial, sans-serif", size=15, color="black")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                    font=dict(family="Arial, sans-serif", size=15, color="black")),
        template="plotly_white", height=500,
        margin=dict(t=120, b=80, l=60, r=60),
    )
    return fig
