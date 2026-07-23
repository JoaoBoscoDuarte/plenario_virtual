"""Figuras Plotly para a página de Tramitação por Ambiente."""

from __future__ import annotations
import plotly.graph_objects as go
import pandas as pd

from estilo import (
    aplicar_padrao, add_er_marker, add_espin_shade, br,
    AZUL, AZUL_CLARO, CINZA, VERDE, ROXO, VERMELHO,
)

CORES_TRAM = {
    "Ambos os ambientes": ROXO,
    "Virtual":            AZUL,   # PV
    "Físico":             CINZA,  # PP
}
CORES_AMBIENTE = {
    "Plenário Virtual":   AZUL,   # PV
    "Plenário Físico":    CINZA,  # PP
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
    "Não concluído": VERMELHO,
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
_TRAMS   = ["Virtual", "Físico", "Ambos os ambientes"]


# ── helpers ───────────────────────────────────────────────────────────────────

def _barras_grupo(tab: pd.DataFrame, col_x: str, col_grupo: str,
                  cores: dict, titulo: str, subtitulo: str,
                  label_y: str, x_title: str,
                  show_values: bool = True) -> go.Figure:
    fig = go.Figure()
    grupos = [g for g in cores if g in tab[col_grupo].unique()]
    for g in grupos:
        d = tab[tab[col_grupo] == g]
        fig.add_trace(go.Bar(
            x=d[col_x], y=d["n"], name=g.upper(),
            marker_color=cores[g],
            text=d["n"] if show_values else None,
            textposition="outside", cliponaxis=False,
            textfont=dict(family="Arial, sans-serif", size=17, color="black"),
        ))
    aplicar_padrao(
        fig, titulo, subtitulo,
        barmode="group",
        showlegend=True,
    )
    fig.update_xaxes(title_text=x_title)
    fig.update_yaxes(title_text=label_y)
    return fig


def _marcar_periodo_2020_2025(fig: go.Figure, y_max: float) -> None:
    """Aplica sombreamento ESPIN + marcador ER 53 num eixo x numérico de 'ano' (2020–2025)."""
    y_top = y_max * 1.2
    add_espin_shade(fig, ano_base=0, y0=0, y1=y_top, y_label=y_max * 1.12)
    add_er_marker(fig, ano_base=0, er=53, y0=0, y1=y_top, y_label=y_max * 1.02)


def _proc(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por processo (incidente único)."""
    d = df.drop_duplicates("incidente").copy()
    d["tipo_questao"] = d["tipo_questao"].replace({"IJ": "QI"})
    return d


# ═══════════════════════════════════════════════════════════════════════════════
# T1 — Pizza geral por ambiente
# ═══════════════════════════════════════════════════════════════════════════════

def gt1_tramitacao(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    serie = _proc(df)["tramitacao"].value_counts()
    ordem = [c for c in _TRAMS if c in serie.index]
    fig = go.Figure(go.Bar(
        x=[c.upper() for c in ordem], y=[serie[c] for c in ordem],
        marker_color=[CORES_TRAM[c] for c in ordem],
        text=[br(serie[c]) for c in ordem] if show_values else None,
        textposition="outside", cliponaxis=False,
        textfont=dict(family="Arial, sans-serif", size=20, color="black", weight="bold"),
    ))
    aplicar_padrao(
        fig,
        "Maioria dos processos tramita em apenas um ambiente",
        "Distribuição de processos distintos por ambiente de tramitação — CC (2020–2025)",
        xaxis=dict(title=""), yaxis=dict(title="Processos distintos"),
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# T2 — Tramitação por classe (barras agrupadas)
# ═══════════════════════════════════════════════════════════════════════════════

def gt2_tram_por_classe(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    proc = _proc(df)
    tab = proc.groupby(["classe", "tramitacao"], observed=True).size().reset_index(name="n")
    return _barras_grupo(
        tab, "classe", "tramitacao", CORES_TRAM,
        "Tramitação por ambiente varia conforme a classe processual",
        "Processos CC por classe e ambiente de tramitação (2020–2025)",
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
        "Tramitação por ambiente varia conforme o tipo de questão",
        "Processos CC por tipo de questão e ambiente de tramitação (2020–2025)",
        "Processos distintos", "Tipo de questão", show_values=show_values,
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
            name=row["tipo_questao"].upper(),
            marker_color=CORES_TIPO.get(row["tipo_questao"], "#999"),
            text=[row["n"]] if show_values else None,
            textposition="outside", cliponaxis=False,
            textfont=dict(family="Arial, sans-serif", size=17, color="black"),
        ))
    aplicar_padrao(
        fig,
        "Poucos processos tramitam em ambos os ambientes",
        "Processos que tramitaram em Plenário Virtual e Físico, por tipo de questão (2020–2025)",
        barmode="group",
        showlegend=True,
    )
    fig.update_xaxes(title_text="Tipo de questão")
    fig.update_yaxes(title_text="Processos distintos")
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# T5 — Macro-desfecho por ambiente de tramitação (inclusões)
# ═══════════════════════════════════════════════════════════════════════════════

def gt5_macro_por_tram(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    tab = df.groupby(["tramitacao", "macro_desfecho"], observed=True).size().reset_index(name="n")
    return _barras_grupo(
        tab, "tramitacao", "macro_desfecho", CORES_MACRO,
        "Taxa de conclusão varia entre ambientes de tramitação",
        "Macro-desfecho por ambiente de tramitação — Inclusões (2020–2025)",
        "Inclusões em pauta", "Tramitação", show_values=show_values,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# T6 — Desfecho detalhado por ambiente de tramitação (inclusões)
# ═══════════════════════════════════════════════════════════════════════════════

def gt6_desfecho_por_tram(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    tab = df.groupby(["tramitacao", "desfecho"], observed=True).size().reset_index(name="n")
    return _barras_grupo(
        tab, "tramitacao", "desfecho", CORES_DESFECHO,
        "Composição dos desfechos difere por ambiente de tramitação",
        "Desfecho detalhado por ambiente de tramitação — Inclusões (2020–2025)",
        "Inclusões em pauta", "Tramitação", show_values=show_values,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# T7 — Classe por ambiente de tramitação — pizza por ambiente (dict de figuras)
# ═══════════════════════════════════════════════════════════════════════════════

def gt7_classe_por_tram(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    proc = _proc(df)
    tab = proc.groupby(["tramitacao", "classe"], observed=True).size().reset_index(name="n")
    totais = tab.groupby("tramitacao")["n"].transform("sum")
    tab["pct"] = (tab["n"] / totais * 100).round(1)
    ordem = [t for t in _TRAMS if t in tab["tramitacao"].unique()]
    fig = go.Figure()
    for cls in _CLASSES:
        d = tab[tab["classe"] == cls]
        if d.empty:
            continue
        fig.add_trace(go.Bar(
            x=d["tramitacao"].str.upper(), y=d["pct"], name=cls.upper(),
            marker_color=CORES_CLASSE[cls],
            text=[f"{v:.0f}%" for v in d["pct"]] if show_values else None,
            textposition="inside",
            textfont=dict(family="Arial, sans-serif", size=14, color="white", weight="bold"),
            cliponaxis=False,
        ))
    aplicar_padrao(
        fig,
        "Composição por classe varia conforme o ambiente de tramitação",
        "Distribuição por classe processual, dentro de cada ambiente de tramitação (2020–2025)",
        barmode="stack", showlegend=True,
        xaxis=dict(title="", categoryorder="array", categoryarray=[t.upper() for t in ordem]),
        yaxis=dict(title="% de processos", range=[0, 100]),
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# T8 — Tipo de questão por ambiente de tramitação (dict de figuras)
# ═══════════════════════════════════════════════════════════════════════════════

def gt8_tipo_por_tram(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    proc = _proc(df)
    proc = proc[proc["tipo_questao"].isin(_TIPOS)]
    tab = proc.groupby(["tramitacao", "tipo_questao"], observed=True).size().reset_index(name="n")
    totais = tab.groupby("tramitacao")["n"].transform("sum")
    tab["pct"] = (tab["n"] / totais * 100).round(1)
    ordem = [t for t in _TRAMS if t in tab["tramitacao"].unique()]
    fig = go.Figure()
    for tipo in _TIPOS:
        d = tab[tab["tipo_questao"] == tipo]
        if d.empty:
            continue
        fig.add_trace(go.Bar(
            x=d["tramitacao"].str.upper(), y=d["pct"], name=tipo.upper(),
            marker_color=CORES_TIPO[tipo],
            text=[f"{v:.0f}%" for v in d["pct"]] if show_values else None,
            textposition="inside",
            textfont=dict(family="Arial, sans-serif", size=14, color="white", weight="bold"),
            cliponaxis=False,
        ))
    aplicar_padrao(
        fig,
        "Composição por tipo de questão varia conforme o ambiente de tramitação",
        "Distribuição por tipo de questão, dentro de cada ambiente de tramitação (2020–2025)",
        barmode="stack", showlegend=True,
        xaxis=dict(title="", categoryorder="array", categoryarray=[t.upper() for t in ordem]),
        yaxis=dict(title="% de processos", range=[0, 100]),
    )
    return fig


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
        "Taxa de conclusão por ambiente de tramitação, por classe",
        "% de inclusões concluídas por ambiente de tramitação e classe (2020–2025)",
        "% de inclusões concluídas", "Tramitação", show_values=show_values,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# T10 — Tabulador interativo
# ═══════════════════════════════════════════════════════════════════════════════

# Mapeamento legível das dimensões disponíveis
DIMENSOES: dict[str, str] = {
    "Ambiente de tramitação": "tramitacao",
    "Classe":                 "classe",
    "Tipo de questão":        "tipo_questao",
    "Ambiente (PV/PP)":       "ambiente",
    "Macro-desfecho":         "macro_desfecho",
    "Desfecho detalhado":     "desfecho",
    "Ano":                    "ano",
    "Reajuste de voto":       "teve_reajuste",
    "Sustentação oral":       "teve_sustentacao",
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
    "ambiente":      CORES_AMBIENTE,
    "teve_reajuste": {"Com reajuste": VERMELHO, "Sem reajuste": CINZA},
    "teve_sustentacao": {True: AZUL, False: CINZA},
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
    """Gráfico de barras reconfigurável: eixo X, grupo/cor e métrica livres.

    ponytail: eixo X é escolhido livremente pelo usuário (pode ou não ser "ano"),
    e quando é "ano" o eixo vira categórico (strings). Marcadores ER/ESPIN dependem
    de posição fracionária num eixo numérico contínuo, então não se aplicam aqui
    com segurança — sem marcadores neste gráfico dinâmico.
    """
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
            name=str(g).upper(),
            marker_color=cor,
            text=d_g["n"].apply(lambda v: f"{v:.1f}%" if barmode == "100%" else str(int(v))) if show_values else None,
            textposition="outside" if bm != "stack" else "inside",
            cliponaxis=False,
            textfont=dict(family="Arial, sans-serif", size=17, color="black"),
        ))

    # rótulos legíveis para título
    inv = {v: k for k, v in DIMENSOES.items()}
    titulo = f"{inv.get(eixo_x, eixo_x)} × {inv.get(grupo, grupo)}"
    subtitulo = (
        f"{'Processos' if metrica == 'processos' else 'Inclusões'} (2020–2025)"
    )

    aplicar_padrao(
        fig, titulo, subtitulo,
        barmode=bm,
        showlegend=True,
    )
    fig.update_xaxes(title_text=inv.get(eixo_x, eixo_x))
    fig.update_yaxes(title_text=label_y)
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
    fig = _barras_grupo(
        tab, "ano", "ambiente", CORES_AMBIENTE,
        "Volume de processos por ambiente muda ao longo dos anos",
        "Processos distintos por ano e ambiente (2020–2025)",
        "Processos (incidentes distintos)", "Ano", show_values=show_values,
    )
    fig.update_yaxes(range=[0, 800])
    _marcar_periodo_2020_2025(fig, y_max=800)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# T12 — Processos por tipo de tramitação, sem repetição
# ═══════════════════════════════════════════════════════════════════════════════

def _classificar_tramitacao(ambientes: set) -> str:
    tem_v = "Plenário Virtual" in ambientes
    tem_f = "Plenário Físico" in ambientes
    if tem_v and tem_f:
        return "Ambos os ambientes"
    return "Virtual" if tem_v else "Físico"


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
    y_max = float(tab.groupby("ano")["n"].sum().max() or 1)
    fig = _barras_grupo(
        tab, "ano", "tramitacao", CORES_TRAM,
        "Ambiente de primeira inclusão muda ao longo dos anos",
        "Processos por tipo de tramitação, por ano da primeira inclusão (2020–2025)",
        "Processos (incidentes distintos)", "Ano", show_values=show_values,
    )
    _marcar_periodo_2020_2025(fig, y_max=y_max)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# T13 — Processos por tipo de tramitação (período total, sem quebra anual)
# ═══════════════════════════════════════════════════════════════════════════════

CORES_TRAMITACAO = {
    "Virtual":            AZUL,
    "Presencial":         CINZA,
    "Ambos os ambientes": VERDE,
}


def _classificar_tramitacao_t13(ambientes: set) -> str:
    tem_v = "Plenário Virtual" in ambientes
    tem_p = "Plenário Presencial" in ambientes
    if tem_v and tem_p:
        return "Ambos os ambientes"
    return "Virtual" if tem_v else "Presencial"


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
    ord_tram = ["Virtual", "Presencial", "Ambos os ambientes"]
    for tr in ord_tram:
        d = tab[tab["tramitacao"] == tr]
        fig.add_trace(go.Bar(
            x=d["periodo"], y=d["n"], name=tr.upper(),
            marker_color=CORES_TRAMITACAO[tr],
            text=d["n"] if show_values else None,
            textposition="outside", cliponaxis=False,
            textfont=dict(family="Arial, sans-serif", size=17, color="black"),
        ))
    aplicar_padrao(
        fig,
        "Maioria dos processos tramita em um único ambiente no período",
        "Processos por tipo de tramitação (2020–2025)",
        barmode="group",
        showlegend=True,
        height=600,
        margin=dict(t=120, b=80, l=60, r=60),
    )
    fig.update_xaxes(title_text="Período")
    fig.update_yaxes(title_text="Processos (incidentes distintos)")
    return fig
