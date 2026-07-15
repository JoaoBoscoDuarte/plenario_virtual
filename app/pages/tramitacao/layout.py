"""Renderização da página de Tramitação por Ambiente."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import (
    gt1_tramitacao,
    gt2_tram_por_classe,
    gt3_tram_por_tipo,
    gt4_ambos_por_tipo,
    gt5_macro_por_tram,
    gt6_desfecho_por_tram,
    gt7_classe_por_tram,
    gt8_tipo_por_tram,
    gt9_taxa_conclusao,
    gt10_tabulador,
    DIMENSOES,
)

# ── Catálogo T1–T9 ────────────────────────────────────────────────────────────
# (label_seletor, subtítulo, descrição, função, unidade)
_CATALOGO = [
    (
        "T1 — Tramitação por Ambiente (pizza geral)",
        "Tramitação por Ambiente — Processos CC (2020–2025)",
        "Pizza com a distribuição dos processos distintos por ambiente: "
        "só PV, só PP ou ambos.",
        gt1_tramitacao,
        "processo (incidente único)",
    ),
    (
        "T2 — Tramitação por Ambiente e Classe",
        "Tramitação por Ambiente e Classe — Processos CC (2020–2025)",
        "Barras agrupadas por ambiente de tramitação (só PV / só PP / ambos) "
        "para cada classe processual (ADI, ADPF, ADC, ADO).",
        gt2_tram_por_classe,
        "processo (incidente único)",
    ),
    (
        "T3 — Tramitação por Ambiente e Tipo de Questão",
        "Tramitação por Ambiente e Tipo de Questão — Processos CC (2020–2025)",
        "Barras agrupadas por ambiente de tramitação para cada tipo de questão "
        "(PR / RC / QI). IJ renomeado para QI.",
        gt3_tram_por_tipo,
        "processo (incidente único)",
    ),
    (
        "T4 — Processos em Ambos os Ambientes por Tipo de Questão",
        "Processos em Ambos os Ambientes por Tipo de Questão (2020–2025)",
        "Recorte dos processos que tramitaram em ambos os ambientes, "
        "distribuídos por tipo de questão (PR / RC / QI).",
        gt4_ambos_por_tipo,
        "processo (incidente único)",
    ),
    (
        "T5 — Macro-Desfecho por Ambiente de Tramitação",
        "Macro-Desfecho por Ambiente de Tramitação — Inclusões (2020–2025)",
        "Volume de inclusões concluídas e não concluídas em cada "
        "grupo de tramitação (só PV / só PP / ambos).",
        gt5_macro_por_tram,
        "inclusão em pauta",
    ),
    (
        "T6 — Desfecho Detalhado por Ambiente de Tramitação",
        "Desfecho Detalhado por Ambiente de Tramitação — Inclusões (2020–2025)",
        "Os 7 desfechos detalhados (unânime, maioria, pedido de vista etc.) "
        "para cada grupo de tramitação.",
        gt6_desfecho_por_tram,
        "inclusão em pauta",
    ),
    (
        "T7 — Distribuição por Classe dentro de cada Ambiente",
        "Distribuição por Classe — por Ambiente de Tramitação (2020–2025)",
        "Uma pizza por ambiente (só PV / só PP / ambos) mostrando a composição "
        "por classe processual. Selecione o ambiente na sub-aba.",
        gt7_classe_por_tram,
        "processo (incidente único)",
    ),
    (
        "T8 — Distribuição por Tipo de Questão dentro de cada Ambiente",
        "Distribuição por Tipo de Questão — por Ambiente de Tramitação (2020–2025)",
        "Uma pizza por ambiente (só PV / só PP / ambos) mostrando a composição "
        "por tipo de questão. Selecione o ambiente na sub-aba.",
        gt8_tipo_por_tram,
        "processo (incidente único)",
    ),
    (
        "T9 — Taxa de Conclusão por Ambiente e Classe (%)",
        "Taxa de Conclusão (%) por Ambiente de Tramitação e Classe (2020–2025)",
        "Percentual de inclusões concluídas para cada combinação de ambiente de "
        "tramitação e classe processual.",
        gt9_taxa_conclusao,
        "inclusão em pauta",
    ),
    (
        "T10 — Tabulador Interativo",
        "Tabulador Interativo — Tramitação por Ambiente (2020–2025)",
        "Configure livremente os eixos, agrupamento, métrica e modo de barras. "
        "Use os pré-definidos como ponto de partida.",
        None,
        "variável (conforme configuração)",
    ),
]

_LABELS = [item[0] for item in _CATALOGO]

# ── Tabulador ─────────────────────────────────────────────────────────────────

_PREDEFINIDOS = [
    ("Ambiente × Classe (inclusões, agrupado)",          "tramitacao",   "classe",         "inclusoes", "group"),
    ("Ambiente × Macro-Desfecho (inclusões, agrupado)",  "tramitacao",   "macro_desfecho", "inclusoes", "group"),
    ("Ambiente × Tipo de Questão (processos, agrupado)", "tramitacao",   "tipo_questao",   "processos", "group"),
    ("Classe × Ambiente (inclusões, empilhado 100%)",    "classe",       "tramitacao",     "inclusoes", "100%"),
    ("Classe × Macro-Desfecho (inclusões, empilhado)",   "classe",       "macro_desfecho", "inclusoes", "stack"),
    ("Ano × Ambiente (inclusões, empilhado)",            "ano",          "tramitacao",     "inclusoes", "stack"),
    ("Ano × Macro-Desfecho (inclusões, empilhado 100%)", "ano",          "macro_desfecho", "inclusoes", "100%"),
    ("Tipo de Questão × Desfecho (inclusões, agrupado)", "tipo_questao", "macro_desfecho", "inclusoes", "group"),
]
_LABELS_PRE = [p[0] for p in _PREDEFINIDOS]
_DIMS_LABEL = list(DIMENSOES.keys())


# ── helpers ───────────────────────────────────────────────────────────────────

def _build_tabela(df: pd.DataFrame) -> pd.DataFrame:
    proc      = df.drop_duplicates("incidente").copy()
    inc_total = df.groupby("incidente").size().rename("Total de Inclusões")
    inc_pv    = (df[df["ambiente"] == "Plenário Virtual"]
                 .groupby("incidente").size().rename("Inclusões PV"))
    inc_pp    = (df[df["ambiente"] == "Plenário Físico"]
                 .groupby("incidente").size().rename("Inclusões PP"))
    tab = (
        proc[["incidente", "nome_processo", "classe", "relator", "tipo_questao", "tramitacao"]]
        .join(inc_total, on="incidente")
        .join(inc_pv,    on="incidente")
        .join(inc_pp,    on="incidente")
    )
    tab["Inclusões PV"] = tab["Inclusões PV"].fillna(0).astype(int)
    tab["Inclusões PP"] = tab["Inclusões PP"].fillna(0).astype(int)
    tab["tipo_questao"] = tab["tipo_questao"].replace({"IJ": "QI"})
    return (
        tab.rename(columns={
            "incidente": "Incidente", "nome_processo": "Processo",
            "classe": "Classe", "relator": "Relator",
            "tipo_questao": "Tipo", "tramitacao": "Tramitação",
        })
        .sort_values("Processo")
        .reset_index(drop=True)
    )


def _render_fig(fn, df: pd.DataFrame, show_values: bool) -> None:
    """Chama a função de plot e renderiza — suporta retorno dict (sub-abas) ou Figure."""
    try:
        result = fn(df, show_values=show_values)
    except TypeError:
        result = fn(df)
    if isinstance(result, dict):
        if not result:
            st.info("Sem dados para exibir.")
            return
        subtabs = st.tabs(list(result.keys()))
        for tab, fig in zip(subtabs, result.values()):
            with tab:
                st.plotly_chart(fig, width="stretch")
    else:
        st.plotly_chart(result, width="stretch")


def _render_tabulador(df: pd.DataFrame, key_suffix: str) -> None:
    """Bloco T10: pré-definidos + configuração livre + show_values."""
    col_pre, _ = st.columns([2, 1])
    with col_pre:
        pre_escolha = st.selectbox(
            "🔖 Pré-definidos — escolha uma configuração pronta",
            options=["— ou configure manualmente abaixo —"] + _LABELS_PRE,
            index=0,
            key=f"tab_predefinido_{key_suffix}",
        )

    if pre_escolha.startswith("—"):
        def_x, def_g, def_m, def_bm = 0, 1, 0, 0
    else:
        _, px, pg, pm, pbm = next(p for p in _PREDEFINIDOS if p[0] == pre_escolha)
        def_x  = _DIMS_LABEL.index(next(k for k, v in DIMENSOES.items() if v == px))
        def_g  = _DIMS_LABEL.index(next(k for k, v in DIMENSOES.items() if v == pg))
        def_m  = ["inclusoes", "processos"].index(pm)
        def_bm = ["group", "stack", "100%"].index(pbm)

    c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 1])
    with c1:
        eixo_x_lbl = st.selectbox("Eixo X",    _DIMS_LABEL, index=def_x, key=f"tab_x_{key_suffix}")
    with c2:
        grupo_lbl  = st.selectbox("Cor/Grupo", _DIMS_LABEL, index=def_g, key=f"tab_g_{key_suffix}")
    with c3:
        metrica = st.selectbox(
            "Métrica", ["inclusoes", "processos"], index=def_m, key=f"tab_m_{key_suffix}",
            format_func=lambda v: "Inclusões em pauta" if v == "inclusoes" else "Processos distintos",
        )
    with c4:
        barmode = st.selectbox(
            "Modo", ["group", "stack", "100%"], index=def_bm, key=f"tab_bm_{key_suffix}",
            format_func=lambda v: {"group": "Agrupado", "stack": "Empilhado", "100%": "Empilhado 100%"}[v],
        )
    with c5:
        show_values = st.checkbox("Exibir valores", value=False, key=f"tab_sv_{key_suffix}")

    eixo_x = DIMENSOES[eixo_x_lbl]
    grupo  = DIMENSOES[grupo_lbl]

    if eixo_x == grupo:
        st.warning("Eixo X e Cor/Grupo não podem ser a mesma dimensão.")
        return

    fig = gt10_tabulador(df, eixo_x, grupo, metrica, barmode, show_values)
    st.plotly_chart(fig, width="stretch")


# ── Ponto de entrada ──────────────────────────────────────────────────────────

def render_graficos(df: pd.DataFrame) -> None:
    escolha = st.selectbox(
        "Selecione a visualização",
        options=_LABELS,
        index=0,
        key="tramitacao_selectbox",
    )

    idx = _LABELS.index(escolha)
    _, subtitulo, descricao, fn, unidade = _CATALOGO[idx]

    st.subheader(subtitulo)
    st.markdown(descricao)
    with st.expander("Critério / Caminho dos dados"):
        st.markdown(
            "- **Fonte:** `data/processed/inclusoes_com_pauta.parquet`  \n"
            f"- **Unidade:** {unidade}  \n"
            "- **Período:** 2020–2025"
        )

    if idx == len(_CATALOGO) - 1:  # T10
        _render_tabulador(df, key_suffix="main")
    else:
        show_values = st.checkbox("Exibir valores", value=False, key=f"tram_sv_{idx}")
        _render_fig(fn, df, show_values)

    # ── Tabela consolidada ────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Tabela Consolidada por Processo")
    st.caption("Um registro por processo com o total de inclusões em cada ambiente.")
    with st.expander("Critério / Caminho dos dados"):
        st.markdown(
            "- **Fonte:** `data/processed/inclusoes_com_pauta.parquet`  \n"
            "- **Unidade:** processo (incidente único)  \n"
            "- **Período:** 2020–2025"
        )

    tab = _build_tabela(df)

    col1, col2, col3 = st.columns(3)
    with col1:
        classes   = st.multiselect("Classe",     sorted(tab["Classe"].unique()),     key="tab_classe")
    with col2:
        ambientes = st.multiselect("Tramitação", sorted(tab["Tramitação"].unique()), key="tab_tram")
    with col3:
        busca = st.text_input("Buscar processo", key="tab_busca", placeholder="ex: ADI 3423")

    if classes:
        tab = tab[tab["Classe"].isin(classes)]
    if ambientes:
        tab = tab[tab["Tramitação"].isin(ambientes)]
    if busca:
        tab = tab[tab["Processo"].str.contains(busca, case=False, na=False)]

    st.caption(f"{len(tab):,} processos exibidos")
    st.dataframe(
        tab.drop(columns=["Incidente"]),
        width="stretch",
        hide_index=True,
        column_config={
            "Processo":           st.column_config.TextColumn(width="medium"),
            "Relator":            st.column_config.TextColumn(width="medium"),
            "Tramitação":         st.column_config.TextColumn(width="medium"),
            "Total de Inclusões": st.column_config.NumberColumn(width="small"),
            "Inclusões PV":       st.column_config.NumberColumn(width="small"),
            "Inclusões PP":       st.column_config.NumberColumn(width="small"),
        },
    )
