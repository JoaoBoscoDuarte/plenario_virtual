"""Renderização da página Gráficos de Narrativa."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import plot_na, plot_nb, plot_nc, plot_nd, plot_ne, plot_nf

_CATALOGO = [
    (
        "NA — Participação estável",
        "Participação estável do PV ao ano",
        "Barras anuais do percentual de inclusões em pauta destinadas ao PV, com marcador vertical no fim da ESPIN (abril de 2022).",
        plot_na,
    ),
    (
        "NB — Pauta versus concluídos",
        "Pauta versus concluídos (síntese do impacto)",
        "Participação do PV na pauta (63,9%) e nos julgamentos concluídos (91,3%).",
        plot_nb,
    ),
    (
        "NC — Tramitação por ambiente",
        "Tramitação por ambiente",
        "Três barras horizontais: processos que tramitaram somente PV, ambos, somente PP.",
        plot_nc,
    ),
    (
        "ND — Recursos",
        "Recursos",
        "Barra única empilhada com o destino das inclusões de recursos: PV (94,3%) vs PP (5,7%).",
        plot_nd,
    ),
    (
        "NE — Inclusões por processo",
        "Inclusões por processo",
        "Média de inclusões em pauta por processo em cada ambiente: PV (1,8) vs PP (4,3).",
        plot_ne,
    ),
    (
        "NF — Conclusão por processo",
        "Conclusão por processo",
        "Percentual de processos pautados que tiveram julgamento concluído: PV (86,0%) vs PP (39,2%).",
        plot_nf,
    ),
]

_LABELS = [item[0] for item in _CATALOGO]

_SUMARIO = {
    "Volume e estabilidade": [
        "NA — participação do PV ao ano (59%–68%)",
    ],
    "Criação de valor": [
        "NB — PV na pauta (63,9%) vs concluídos (91,3%)",
    ],
    "A tramitação por ambiente": [
        "NC — somente PV (77,5%), ambos (16,9%), somente PP (5,6%)",
    ],
    "O tipo de questão decidida": [
        "ND — recursos no PV (94,3%) vs PP (5,7%)",
    ],
    "As múltiplas inclusões em pauta": [
        "NE — média de inclusões por processo: PV (1,8) vs PP (4,3)",
        "NF — conclusão por processo: PV (86,0%) vs PP (39,2%)",
    ],
}


def _tabela_na() -> pd.DataFrame:
    return pd.DataFrame({
        "Ano": ["2020", "2021", "2022", "2023", "2024", "2025"],
        "Inclusões PV": [3021, 468, 1257, 541, 237, 283],
        "Total inclusões": ["5.053", "688", "1.961", "810", "402", "425"],
        "% PV": ["59,8%", "68,0%", "64,1%", "66,8%", "59,0%", "66,6%"],
    }).assign(**{"Inclusões PV": lambda d: [int(str(v).replace(".", "")) for v in d["Inclusões PV"]]})

def _tabela_nb() -> pd.DataFrame:
    return pd.DataFrame({
        "Métrica": ["Participação na pauta", "Participação nos julgamentos concluídos"],
        "PV": ["63,9% (4.807 de 7.517)", "91,3% (2.911 de 3.187)"],
        "PP": ["36,1% (2.710 de 7.517)", "8,7% (276 de 3.187)"],
    })

def _tabela_nc() -> pd.DataFrame:
    return pd.DataFrame({
        "Tramitação": ["Somente PV", "Ambos", "Somente PP", "Total"],
        "Processos": [2197, 478, 159, 2834],
        "%": ["77,5%", "16,9%", "5,6%", "100%"],
    })

def _tabela_nd() -> pd.DataFrame:
    return pd.DataFrame({
        "Destino": ["Plenário Virtual", "Plenário Presencial", "Total"],
        "Recursos": [1048, 63, 1111],
        "%": ["94,3%", "5,7%", "100%"],
    })

def _tabela_ne() -> pd.DataFrame:
    return pd.DataFrame({
        "Ambiente": ["Plenário Virtual", "Plenário Presencial"],
        "Inclusões em pauta": [4807, 2710],
        "Processos distintos": [2675, 637],
        "Média (incl./proc.)": ["1,8", "4,3"],
    })

def _tabela_nf() -> pd.DataFrame:
    return pd.DataFrame({
        "Ambiente": ["PV", "PP"],
        "Processos pautados": [2675, 637],
        "Com julgamento concluído": ["2.301", "250"],
        "% concluído": ["86,0%", "39,2%"],
    })


_TABELAS = [_tabela_na, _tabela_nb, _tabela_nc, _tabela_nd, _tabela_ne, _tabela_nf]


def render_graficos() -> None:
    with st.expander("Sumário — visualizações disponíveis", expanded=True):
        cols = st.columns(2)
        items = list(_SUMARIO.items())
        for i, (bloco, graficos) in enumerate(items):
            with cols[i % 2]:
                st.markdown(f"**{bloco}**")
                for g in graficos:
                    st.markdown(f"- {g}")

    st.markdown("---")

    escolha = st.selectbox(
        "Selecione a visualização",
        options=_LABELS,
        index=0,
        key="narrativa_selectbox",
    )

    idx = _LABELS.index(escolha)
    _, subtitulo, descricao, fn = _CATALOGO[idx]

    st.subheader(subtitulo)
    st.caption(descricao)

    fig = fn()
    st.plotly_chart(fig, width="stretch")

    with st.expander("📊 Dados da visualização"):
        tab = _TABELAS[idx]()
        st.dataframe(tab.style.format(
            {c: "{:,.0f}" for c in tab.columns if tab[c].dtype.kind in "iuf"},
            na_rep="—",
        ), width="stretch", height=280)
