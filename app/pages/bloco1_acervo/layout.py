"""Renderização da página Bloco 1 — Narrativa do Acervo."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import fig_1a_variacao_trienal, fig_1b_acervo_por_classe, fig_1c_distribuicao_baixa, fig_1d_variacao_anual

_CATALOGO = [
    ("1.a — Variação trienal", "Variação trienal do acervo (distribuições − baixas), 1988–2025.", fig_1a_variacao_trienal),
    ("1.b — Acervo por classe", "Acervo ativo por classe processual e ano (barras horizontais empilhadas), 1988–2025.", fig_1b_acervo_por_classe),
    ("1.c — Distribuição e baixa espelhada", "Distribuições e baixas anuais, escala espelhada, 1988–2025.", fig_1c_distribuicao_baixa),
    ("1.d — Variação anual", "Variação anual do acervo (distribuições − baixas), 1988–2025.", fig_1d_variacao_anual),
]
_LABELS = [item[0] for item in _CATALOGO]


def render_graficos(df: pd.DataFrame) -> None:
    escolha = st.selectbox("Selecione a visualização", options=_LABELS, index=0, key="bloco1_selectbox")
    idx = _LABELS.index(escolha)
    _, descricao, fn = _CATALOGO[idx]

    st.caption(descricao)
    show_values = st.checkbox("Exibir valores", value=True, key=f"bloco1_sv_{idx}")

    fig = fn(df, show_values=show_values)
    st.plotly_chart(fig, width="stretch")

    with st.expander("📊 Dados agregados por ano"):
        tab = df.groupby("ano", as_index=False)[
            ["quantidade_ativos", "quantidade_distribuidos", "quantidade_baixas"]
        ].sum()
        st.dataframe(tab, width="stretch", height=280)
