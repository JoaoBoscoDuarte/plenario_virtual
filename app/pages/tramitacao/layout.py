"""Renderização da página de Tramitação por Ambiente."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import gt1_tramitacao, gt2_ambos_por_tipo

_CATALOGO = [
    (
        "T1 — Tramitação por Ambiente (processos distintos)",
        "Tramitação por Ambiente — Processos CC (2020–2025)",
        "Pizza com a distribuição dos processos distintos por ambiente de tramitação: "
        "só no Plenário Virtual, só no Plenário Físico, ou em ambos os ambientes. "
        "Unidade: processo (incidente único), não inclusão.",
        gt1_tramitacao,
    ),
    (
        "T2 — Processos em Ambos os Ambientes por Tipo de Questão",
        "Processos em Ambos os Ambientes por Tipo de Questão (2020–2025)",
        "Barras com o volume de processos distintos que tramitaram em ambos os ambientes, "
        "agrupados por tipo de questão (PR / RC / QI). "
        "IJ renomeado para QI na exibição.",
        gt2_ambos_por_tipo,
    ),
]

_LABELS = [item[0] for item in _CATALOGO]

_SUMARIO = {
    "Distribuição por ambiente (T1–T2)": [
        "T1 — proporção de processos por ambiente (só PV / só PP / ambos)",
        "T2 — processos em ambos os ambientes por tipo de questão",
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
        "incidente":    "Incidente",
        "nome_processo": "Processo",
        "classe":       "Classe",
        "relator":      "Relator",
        "tipo_questao": "Tipo",
        "tramitacao":   "Tramitação",
    })
    return tab.sort_values("Processo").reset_index(drop=True)


def render_graficos(df: pd.DataFrame) -> None:
    with st.expander("Sumário — visualizações disponíveis", expanded=True):
        for bloco, graficos in _SUMARIO.items():
            st.markdown(f"**{bloco}**")
            for g in graficos:
                st.markdown(f"- {g}")

    st.markdown("---")

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
        st.markdown(
            "- **Fonte:** `data/processed/inclusoes_com_pauta.parquet`  \n"
            "- **Unidade:** processo (incidente único) — `drop_duplicates('incidente')`  \n"
            "- **Período:** 2020–2025  \n"
            "- **Colunas:** `tramitacao` e `tramitou_ambos` (derivadas do dataset)"
        )

    st.plotly_chart(fn(df), width="stretch")

    # ── Tabela consolidada ───────────────────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Tabela Consolidada por Processo")
    st.caption(
        f"2.834 processos distintos — uma linha por incidente, com contagem de inclusões "
        "por ambiente. Use os filtros da tabela para explorar."
    )

    tab = _build_tabela(df)

    # Filtros rápidos
    col1, col2, col3 = st.columns(3)
    with col1:
        classes = st.multiselect("Classe", sorted(tab["Classe"].unique()), key="tab_classe")
    with col2:
        ambientes = st.multiselect(
            "Tramitação",
            sorted(tab["Tramitação"].unique()),
            key="tab_tram",
        )
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
        use_container_width=True,
        hide_index=True,
        column_config={
            "Processo":           st.column_config.TextColumn(width="medium"),
            "Relator":            st.column_config.TextColumn(width="medium"),
            "Tramitação":        st.column_config.TextColumn(width="medium"),
            "Total de Inclusões": st.column_config.NumberColumn(width="small"),
            "Inclusões PV":       st.column_config.NumberColumn(width="small"),
            "Inclusões PP":       st.column_config.NumberColumn(width="small"),
        },
    )
