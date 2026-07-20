"""Renderização da página Gráficos de Narrativa."""

from __future__ import annotations
import streamlit as st
from .plots import plot_na, plot_nb, plot_nc, plot_nd, plot_ne, plot_nf

_SECOES = [
    ("NA — Participação estável",
     "A participação do Plenário Virtual mantém-se entre 59% e 68% ao ano",
     plot_na),
    ("NB — Pauta versus concluídos (síntese do impacto)",
     "O Plenário Virtual concentra os julgamentos concluídos",
     plot_nb),
    ("NC — Tramitação por ambiente",
     "Três de cada quatro processos nunca passam pelo Plenário Presencial",
     plot_nc),
    ("ND — Recursos",
     "A atividade recursal migrou quase integralmente para o ambiente virtual",
     plot_nd),
    ("NE — Inclusões por processo",
     "Cada julgamento presencial consome mais que o dobro de inclusões em pauta",
     plot_ne),
    ("NF — Conclusão por processo",
     "Considerado o processo, o ambiente virtual conclui 86% do que pauta",
     plot_nf),
]

def render_graficos() -> None:
    for titulo, subtitulo, fn in _SECOES:
        st.subheader(titulo)
        fig = fn()
        st.plotly_chart(fig, width="stretch")
        st.markdown("---")
