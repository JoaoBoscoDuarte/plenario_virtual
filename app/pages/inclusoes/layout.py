"""Renderização da página de Inclusões em Pauta."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import (
    g5_anual_ambiente, g6_pv_por_classe, g7_pp_por_classe,
    g8_desfecho_pv, g9_desfecho_pp,
    g10_macro_anual_pv, g11_macro_anual_pp,
    g12_concluidos_pv, g13_concluidos_pp,
    g14_nao_concluidos_classe_pv, g15_nao_concluidos_classe_pp,
    g16_concluidos_classe_pv, g17_concluidos_classe_pp,
    g18_nc_tipo_pv, g19_nc_tipo_pp, g20_c_tipo_pv, g21_c_tipo_pp,
    g22_cat_periodo_pv, g23_cat_periodo_pp,
    g24_cat_anual_pv, g25_cat_anual_pp,
    g26_cat_tipo_periodo_pv, g27_cat_tipo_periodo_pp,
    g28_cat_tipo_anual_pv, g29_cat_tipo_anual_pp,
    g30_nc_cat_anual_pv, g31_nc_cat_anual_pp,
    g32_nc_cat_classe_pv, g33_nc_cat_classe_pp,
    g34_nc_cat_tipo_pv, g35_nc_cat_tipo_pp,
    g36_sust_periodo_pv, g37_sust_periodo_pp,
    g38_sust_anual_pv, g39_sust_anual_pp,
)

# Catálogo: (label do selectbox, subtítulo, descrição, callable)
# Para gráficos que retornam dict, o callable retorna dict e _render trata.
_CATALOGO: list[tuple[str, str, str, object]] = [
    # ── Inclusões em Pauta ────────────────────────────────────────────────────
    (
        "G5 — Inclusões por Ano e Ambiente (PV vs PP)",
        "Inclusões em Pauta por Ano e Ambiente",
        "Comparação anual do volume de inclusões em pauta entre o Plenário Virtual e o Plenário Físico. "
        "Inclui pizza com a proporção acumulada no período.",
        g5_anual_ambiente,
    ),
    (
        "G6 — Inclusões por Classe e Ano — PV",
        "Inclusões por Classe — Plenário Virtual",
        "Barras agrupadas por classe (ADI, ADPF, ADC, ADO) com linha do total geral no eixo secundário. "
        "Inclui pizza com a distribuição por classe no período.",
        g6_pv_por_classe,
    ),
    (
        "G7 — Inclusões por Classe e Ano — PP",
        "Inclusões por Classe — Plenário Físico",
        "Mesmo recorte do G6, aplicado ao Plenário Físico.",
        g7_pp_por_classe,
    ),
    (
        "G8 — Desfecho Geral — PV (período total)",
        "Desfecho — Plenário Virtual (período total)",
        "Pizza com a proporção de concluídos e não concluídos no PV ao longo de todo o período, "
        "mais pizza com o desfecho detalhado (unânime, maioria, pedido de vista etc.).",
        g8_desfecho_pv,
    ),
    (
        "G9 — Desfecho Geral — PP (período total)",
        "Desfecho — Plenário Físico (período total)",
        "Pizza com a proporção de concluídos e não concluídos no PP ao longo de todo o período.",
        g9_desfecho_pp,
    ),
    (
        "G10 — Concluídos e Não Concluídos por Ano — PV",
        "Macro-Desfecho Anual — Plenário Virtual",
        "Evolução anual do volume de inclusões concluídas e não concluídas no PV.",
        g10_macro_anual_pv,
    ),
    (
        "G11 — Concluídos e Não Concluídos por Ano — PP",
        "Macro-Desfecho Anual — Plenário Físico",
        "Evolução anual do volume de inclusões concluídas e não concluídas no PP.",
        g11_macro_anual_pp,
    ),
    (
        "G12 — Concluídos por Ano — PV",
        "Inclusões Concluídas por Ano — Plenário Virtual",
        "Fluxo anual de inclusões com desfecho concluído no PV, excluindo não concluídos.",
        g12_concluidos_pv,
    ),
    (
        "G13 — Concluídos por Ano — PP",
        "Inclusões Concluídas por Ano — Plenário Físico",
        "Fluxo anual de inclusões com desfecho concluído no PP.",
        g13_concluidos_pp,
    ),
    (
        "G14 — Não Concluídos por Classe e Ano — PV",
        "Não Concluídos por Classe — Plenário Virtual",
        "Barras por classe com linha do total de não concluídos no PV.",
        g14_nao_concluidos_classe_pv,
    ),
    (
        "G15 — Não Concluídos por Classe e Ano — PP",
        "Não Concluídos por Classe — Plenário Físico",
        "Barras por classe com linha do total de não concluídos no PP.",
        g15_nao_concluidos_classe_pp,
    ),
    (
        "G16 — Concluídos por Classe e Ano — PV",
        "Concluídos por Classe — Plenário Virtual",
        "Barras por classe com linha do total de concluídos no PV.",
        g16_concluidos_classe_pv,
    ),
    (
        "G17 — Concluídos por Classe e Ano — PP",
        "Concluídos por Classe — Plenário Físico",
        "Barras por classe com linha do total de concluídos no PP.",
        g17_concluidos_classe_pp,
    ),
    # ── Tipo de Questão ───────────────────────────────────────────────────────
    (
        "G18 — Não Concluídos por Tipo de Questão — PV",
        "Não Concluídos por Tipo de Questão — Plenário Virtual",
        "Barras por tipo de questão (PR / RC / QI) com linha do total de não concluídos no PV. "
        "IJ renomeado para QI na exibição.",
        g18_nc_tipo_pv,
    ),
    (
        "G19 — Não Concluídos por Tipo de Questão — PP",
        "Não Concluídos por Tipo de Questão — Plenário Físico",
        "Mesmo recorte do G18 para o Plenário Físico.",
        g19_nc_tipo_pp,
    ),
    (
        "G20 — Concluídos por Tipo de Questão — PV",
        "Concluídos por Tipo de Questão — Plenário Virtual",
        "Barras por tipo de questão (PR / RC / QI) com linha do total de concluídos no PV.",
        g20_c_tipo_pv,
    ),
    (
        "G21 — Concluídos por Tipo de Questão — PP",
        "Concluídos por Tipo de Questão — Plenário Físico",
        "Mesmo recorte do G20 para o Plenário Físico.",
        g21_c_tipo_pp,
    ),
    # ── Desfecho Concluído por Categoria ─────────────────────────────────────
    (
        "G22 — Categoria de Desfecho — PV (período total)",
        "Categoria de Desfecho — Plenário Virtual (período total)",
        "Pizza com as 4 categorias: Unânime, Maioria (relator vencedor), Maioria (relator vencido) "
        "e Não concluído (bloco agregado).",
        g22_cat_periodo_pv,
    ),
    (
        "G23 — Categoria de Desfecho — PP (período total)",
        "Categoria de Desfecho — Plenário Físico (período total)",
        "Mesmo recorte do G22 para o Plenário Físico.",
        g23_cat_periodo_pp,
    ),
    (
        "G24 — Categoria de Desfecho por Ano — PV",
        "Categoria de Desfecho por Ano — Plenário Virtual",
        "Evolução anual das 4 categorias de desfecho no PV.",
        g24_cat_anual_pv,
    ),
    (
        "G25 — Categoria de Desfecho por Ano — PP",
        "Categoria de Desfecho por Ano — Plenário Físico",
        "Evolução anual das 4 categorias de desfecho no PP.",
        g25_cat_anual_pp,
    ),
    (
        "G26 — Categoria × Tipo de Questão — PV (período total)",
        "Categoria de Desfecho por Tipo de Questão — Plenário Virtual",
        "Eixo X = tipo de questão (PR/RC/QI); barras empilhadas pelas 4 categorias. Período total, PV.",
        g26_cat_tipo_periodo_pv,
    ),
    (
        "G27 — Categoria × Tipo de Questão — PP (período total)",
        "Categoria de Desfecho por Tipo de Questão — Plenário Físico",
        "Mesmo recorte do G26 para o Plenário Físico.",
        g27_cat_tipo_periodo_pp,
    ),
    (
        "G28 — Categoria × Tipo de Questão por Ano — PV",
        "Categoria de Desfecho por Tipo de Questão e Ano — Plenário Virtual",
        "Um gráfico por tipo de questão (PR, RC, QI) mostrando a evolução anual das categorias no PV. "
        "Selecione o tipo na sub-aba.",
        g28_cat_tipo_anual_pv,
    ),
    (
        "G29 — Categoria × Tipo de Questão por Ano — PP",
        "Categoria de Desfecho por Tipo de Questão e Ano — Plenário Físico",
        "Mesmo recorte do G28 para o Plenário Físico.",
        g29_cat_tipo_anual_pp,
    ),
    # ── Desfecho Não Concluído por Categoria ──────────────────────────────────
    (
        "G30 — Não Concluídos por Categoria e Ano — PV",
        "Não Concluídos por Categoria — Plenário Virtual",
        "Evolução anual das 4 categorias de não conclusão: Pedido de vista, Destaque, "
        "Retirado de pauta e Motivos diversos. PV.",
        g30_nc_cat_anual_pv,
    ),
    (
        "G31 — Não Concluídos por Categoria e Ano — PP",
        "Não Concluídos por Categoria — Plenário Físico",
        "Mesmo recorte do G30 para o PP. Destaque = 0 no Plenário Físico.",
        g31_nc_cat_anual_pp,
    ),
    (
        "G32 — Não Concluídos por Categoria e Classe — PV",
        "Não Concluídos por Categoria e Classe — Plenário Virtual",
        "Um gráfico por classe (ADI, ADPF, ADC, ADO) com as categorias de não conclusão no PV. "
        "Selecione a classe na sub-aba.",
        g32_nc_cat_classe_pv,
    ),
    (
        "G33 — Não Concluídos por Categoria e Classe — PP",
        "Não Concluídos por Categoria e Classe — Plenário Físico",
        "Mesmo recorte do G32 para o PP.",
        g33_nc_cat_classe_pp,
    ),
    (
        "G34 — Não Concluídos por Categoria e Tipo — PV",
        "Não Concluídos por Categoria e Tipo de Questão — Plenário Virtual",
        "Um gráfico por tipo de questão (PR, RC, QI) com as categorias de não conclusão no PV. "
        "Selecione o tipo na sub-aba.",
        g34_nc_cat_tipo_pv,
    ),
    (
        "G35 — Não Concluídos por Categoria e Tipo — PP",
        "Não Concluídos por Categoria e Tipo de Questão — Plenário Físico",
        "Mesmo recorte do G34 para o PP.",
        g35_nc_cat_tipo_pp,
    ),
    # ── Sustentação Oral ──────────────────────────────────────────────────────
    (
        "G36 — Sustentação Oral — Período — PV",
        "Sustentação Oral — Plenário Virtual (período total)",
        "Pizza com a proporção de inclusões com e sem sustentação oral no PV ao longo de todo o período.",
        g36_sust_periodo_pv,
    ),
    (
        "G37 — Sustentação Oral — Período — PP",
        "Sustentação Oral — Plenário Físico (período total)",
        "Pizza com a proporção de inclusões com e sem sustentação oral no PP ao longo de todo o período.",
        g37_sust_periodo_pp,
    ),
    (
        "G38 — Sustentação Oral — Anual — PV",
        "Sustentação Oral por Ano — Plenário Virtual",
        "Contagem anual de inclusões com sustentação oral realizada no PV (2020–2025).",
        g38_sust_anual_pv,
    ),
    (
        "G39 — Sustentação Oral — Anual — PP",
        "Sustentação Oral por Ano — Plenário Físico",
        "Contagem anual de inclusões com sustentação oral realizada no PP (2020–2025).",
        g39_sust_anual_pp,
    ),
]

_LABELS = [item[0] for item in _CATALOGO]

_SUMARIO = {
    "Inclusões em Pauta (G5–G17)": [
        "G5 — volume anual por ambiente (PV vs PP)",
        "G6/G7 — volume por classe e ano (PV e PP)",
        "G8/G9 — desfecho geral no período (PV e PP)",
        "G10/G11 — macro-desfecho anual (PV e PP)",
        "G12/G13 — concluídos por ano (PV e PP)",
        "G14/G15 — não concluídos por classe (PV e PP)",
        "G16/G17 — concluídos por classe (PV e PP)",
    ],
    "Tipo de Questão (G18–G21)": [
        "G18/G19 — não concluídos por tipo PR/RC/QI (PV e PP)",
        "G20/G21 — concluídos por tipo PR/RC/QI (PV e PP)",
    ],
    "Desfecho Concluído por Categoria (G22–G29)": [
        "G22/G23 — distribuição por categoria no período (PV e PP)",
        "G24/G25 — evolução anual por categoria (PV e PP)",
        "G26/G27 — categoria × tipo de questão no período (PV e PP)",
        "G28/G29 — categoria × tipo de questão por ano (PV e PP)",
    ],
    "Desfecho Não Concluído por Categoria (G30–G35)": [
        "G30/G31 — categorias de não conclusão por ano (PV e PP)",
        "G32/G33 — categorias de não conclusão por classe (PV e PP)",
        "G34/G35 — categorias de não conclusão por tipo de questão (PV e PP)",
    ],
    "Sustentação Oral (G36–G39)": [
        "G36/G37 — proporção com/sem sustentação no período (PV e PP)",
        "G38/G39 — contagem anual com sustentação oral (PV e PP)",
    ],
}


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
    elif isinstance(result, tuple):
        for fig in result:
            st.plotly_chart(fig, width="stretch")
    else:
        st.plotly_chart(result, width="stretch")


def render_graficos(df: pd.DataFrame) -> None:
    # ── Sumário ───────────────────────────────────────────────────────────────
    with st.expander("Sumário — visualizações disponíveis", expanded=True):
        cols = st.columns(2)
        items = list(_SUMARIO.items())
        for i, (bloco, graficos) in enumerate(items):
            with cols[i % 2]:
                st.markdown(f"**{bloco}**")
                for g in graficos:
                    st.markdown(f"- {g}")

    st.markdown("---")

    # ── Seletor único ─────────────────────────────────────────────────────────
    escolha = st.selectbox(
        "Selecione a visualização",
        options=_LABELS,
        index=0,
        key="inclusoes_selectbox",
    )

    idx = _LABELS.index(escolha)
    _, subtitulo, descricao, fn = _CATALOGO[idx]

    st.subheader(subtitulo)
    st.caption(descricao)
    with st.expander("Critério / Caminho dos dados"):
        st.markdown(
            "- **Fonte:** `data/processed/inclusoes_em_pauta.parquet`  \n"
            "- **Período:** 2020–2025  \n"
            "- **Unidade:** inclusão em pauta (uma linha por inclusão)  \n"
            "- **Renomeação:** `IJ` → `QI` (Questão Incidental) apenas na exibição"
        )

    _render(fn, df)
