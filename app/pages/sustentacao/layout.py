"""Renderização da página de Sustentação Oral."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import (
    gs1_pizza_pv, gs2_pizza_pp,
    gs3_anual_pv, gs4_anual_pp,
    gs5_classe_pv, gs6_classe_pp,
    gs7_tipo_pv, gs8_taxa_ambiente,
)

_CATALOGO = [
    (
        "S1 — Proporção com/sem sustentação — PV (período total)",
        "Sustentação Oral — Plenário Virtual (período total)",
        "Pizza com a proporção de inclusões que tiveram sustentação oral realizada "
        "no Plenário Virtual ao longo de todo o período (2020–2025).",
        gs1_pizza_pv,
    ),
    (
        "S2 — Proporção com/sem sustentação — PP (período total)",
        "Sustentação Oral — Plenário Físico (período total)",
        "Mesmo recorte do S1 para o Plenário Físico.",
        gs2_pizza_pp,
    ),
    (
        "S3 — Sustentações por Ano — PV",
        "Sustentação Oral por Ano — Plenário Virtual",
        "Volume anual de inclusões com sustentação oral no PV. "
        "Anos sem ocorrência aparecem com valor zero.",
        gs3_anual_pv,
    ),
    (
        "S4 — Sustentações por Ano — PP",
        "Sustentação Oral por Ano — Plenário Físico",
        "Mesmo recorte do S3 para o Plenário Físico.",
        gs4_anual_pp,
    ),
    (
        "S5 — Sustentações por Ano e Classe — PV",
        "Sustentação Oral por Ano e Classe — Plenário Virtual",
        "Barras agrupadas por classe (ADI, ADPF, ADC, ADO) com linha do total no eixo secundário. PV.",
        gs5_classe_pv,
    ),
    (
        "S6 — Sustentações por Ano e Classe — PP",
        "Sustentação Oral por Ano e Classe — Plenário Físico",
        "Mesmo recorte do S5 para o Plenário Físico.",
        gs6_classe_pp,
    ),
    (
        "S7 — Sustentações por Ano e Tipo de Questão — PV",
        "Sustentação Oral por Ano e Tipo de Questão — Plenário Virtual",
        "Barras agrupadas por tipo de questão (PR / RC / QI) com linha do total. "
        "IJ renomeado para QI na exibição. Apenas PV.",
        gs7_tipo_pv,
    ),
    (
        "S8 — Taxa de Sustentação por Ano e Ambiente (%)",
        "Taxa de Sustentação Oral por Ano e Ambiente (%)",
        "Percentual de inclusões com sustentação oral em cada ano, comparando "
        "Plenário Virtual e Plenário Físico lado a lado.",
        gs8_taxa_ambiente,
    ),
]

_LABELS = [item[0] for item in _CATALOGO]

_SUMARIO = {
    "Período total (S1–S2)": [
        "S1 — proporção com/sem sustentação — PV",
        "S2 — proporção com/sem sustentação — PP",
    ],
    "Evolução anual (S3–S4)": [
        "S3 — volume de sustentações por ano — PV",
        "S4 — volume de sustentações por ano — PP",
    ],
    "Por classe e tipo (S5–S7)": [
        "S5 — sustentações por ano e classe — PV",
        "S6 — sustentações por ano e classe — PP",
        "S7 — sustentações por ano e tipo de questão — PV",
    ],
    "Comparação entre ambientes (S8)": [
        "S8 — taxa de sustentação (%) por ano e ambiente",
    ],
}


def render_graficos(df: pd.DataFrame) -> None:
    with st.expander("Sumário — visualizações disponíveis", expanded=True):
        cols = st.columns(2)
        for i, (bloco, graficos) in enumerate(_SUMARIO.items()):
            with cols[i % 2]:
                st.markdown(f"**{bloco}**")
                for g in graficos:
                    st.markdown(f"- {g}")

    st.markdown("---")

    escolha = st.selectbox(
        "Selecione a visualização",
        options=_LABELS,
        index=0,
        key="sustentacao_selectbox",
    )

    idx = _LABELS.index(escolha)
    _, subtitulo, descricao, fn = _CATALOGO[idx]

    st.subheader(subtitulo)
    st.caption(descricao)
    with st.expander("Critério / Caminho dos dados"):
        st.markdown(
            "- **Fonte:** `data/processed/inclusoes_em_pauta.parquet`  \n"
            "- **Coluna-chave:** `teve_sustentacao` (bool) — `True` quando a inclusão "
            "registrou ao menos um andamento de sustentação oral realizada  \n"
            "- **Período:** 2020–2025  \n"
            "- **Unidade:** inclusão em pauta  \n"
            "- **Detecção:** `and_nome == 'Sustentação Oral'` OU padrão regex no complemento; "
            "sustentações indeferidas/rejeitadas excluídas; janela de ±15/+30 dias da inclusão"
        )

    st.plotly_chart(fn(df), width="stretch")
