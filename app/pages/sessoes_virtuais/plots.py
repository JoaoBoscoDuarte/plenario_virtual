"""Figuras Plotly para a página de Sessões Virtuais."""

from __future__ import annotations
import plotly.graph_objects as go
import pandas as pd

from estilo import aplicar_padrao, add_er_marker, add_espin_shade, AZUL, VERDE

COR_SESSAO = AZUL
CORES_CLASSE = {
    "ADI":  AZUL,
    "ADPF": "#f59e0b",
    "ADC":  VERDE,
    "ADO":  "#ef4444",
}
CORES_TIPO = {"PR": AZUL, "RC": "#f59e0b", "QI": VERDE}
CORES_MACRO = {"Concluído": VERDE, "Não concluído": "#ef4444"}
_CLASSES = ["ADI", "ADPF", "ADC", "ADO"]
_TIPOS = ["PR", "RC", "QI"]
_ANOS = list(range(2020, 2026))

# ── helpers ───────────────────────────────────────────────────────────────────

def _faixa_sessoes(n: int) -> str:
    if n == 1: return "1 sessão"
    if n <= 3: return "2–3 sessões"
    if n <= 5: return "4–5 sessões"
    return "6+ sessões"

ORDEM_FAIXA = ["1 sessão", "2–3 sessões", "4–5 sessões", "6+ sessões"]

# ═══════════════════════════════════════════════════════════════════════════════
# G0 — Sessões vs Inclusões em pauta (PV)
# ═══════════════════════════════════════════════════════════════════════════════

def g0_sessoes_vs_inclusoes(df_s: pd.DataFrame, df_final: pd.DataFrame,
                              show_values: bool = True) -> go.Figure:
    """Sessões virtuais vs inclusões em pauta (PV) por ano."""
    sessoes = df_s.groupby("ano").size().reset_index(name="Sessões virtuais")
    df_pv = df_final[df_final["ambiente"] == "Plenário Virtual"].copy()
    if df_pv.empty:
        df_pv = df_final[df_final["ambiente"] == "Plenário Virtual"]
    inclusoes = df_pv.groupby("ano").size().reset_index(name="Inclusões em pauta (PV)")
    tab = sessoes.merge(inclusoes, on="ano", how="outer").fillna(0)
    tab = tab.set_index("ano").reindex(_ANOS, fill_value=0).reset_index()
    tab["ano_str"] = tab["ano"].astype(str)
    fig = go.Figure()
    for col, cor in [("Sessões virtuais", AZUL), ("Inclusões em pauta (PV)", VERDE)]:
        vals = tab[col].astype(int)
        fig.add_trace(go.Bar(
            x=tab["ano_str"], y=vals, name=col,
            marker_color=cor,
            text=vals if show_values else None,
            textposition="outside", cliponaxis=False,
            textfont=dict(family="Arial, sans-serif", size=17, color="black"),
        ))
    aplicar_padrao(
        fig,
        "Sessões virtuais vs Inclusões em pauta (PV) por ano",
        "Comparação anual entre sessões virtuais iniciadas e inclusões em pauta — 2020–2025",
        barmode="group", showlegend=True,
        xaxis=dict(title="Ano"),
        yaxis=dict(title="Quantidade"),
    )
    ymax = float(tab[["Sessões virtuais", "Inclusões em pauta (PV)"]].to_numpy().max()) * 1.15 + 1
    add_espin_shade(fig, _ANOS[0], y0=0, y1=ymax, y_label=ymax * 0.97)
    add_er_marker(fig, _ANOS[0], 53, y0=0, y1=ymax, y_label=ymax * 0.85)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# BLOCO 3 — Múltiplas sessões por processo
# ═══════════════════════════════════════════════════════════════════════════════

