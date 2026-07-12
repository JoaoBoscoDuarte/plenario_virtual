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
