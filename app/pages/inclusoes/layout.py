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
)

_ABAS = [
    "G5 — Anual por Ambiente",
    "G6 — PV por Classe",
    "G7 — PP por Classe",
    "G8 — Desfecho PV",
    "G9 — Desfecho PP",
    "G10 — Macro Anual PV",
    "G11 — Macro Anual PP",
    "G12 — Concluídos PV",
    "G13 — Concluídos PP",
    "G14 — Não Concluídos/Classe PV",
    "G15 — Não Concluídos/Classe PP",
    "G16 — Concluídos/Classe PV",
    "G17 — Concluídos/Classe PP",
]


def render_graficos(df: pd.DataFrame) -> None:
    tabs = st.tabs(_ABAS)

    with tabs[0]:
        st.subheader("Inclusões em Pauta por Ano e Ambiente")
        st.caption("Volume total de inclusões em pauta por ano, comparando Plenário Virtual e Físico.")
        fig, fig_p = g5_anual_ambiente(df)
        st.plotly_chart(fig, use_container_width=True)
        st.plotly_chart(fig_p, use_container_width=True)

    with tabs[1]:
        st.subheader("Inclusões por Classe — Plenário Virtual")
        st.caption("Barras por classe (eixo esquerdo) e linha do total PV (eixo direito).")
        fig, fig_p = g6_pv_por_classe(df)
        st.plotly_chart(fig, use_container_width=True)
        st.plotly_chart(fig_p, use_container_width=True)

    with tabs[2]:
        st.subheader("Inclusões por Classe — Plenário Físico")
        st.caption("Barras por classe (eixo esquerdo) e linha do total PP (eixo direito).")
        fig, fig_p = g7_pp_por_classe(df)
        st.plotly_chart(fig, use_container_width=True)
        st.plotly_chart(fig_p, use_container_width=True)

    with tabs[3]:
        st.subheader("Desfecho — Plenário Virtual")
        st.caption("Proporção de processos concluídos e não concluídos no PV.")
        fig_macro, fig_det = g8_desfecho_pv(df)
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(fig_macro, use_container_width=True)
        with c2:
            st.plotly_chart(fig_det, use_container_width=True)

    with tabs[4]:
        st.subheader("Desfecho — Plenário Físico")
        st.caption("Proporção de processos concluídos e não concluídos no PP.")
        st.plotly_chart(g9_desfecho_pp(df), use_container_width=True)

    with tabs[5]:
        st.subheader("Concluídos e Não Concluídos por Ano — PV")
        st.caption("Evolução anual do desfecho macro no Plenário Virtual.")
        st.plotly_chart(g10_macro_anual_pv(df), use_container_width=True)

    with tabs[6]:
        st.subheader("Concluídos e Não Concluídos por Ano — PP")
        st.caption("Evolução anual do desfecho macro no Plenário Físico.")
        st.plotly_chart(g11_macro_anual_pp(df), use_container_width=True)

    with tabs[7]:
        st.subheader("Concluídos por Ano — Plenário Virtual")
        st.caption("Fluxo anual de inclusões concluídas no PV.")
        st.plotly_chart(g12_concluidos_pv(df), use_container_width=True)

    with tabs[8]:
        st.subheader("Concluídos por Ano — Plenário Físico")
        st.caption("Fluxo anual de inclusões concluídas no PP.")
        st.plotly_chart(g13_concluidos_pp(df), use_container_width=True)

    with tabs[9]:
        st.subheader("Não Concluídos por Classe e Ano — PV")
        st.caption("Barras por classe + linha do total de não concluídos no PV.")
        st.plotly_chart(g14_nao_concluidos_classe_pv(df), use_container_width=True)

    with tabs[10]:
        st.subheader("Não Concluídos por Classe e Ano — PP")
        st.caption("Barras por classe + linha do total de não concluídos no PP.")
        st.plotly_chart(g15_nao_concluidos_classe_pp(df), use_container_width=True)

    with tabs[11]:
        st.subheader("Concluídos por Classe e Ano — PV")
        st.caption("Barras por classe + linha do total de concluídos no PV.")
        st.plotly_chart(g16_concluidos_classe_pv(df), use_container_width=True)

    with tabs[12]:
        st.subheader("Concluídos por Classe e Ano — PP")
        st.caption("Barras por classe + linha do total de concluídos no PP.")
        st.plotly_chart(g17_concluidos_classe_pp(df), use_container_width=True)
