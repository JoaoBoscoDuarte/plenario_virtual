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
)

_CATALOGO = [
    (
        "T1 — Tramitação por Ambiente (pizza geral)",
        "Tramitação por Ambiente — Processos CC (2020–2025)",
        "Pizza com a distribuição dos 2.834 processos distintos por ambiente: "
        "só PV, só PP ou ambos. Unidade: processo (incidente único).",
        gt1_tramitacao,
    ),
    (
        "T2 — Tramitação por Ambiente e Classe",
        "Tramitação por Ambiente e Classe — Processos CC (2020–2025)",
        "Barras agrupadas por ambiente de tramitação (só PV / só PP / ambos) "
        "para cada classe processual (ADI, ADPF, ADC, ADO). Unidade: processo.",
        gt2_tram_por_classe,
    ),
    (
        "T3 — Tramitação por Ambiente e Tipo de Questão",
        "Tramitação por Ambiente e Tipo de Questão — Processos CC (2020–2025)",
        "Barras agrupadas por ambiente de tramitação para cada tipo de questão "
        "(PR / RC / QI). IJ renomeado para QI. Unidade: processo.",
        gt3_tram_por_tipo,
    ),
    (
        "T4 — Processos em Ambos os Ambientes por Tipo de Questão",
        "Processos em Ambos os Ambientes por Tipo de Questão (2020–2025)",
        "Recorte dos 478 processos que tramitaram em ambos os ambientes, "
        "distribuídos por tipo de questão (PR / RC / QI). Unidade: processo.",
        gt4_ambos_por_tipo,
    ),
    (
        "T5 — Macro-Desfecho por Ambiente de Tramitação",
        "Macro-Desfecho por Ambiente de Tramitação — Inclusões (2020–2025)",
        "Barras com o volume de inclusões concluídas e não concluídas em cada "
        "grupo de tramitação (só PV / só PP / ambos). Unidade: inclusão em pauta.",
        gt5_macro_por_tram,
    ),
    (
        "T6 — Desfecho Detalhado por Ambiente de Tramitação",
        "Desfecho Detalhado por Ambiente de Tramitação — Inclusões (2020–2025)",
        "Barras com os 7 desfechos detalhados (unânime, maioria, pedido de vista etc.) "
        "para cada grupo de tramitação. Unidade: inclusão em pauta.",
        gt6_desfecho_por_tram,
    ),
    (
        "T7 — Distribuição por Classe dentro de cada Ambiente",
        "Distribuição por Classe — por Ambiente de Tramitação (2020–2025)",
        "Uma pizza por ambiente (só PV / só PP / ambos) mostrando a composição "
        "por classe processual. Selecione o ambiente na sub-aba. Unidade: processo.",
        gt7_classe_por_tram,
    ),
    (
        "T8 — Distribuição por Tipo de Questão dentro de cada Ambiente",
        "Distribuição por Tipo de Questão — por Ambiente de Tramitação (2020–2025)",
        "Uma pizza por ambiente (só PV / só PP / ambos) mostrando a composição "
        "por tipo de questão. Selecione o ambiente na sub-aba. Unidade: processo.",
        gt8_tipo_por_tram,
    ),
    (
        "T9 — Taxa de Conclusão por Ambiente e Classe (%)",
        "Taxa de Conclusão (%) por Ambiente de Tramitação e Classe (2020–2025)",
        "Percentual de inclusões concluídas para cada combinação de ambiente de "
        "tramitação e classe processual. Unidade: inclusão em pauta.",
        gt9_taxa_conclusao,
    ),
]

_LABELS = [item[0] for item in _CATALOGO]

_SUMARIO = {
    "Distribuição geral (T1–T4)": [
        "T1 — pizza geral por ambiente (só PV / só PP / ambos)",
        "T2 — tramitação por ambiente e classe",
        "T3 — tramitação por ambiente e tipo de questão",
        "T4 — processos em ambos os ambientes por tipo de questão",
    ],
    "Desfecho por tramitação (T5–T6)": [
        "T5 — macro-desfecho (concluído / não concluído) por ambiente",
        "T6 — desfecho detalhado (7 categorias) por ambiente",
    ],
    "Composição interna por ambiente (T7–T9)": [
        "T7 — distribuição por classe dentro de cada ambiente",
        "T8 — distribuição por tipo de questão dentro de cada ambiente",
        "T9 — taxa de conclusão (%) por ambiente e classe",
    ],
}


def _build_tabela(df: pd.DataFrame) -> pd.DataFrame:
    """Consolida uma linha por processo com contagens de inclusões por ambiente."""
    proc = df.drop_duplicates("incidente").copy()
    inc_total = df.groupby("incidente").size().rename("Total de Inclusões")
    inc_pv = (
        df[df["ambiente"] == "Plenário Virtual"]
        .groupby("incidente").size().rename("Inclusões PV")
    )
    inc_pp = (
        df[df["ambiente"] == "Plenário Físico"]
        .groupby("incidente").size().rename("Inclusões PP")
    )
    tab = (
        proc[["incidente", "nome_processo", "classe", "relator", "tipo_questao", "tramitacao"]]
        .join(inc_total, on="incidente")
        .join(inc_pv, on="incidente")
        .join(inc_pp, on="incidente")
    )
    tab["Inclusões PV"] = tab["Inclusões PV"].fillna(0).astype(int)
    tab["Inclusões PP"] = tab["Inclusões PP"].fillna(0).astype(int)
    tab["tipo_questao"] = tab["tipo_questao"].replace({"IJ": "QI"})
    tab = tab.rename(columns={
        "incidente":     "Incidente",
        "nome_processo": "Processo",
        "classe":        "Classe",
        "relator":       "Relator",
        "tipo_questao":  "Tipo",
        "tramitacao":    "Tramitação",
    })
    return tab.sort_values("Processo").reset_index(drop=True)


def _render(fn, df: pd.DataFrame) -> None:
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


def render_graficos(df: pd.DataFrame) -> None:
    # ── Sumário ───────────────────────────────────────────────────────────────
    with st.expander("Sumário — visualizações disponíveis", expanded=True):
        cols = st.columns(3)
        for i, (bloco, graficos) in enumerate(_SUMARIO.items()):
            with cols[i]:
                st.markdown(f"**{bloco}**")
                for g in graficos:
                    st.markdown(f"- {g}")

    st.markdown("---")

    # ── Seletor único ─────────────────────────────────────────────────────────
    escolha = st.selectbox(
        "Selecione a visualização",
        options=_LABELS,
        index=0,
        key="tramitacao_selectbox",
    )

    idx = _LABELS.index(escolha)
    _, subtitulo, descricao, fn = _CATALOGO[idx]

    st.subheader(subtitulo)
    st.caption(descricao)
    with st.expander("Critério / Caminho dos dados"):
        unidade = "processo (incidente único)" if idx in (0, 1, 2, 3, 6, 7) else "inclusão em pauta"
        st.markdown(
            "- **Fonte:** `data/processed/inclusoes_com_pauta.parquet`  \n"
            f"- **Unidade:** {unidade}  \n"
            "- **Período:** 2020–2025"
        )

    _render(fn, df)

    # ── Tabela consolidada ────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Tabela Consolidada por Processo")

    tab = _build_tabela(df)

    col1, col2, col3 = st.columns(3)
    with col1:
        classes = st.multiselect("Classe", sorted(tab["Classe"].unique()), key="tab_classe")
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