def _prep_sessoes_por_processo(df_s: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Retorna (sess_por_proc, df_s_ord)."""
    spp = df_s.groupby("incidente").size().reset_index(name="n_sessoes")
    spp = spp.merge(
        df_s[["incidente", "classe", "tipo_questao", "macro_desfecho"]].drop_duplicates("incidente"),
        on="incidente", how="left",
    )
    spp["faixa"] = spp["n_sessoes"].apply(_faixa_sessoes)

    df_ord = df_s.sort_values(["incidente", "data_sessao_dt"]).copy()
    df_ord["n_sessao"] = df_ord.groupby("incidente").cumcount() + 1
    return spp, df_ord


def g3_1_distribuicao_sessoes(df_s: pd.DataFrame, show_values: bool = True) -> go.Figure:
    spp, _ = _prep_sessoes_por_processo(df_s)
    tab = spp["faixa"].value_counts().reindex(ORDEM_FAIXA)
    fig = go.Figure(go.Bar(
        x=tab.index, y=tab.values,
        marker_color=COR_SESSAO,
        text=tab.values if show_values else None,
        textposition="outside", cliponaxis=False,
        textfont=dict(family="Arial, sans-serif", size=17, color="black"),
    ))
    aplicar_padrao(
        fig,
        "Distribuição de sessões por processo",
        "Nº de sessões virtuais necessárias por processo — 2020–2025",
        xaxis=dict(title="Nº de sessões por processo"),
        yaxis=dict(title="Nº de processos"),
    )
    return fig


def g3_2_faixa_sessoes_classe(df_s: pd.DataFrame, show_values: bool = True) -> go.Figure:
    spp, _ = _prep_sessoes_por_processo(df_s)
    tab = spp.groupby(["classe", "faixa"]).size().reset_index(name="n")
    fig = go.Figure()
    for faixa in ORDEM_FAIXA:
        d = tab[tab["faixa"] == faixa]
        fig.add_trace(go.Bar(
            x=d["classe"], y=d["n"], name=faixa,
            marker_color=COR_SESSAO if faixa == ORDEM_FAIXA[0] else None,
            text=d["n"] if show_values else None,
            textposition="inside",
            textfont=dict(family="Arial, sans-serif", size=16, color="white"),
        ))
    cores_faixa = {"1 sessão": "#2563eb", "2–3 sessões": "#f59e0b",
                   "4–5 sessões": "#16a34a", "6+ sessões": "#ef4444"}
    for i, faixa in enumerate(ORDEM_FAIXA):
        d = tab[tab["faixa"] == faixa]
        if d.empty:
            continue
        fig.data[i].marker.color = cores_faixa[faixa]
    aplicar_padrao(
        fig,
        "Número de sessões por processo e classe",
        "Distribuição por faixa de nº de sessões — 2020–2025",
        barmode="stack", showlegend=True,
        xaxis=dict(title="Classe"),
        yaxis=dict(title="Nº de processos"),
    )
    return fig


def g3_3_taxa_conclusao_primeira(df_s: pd.DataFrame, show_values: bool = True) -> go.Figure:
    _, df_ord = _prep_sessoes_por_processo(df_s)
    df_ord["posicao"] = df_ord["n_sessao"].apply(
        lambda n: "1ª sessão" if n == 1 else "Sessões posteriores"
    )
    tab = df_ord.groupby("posicao")["macro_desfecho"].apply(
        lambda x: round(100 * (x == "Concluído").mean(), 1)
    )
    ORDEM_POS = ["1ª sessão", "Sessões posteriores"]
    tab = tab.reindex(ORDEM_POS)
    fig = go.Figure(go.Bar(
        x=tab.index, y=tab.values,
        marker_color=[COR_SESSAO, "#94a3b8"],
        text=[f"{v}%" for v in tab.values] if show_values else None,
        textposition="outside", cliponaxis=False,
        textfont=dict(family="Arial, sans-serif", size=17, color="black"),
    ))
    aplicar_padrao(
        fig,
        "Taxa de conclusão: 1ª sessão vs sessões posteriores",
        "Percentual de sessões concluídas por posição — 2020–2025",
        xaxis=dict(title=""),
        yaxis=dict(title="% Concluído", range=[0, 105]),
    )
    return fig


def g3_4_taxa_conclusao_posicao(df_s: pd.DataFrame, show_values: bool = True) -> go.Figure:
    _, df_ord = _prep_sessoes_por_processo(df_s)

    def pos_label(n: int) -> str:
        if n <= 3: return f"{n}ª sessão"
        return "4ª+ sessão"

    ORDEM = ["1ª sessão", "2ª sessão", "3ª sessão", "4ª+ sessão"]
    df_ord["posicao_n"] = df_ord["n_sessao"].apply(pos_label)
    tab = df_ord.groupby("posicao_n")["macro_desfecho"].apply(
        lambda x: round(100 * (x == "Concluído").mean(), 1)
    ).reindex(ORDEM)
    fig = go.Figure(go.Bar(
        x=tab.index, y=tab.values,
        marker_color=COR_SESSAO,
        text=[f"{v}%" for v in tab.values] if show_values else None,
        textposition="outside", cliponaxis=False,
        textfont=dict(family="Arial, sans-serif", size=17, color="black"),
    ))
    aplicar_padrao(
        fig,
        "Taxa de conclusão por posição da sessão no processo",
        "Percentual concluído em cada posição — 2020–2025",
        xaxis=dict(title=""),
        yaxis=dict(title="% Concluído", range=[0, 105]),
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# BLOCO 4 — Cruzamentos
# ═══════════════════════════════════════════════════════════════════════════════

def g4_2_sessoes_classe_tipo(df_s: pd.DataFrame, show_values: bool = True) -> go.Figure:
    tab = df_s.groupby(["classe", "tipo_questao"]).size().reset_index(name="n")
    fig = go.Figure()
    for tp in _TIPOS:
        d = tab[tab["tipo_questao"] == tp]
        fig.add_trace(go.Bar(
            x=d["classe"], y=d["n"], name=tp,
            marker_color=CORES_TIPO[tp],
            text=d["n"] if show_values else None,
            textposition="outside", cliponaxis=False,
            textfont=dict(family="Arial, sans-serif", size=17, color="black"),
        ))
    aplicar_padrao(
        fig,
        "Sessões por classe e tipo de questão",
        "Volume de sessões virtuais — 2020–2025",
        barmode="group", showlegend=True,
        xaxis=dict(title="Classe"),
        yaxis=dict(title="Nº de sessões"),
    )
    return fig


def _barras_macro_ano(df_sub: pd.DataFrame, titulo: str,
                      show_values: bool = True) -> go.Figure:
    tab = df_sub.groupby(["ano", "macro_desfecho"]).size().reset_index(name="n")
    fig = go.Figure()
    for desf in ["Concluído", "Não concluído"]:
        d = tab[tab["macro_desfecho"] == desf]
        fig.add_trace(go.Bar(
            x=d["ano"].astype(str), y=d["n"], name=desf,
            marker_color=CORES_MACRO[desf],
            text=d["n"] if show_values else None,
            textposition="inside",
            textfont=dict(family="Arial, sans-serif", size=16, color="white"),
        ))
    aplicar_padrao(
        fig, titulo, "Nº de sessões concluídas vs não concluídas por ano",
        barmode="stack", showlegend=True,
        xaxis=dict(title="Ano"),
        yaxis=dict(title="Nº de sessões"),
    )
    anos_presentes = sorted(df_sub["ano"].dropna().unique().tolist())
    if anos_presentes:
        ano_base = int(min(anos_presentes))
        ymax = float(tab.groupby("ano")["n"].sum().max()) * 1.15 + 1
        add_espin_shade(fig, ano_base, y0=0, y1=ymax, y_label=ymax * 0.97)
        add_er_marker(fig, ano_base, 53, y0=0, y1=ymax, y_label=ymax * 0.85)
    return fig


def g4_3_macro_ano_tipo(df_s: pd.DataFrame, show_values: bool = True) -> dict[str, go.Figure]:
    figs = {}
    for tp in _TIPOS:
        sub = df_s[df_s["tipo_questao"] == tp]
        titulo = f"Macro-desfecho por ano — {tp} — Sessões virtuais (2020–2025)"
        figs[tp] = _barras_macro_ano(sub, titulo, show_values)
    return figs


def g4_4_macro_ano_classe(df_s: pd.DataFrame, show_values: bool = True) -> dict[str, go.Figure]:
    figs = {}
    for cl in ["ADI", "ADPF"]:
        sub = df_s[df_s["classe"] == cl]
        titulo = f"Macro-desfecho por ano — {cl} — Sessões virtuais (2020–2025)"
        figs[cl] = _barras_macro_ano(sub, titulo, show_values)
    return figs


def g4_5_taxa_conclusao_classe_tipo(df_s: pd.DataFrame, show_values: bool = True) -> go.Figure:
    tab = df_s.groupby(["classe", "tipo_questao"])["macro_desfecho"].apply(
        lambda x: round(100 * (x == "Concluído").mean(), 1)
    ).reset_index(name="n")
    fig = go.Figure()
    for tp in _TIPOS:
        d = tab[tab["tipo_questao"] == tp]
        fig.add_trace(go.Bar(
            x=d["classe"], y=d["n"], name=tp,
            marker_color=CORES_TIPO[tp],
            text=[f"{v}%" for v in d["n"]] if show_values else None,
            textposition="outside", cliponaxis=False,
            textfont=dict(family="Arial, sans-serif", size=17, color="black"),
        ))
    aplicar_padrao(
        fig,
        "Taxa de conclusão por classe e tipo de questão",
        "Sessões virtuais — 2020–2025",
        barmode="group", showlegend=True,
        xaxis=dict(title="Classe"),
        yaxis=dict(title="% Concluído", range=[0, 105]),
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# BLOCO 5 — Duração até conclusão
# ═══════════════════════════════════════════════════════════════════════════════

def _faixa_duracao(d: int) -> str:
    if d <= 30:   return "≤ 30 dias"
    if d <= 90:   return "31–90 dias"
    if d <= 180:  return "91–180 dias"
    if d <= 365:  return "6–12 meses"
    if d <= 730:  return "1–2 anos"
    return "> 2 anos"

ORDEM_DUR = ["≤ 30 dias", "31–90 dias", "91–180 dias",
             "6–12 meses", "1–2 anos", "> 2 anos"]


def prep_duracao(df_s: pd.DataFrame, df_final: pd.DataFrame,
                 ambiente: str = "Plenário Virtual") -> pd.DataFrame:
    """Prepara dataframe de duração para Block 5."""
    df_filt = df_final[df_final["ambiente"] == ambiente].copy()
    primeira_pauta = (
        df_filt.groupby("incidente")["data_inclusao_dt"]
        .min().reset_index(name="primeira_pauta_dt")
    )
    conc = (
        df_s[df_s["macro_desfecho"] == "Concluído"]
        .sort_values("data_sessao_dt")
        .groupby("incidente").last()
        .reset_index()[["incidente", "data_sessao_dt", "classe", "tipo_questao"]]
    )
    dur = conc.merge(primeira_pauta, on="incidente", how="left")
    dur["dias"] = (dur["data_sessao_dt"] - dur["primeira_pauta_dt"]).dt.days
    dur = dur[dur["dias"] >= 0].copy()
    dur["faixa_dur"] = dur["dias"].apply(_faixa_duracao)
    return dur


def g5_1_distribuicao_duracao(duracao: pd.DataFrame, show_values: bool = True) -> go.Figure:
    tab = duracao["faixa_dur"].value_counts().reindex(ORDEM_DUR)
    fig = go.Figure(go.Bar(
        x=tab.index, y=tab.values,
        marker_color=COR_SESSAO,
        text=tab.values if show_values else None,
        textposition="outside", cliponaxis=False,
        textfont=dict(family="Arial, sans-serif", size=17, color="black"),
    ))
    aplicar_padrao(
        fig,
        "Tempo até conclusão",
        "Processos virtuais — 2020–2025",
        xaxis=dict(title="Duração"),
        yaxis=dict(title="Nº de processos concluídos"),
    )
    return fig


def g5_2_duracao_mediana_classe(duracao: pd.DataFrame, show_values: bool = True) -> go.Figure:
    tab = duracao.groupby("classe")["dias"].median().round(0).astype(int)
    fig = go.Figure(go.Bar(
        x=tab.index, y=tab.values,
        marker_color=COR_SESSAO,
        text=tab.values if show_values else None,
        textposition="outside", cliponaxis=False,
        textfont=dict(family="Arial, sans-serif", size=17, color="black"),
    ))
    aplicar_padrao(
        fig,
        "Tempo mediano até conclusão por classe",
        "Dias — 2020–2025",
        xaxis=dict(title="Classe"),
        yaxis=dict(title="Dias (mediana)"),
    )
    return fig


def g5_3_duracao_mediana_tipo(duracao: pd.DataFrame, show_values: bool = True) -> go.Figure:
    tab = duracao.groupby("tipo_questao")["dias"].median().round(0).astype(int)
    fig = go.Figure(go.Bar(
        x=tab.index, y=tab.values,
        marker_color=COR_SESSAO,
        text=tab.values if show_values else None,
        textposition="outside", cliponaxis=False,
        textfont=dict(family="Arial, sans-serif", size=17, color="black"),
    ))
    aplicar_padrao(
        fig,
        "Tempo mediano até conclusão por tipo de questão",
        "Dias — 2020–2025",
        xaxis=dict(title="Tipo de questão"),
        yaxis=dict(title="Dias (mediana)"),
    )
    return fig
