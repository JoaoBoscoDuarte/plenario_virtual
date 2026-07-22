"""Renderização da página Bloco 2 — Narrativa Estendida das Inclusões em Pauta."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from . import plots as p

_CATALOGO = [
    ("2.a — Participação por ano", "Participação % do PV nas inclusões, 2016–2025.", p.fig_2a_participacao_ano),
    ("2.b — Inclusões por ano e ambiente", "Volume de inclusões por ano e ambiente, 2016–2025.", p.fig_2b_inclusoes_ano_ambiente),
    ("2.c — Composição do PV por tipo", "Inclusões do PV por tipo de questão (PR/RC/QI), 2016–2019.", p.fig_2c_composicao_pv_tipo, p._tabela_2c),
    ("2.e — Classe por ano (PV)", "Inclusões por classe e ano no PV, 2020–2025.", p.fig_2e_classe_ano_pv),
    ("2.f — Classe por ano (PP)", "Inclusões por classe e ano no PP, 2020–2025.", p.fig_2f_classe_ano_pp),
    ("2.h — Tramitação anual (2020–2025)", "Tramitação por ambiente e ano, 2020–2025.", p.fig_2h_tramitacao_anual_2020),
    ("2.i — Tramitação anual (2016–2025)", "Tramitação por ambiente e ano, série completa.", p.fig_2i_tramitacao_anual_2016),
    ("2.j — Destino dos recursos (2020–2025)", "Recursos por ambiente, 2020–2025.", p.fig_2j_recursos_2020),
    ("2.j2 — Destino dos recursos (2016–2019)", "Recursos por ambiente, 2016–2019.", p.fig_2j2_recursos_2016),
    ("2.k1 — Tipo × ambiente (2016–2019)", "Tipo de questão por ambiente, 2016–2019.", p.fig_2k1_tipo_ambiente_2016),
    ("2.k2 — Tipo × ambiente (2020–2025)", "Tipo de questão por ambiente, 2020–2025.", p.fig_2k2_tipo_ambiente_2020),
    ("2.l — Pauta vs. concluídos", "Participação do PV na pauta e nos concluídos, 2020–2025.", p.fig_2l_pauta_vs_concluidos),
    ("2.m — Desfecho por categoria (PV)", "Desfecho por categoria e ano no PV, 2020–2025.", p.fig_2m_categoria_ano_pv),
    ("2.n — Desfecho por categoria (PP)", "Desfecho por categoria e ano no PP, 2020–2025.", p.fig_2n_categoria_ano_pp),
    ("2.o — Não concluídos por categoria (PV)", "Motivos de não conclusão no PV, 2020–2025.", p.fig_2o_nc_categoria_ano_pv),
    ("2.p — Não concluídos por categoria (PP)", "Motivos de não conclusão no PP, 2020–2025.", p.fig_2p_nc_categoria_ano_pp),
    ("2.q — Média de inclusões por processo", "Média de inclusões por processo, 2020–2025.", p.fig_2q_media_por_processo),
    ("2.r — % de processos concluídos", "Percentual de processos concluídos, 2020–2025.", p.fig_2r_pct_concluidos),
    ("3.1 — Tramitação por período (2016–2019)", "Tramitação por ambiente, 2016–2019.", p.fig_31_tramitacao_2016),
    ("3.2 — Tramitação por período (2020–2025)", "Tramitação por ambiente, 2020–2025.", p.fig_32_tramitacao_2020),
]
_LABELS = [item[0] for item in _CATALOGO]


def render_graficos(df: pd.DataFrame) -> None:
    escolha = st.selectbox("Selecione a visualização", options=_LABELS, index=0, key="bloco2_selectbox")
    idx = _LABELS.index(escolha)
    item = _CATALOGO[idx]
    _, descricao, fn = item[0], item[1], item[2]
    dados_fn = item[3] if len(item) > 3 else None

    st.caption(descricao)
    show_values = st.checkbox("Exibir valores", value=True, key=f"bloco2_sv_{idx}")

    fig = fn(df, show_values=show_values)
    st.plotly_chart(fig, width="stretch")

    if dados_fn is not None:
        tabela = dados_fn(df)
        with st.expander("📊 Dado exportado (tabela)"):
            st.dataframe(tabela, width="stretch")
            st.download_button(
                "Baixar CSV", tabela.to_csv(index=False).encode("utf-8"),
                file_name=f"{_LABELS[idx].split(' — ')[0]}.csv", mime="text/csv",
                key=f"bloco2_download_{idx}",
            )
