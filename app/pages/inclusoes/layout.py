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
)


def _chart(fig) -> None:
    st.plotly_chart(fig, use_container_width=True)


def _dict_subtabs(figs: dict[str, object]) -> None:
    """Renderiza um dict {label: figura} como sub-abas."""
    if not figs:
        st.info("Sem dados para exibir.")
        return
    keys = list(figs.keys())
    subtabs = st.tabs(keys)
    for tab, key in zip(subtabs, keys):
        with tab:
            _chart(figs[key])


def render_graficos(df: pd.DataFrame) -> None:
    # ── Bloco INCLUSÕES EM PAUTA ──────────────────────────────────────────────
    st.subheader("Inclusões em Pauta")
    tabs_ip = st.tabs([
        "G5 — Anual/Ambiente",
        "G6 — PV/Classe",
        "G7 — PP/Classe",
        "G8 — Desfecho PV",
        "G9 — Desfecho PP",
        "G10 — Macro Anual PV",
        "G11 — Macro Anual PP",
        "G12 — Concluídos PV",
        "G13 — Concluídos PP",
        "G14 — NC/Classe PV",
        "G15 — NC/Classe PP",
        "G16 — C/Classe PV",
        "G17 — C/Classe PP",
    ])

    with tabs_ip[0]:
        st.caption("Volume total de inclusões por ano — PV vs PP.")
        fig, fig_p = g5_anual_ambiente(df)
        _chart(fig)
        _chart(fig_p)

    with tabs_ip[1]:
        st.caption("Inclusões por classe e ano — Plenário Virtual.")
        fig, fig_p = g6_pv_por_classe(df)
        _chart(fig); _chart(fig_p)

    with tabs_ip[2]:
        st.caption("Inclusões por classe e ano — Plenário Físico.")
        fig, fig_p = g7_pp_por_classe(df)
        _chart(fig); _chart(fig_p)

    with tabs_ip[3]:
        st.caption("Proporção concluído/não concluído — PV (período total).")
        fig_macro, fig_det = g8_desfecho_pv(df)
        c1, c2 = st.columns(2)
        with c1: _chart(fig_macro)
        with c2: _chart(fig_det)

    with tabs_ip[4]:
        st.caption("Proporção concluído/não concluído — PP (período total).")
        _chart(g9_desfecho_pp(df))

    with tabs_ip[5]:
        st.caption("Evolução anual do desfecho macro — PV.")
        _chart(g10_macro_anual_pv(df))

    with tabs_ip[6]:
        st.caption("Evolução anual do desfecho macro — PP.")
        _chart(g11_macro_anual_pp(df))

    with tabs_ip[7]:
        st.caption("Fluxo anual de inclusões concluídas — PV.")
        _chart(g12_concluidos_pv(df))

    with tabs_ip[8]:
        st.caption("Fluxo anual de inclusões concluídas — PP.")
        _chart(g13_concluidos_pp(df))

    with tabs_ip[9]:
        st.caption("Não concluídos por classe e ano — PV.")
        _chart(g14_nao_concluidos_classe_pv(df))

    with tabs_ip[10]:
        st.caption("Não concluídos por classe e ano — PP.")
        _chart(g15_nao_concluidos_classe_pp(df))

    with tabs_ip[11]:
        st.caption("Concluídos por classe e ano — PV.")
        _chart(g16_concluidos_classe_pv(df))

    with tabs_ip[12]:
        st.caption("Concluídos por classe e ano — PP.")
        _chart(g17_concluidos_classe_pp(df))

    st.markdown("---")

    # ── Bloco TIPO DE QUESTÃO ─────────────────────────────────────────────────
    st.subheader("Tipo de Questão")
    tabs_tq = st.tabs([
        "G18 — NC/Tipo PV",
        "G19 — NC/Tipo PP",
        "G20 — C/Tipo PV",
        "G21 — C/Tipo PP",
    ])

    with tabs_tq[0]:
        st.caption("Não concluídos por tipo de questão (PR/RC/QI) e ano — PV.")
        _chart(g18_nc_tipo_pv(df))

    with tabs_tq[1]:
        st.caption("Não concluídos por tipo de questão (PR/RC/QI) e ano — PP.")
        _chart(g19_nc_tipo_pp(df))

    with tabs_tq[2]:
        st.caption("Concluídos por tipo de questão (PR/RC/QI) e ano — PV.")
        _chart(g20_c_tipo_pv(df))

    with tabs_tq[3]:
        st.caption("Concluídos por tipo de questão (PR/RC/QI) e ano — PP.")
        _chart(g21_c_tipo_pp(df))

    st.markdown("---")

    # ── Bloco DESFECHO CONCLUÍDO POR CATEGORIA ────────────────────────────────
    st.subheader("Desfecho Concluído por Categoria")
    tabs_dc = st.tabs([
        "G22 — Período PV",
        "G23 — Período PP",
        "G24 — Anual PV",
        "G25 — Anual PP",
        "G26 — Tipo/Período PV",
        "G27 — Tipo/Período PP",
        "G28 — Tipo/Anual PV",
        "G29 — Tipo/Anual PP",
    ])

    with tabs_dc[0]:
        st.caption("Distribuição por categoria de desfecho — PV (período total).")
        _chart(g22_cat_periodo_pv(df))

    with tabs_dc[1]:
        st.caption("Distribuição por categoria de desfecho — PP (período total).")
        _chart(g23_cat_periodo_pp(df))

    with tabs_dc[2]:
        st.caption("Evolução anual das categorias de desfecho — PV.")
        _chart(g24_cat_anual_pv(df))

    with tabs_dc[3]:
        st.caption("Evolução anual das categorias de desfecho — PP.")
        _chart(g25_cat_anual_pp(df))

    with tabs_dc[4]:
        st.caption("Categoria de desfecho por tipo de questão — PV (período total).")
        _chart(g26_cat_tipo_periodo_pv(df))

    with tabs_dc[5]:
        st.caption("Categoria de desfecho por tipo de questão — PP (período total).")
        _chart(g27_cat_tipo_periodo_pp(df))

    with tabs_dc[6]:
        st.caption("Categoria de desfecho por tipo de questão e ano — PV. Sub-abas por tipo.")
        _dict_subtabs(g28_cat_tipo_anual_pv(df))

    with tabs_dc[7]:
        st.caption("Categoria de desfecho por tipo de questão e ano — PP. Sub-abas por tipo.")
        _dict_subtabs(g29_cat_tipo_anual_pp(df))

    st.markdown("---")

    # ── Bloco DESFECHO NÃO CONCLUÍDO POR CATEGORIA ───────────────────────────
    st.subheader("Desfecho Não Concluído por Categoria")
    tabs_nc = st.tabs([
        "G30 — Anual PV",
        "G31 — Anual PP",
        "G32 — Classe PV",
        "G33 — Classe PP",
        "G34 — Tipo PV",
        "G35 — Tipo PP",
    ])

    with tabs_nc[0]:
        st.caption("Não concluídos por categoria (vista/destaque/retirado/outros) e ano — PV.")
        _chart(g30_nc_cat_anual_pv(df))

    with tabs_nc[1]:
        st.caption("Não concluídos por categoria e ano — PP (destaque = 0 no PP).")
        _chart(g31_nc_cat_anual_pp(df))

    with tabs_nc[2]:
        st.caption("Não concluídos por categoria e ano, por classe — PV. Sub-abas por classe.")
        _dict_subtabs(g32_nc_cat_classe_pv(df))

    with tabs_nc[3]:
        st.caption("Não concluídos por categoria e ano, por classe — PP. Sub-abas por classe.")
        _dict_subtabs(g33_nc_cat_classe_pp(df))

    with tabs_nc[4]:
        st.caption("Não concluídos por categoria e ano, por tipo de questão — PV. Sub-abas por tipo.")
        _dict_subtabs(g34_nc_cat_tipo_pv(df))

    with tabs_nc[5]:
        st.caption("Não concluídos por categoria e ano, por tipo de questão — PP. Sub-abas por tipo.")
        _dict_subtabs(g35_nc_cat_tipo_pp(df))
