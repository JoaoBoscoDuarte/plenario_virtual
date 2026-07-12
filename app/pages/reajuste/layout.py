"""Renderização da página de Reajuste de Voto."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import (
    gr1_pizza_pv, gr2_pizza_pp,
    gr3_anual_pv, gr4_anual_pp,
    gr5_classe_pv, gr6_classe_pp,
)

_CATALOGO = [
    (
        "R1 — Proporção com/sem reajuste — PV (período total)",
        "Reajuste de Voto — Plenário Virtual (período total)",
        "Pizza com a proporção de inclusões que tiveram ao menos um reajuste de voto "
        "no Plenário Virtual ao longo de todo o período (2020–2025).",
        gr1_pizza_pv,
    ),
    (
        "R2 — Proporção com/sem reajuste — PP (período total)",
        "Reajuste de Voto — Plenário Físico (período total)",
        "Mesmo recorte do R1 para o Plenário Físico.",
        gr2_pizza_pp,
    ),
    (
        "R3 — Reajustes por Ano — PV",
        "Reajuste de Voto por Ano — Plenário Virtual",
        "Volume anual de inclusões em pauta que registraram reajuste de voto no PV. "
        "Anos sem ocorrência aparecem com valor zero.",
        gr3_anual_pv,
    ),
    (
        "R4 — Reajustes por Ano — PP",
        "Reajuste de Voto por Ano — Plenário Físico",
        "Mesmo recorte do R3 para o Plenário Físico.",
        gr4_anual_pp,
    ),
    (
        "R5 — Reajustes por Ano e Classe — PV",
        "Reajuste de Voto por Ano e Classe — Plenário Virtual",
        "Barras agrupadas por classe (ADI, ADPF, ADC, ADO) mostrando o volume anual "
        "de reajustes de voto no PV.",
        gr5_classe_pv,
    ),
    (
        "R6 — Reajustes por Ano e Classe — PP",
        "Reajuste de Voto por Ano e Classe — Plenário Físico",
        "Mesmo recorte do R5 para o Plenário Físico.",
        gr6_classe_pp,
    ),
]

_LABELS = [item[0] for item in _CATALOGO]

_SUMARIO = {
    "Período total (R1–R2)": [
        "R1 — proporção com/sem reajuste — PV",
        "R2 — proporção com/sem reajuste — PP",
    ],
    "Evolução anual (R3–R4)": [
        "R3 — volume de reajustes por ano — PV",
        "R4 — volume de reajustes por ano — PP",
    ],
    "Por classe (R5–R6)": [
        "R5 — reajustes por ano e classe — PV",
        "R6 — reajustes por ano e classe — PP",
    ],
}


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
        key="reajuste_selectbox",
    )

    idx = _LABELS.index(escolha)
    _, subtitulo, descricao, fn = _CATALOGO[idx]

    st.subheader(subtitulo)
    st.caption(descricao)
    with st.expander("Critério / Caminho dos dados"):
        st.markdown(
            "- **Fonte:** `data/processed/inclusoes_com_pauta.parquet`  \n"
            "- **Coluna-chave:** `teve_reajuste` (bool) — `True` quando a inclusão "
            "registrou ao menos um andamento de reajuste de voto  \n"
            "- **Período:** 2020–2025  \n"
            "- **Unidade:** inclusão em pauta (uma linha por inclusão)"
        )

    st.plotly_chart(fn(df), use_container_width=True)
