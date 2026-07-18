"""Renderização da página de Sustentação Oral."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import (
    gs1_sust_filtravel, gs3_sust_anual_filtravel,
    gs5_sust_classe_filtravel, gs7_sust_tipo_filtravel, gs8_taxa_ambiente,
)
from pages.tramitacao.plots import gt10_tabulador, DIMENSOES

_CATALOGO = [
    (
        "S1/S2 — Proporção com/sem sustentação (Plenário Virtual e Plenário Presencial)",
        "Sustentação Oral — período total",
        "Pizza com a proporção de inclusões que tiveram sustentação oral. "
        "Selecione o âmbito.",
        gs1_sust_filtravel,
    ),
    (
        "S3/S4 — Sustentações por Ano (Plenário Virtual e Plenário Presencial)",
        "Sustentação Oral por Ano",
        "Volume anual de inclusões com sustentação oral. "
        "Anos sem ocorrência aparecem com valor zero. Selecione o âmbito.",
        gs3_sust_anual_filtravel,
    ),
    (
        "S5/S6 — Sustentações por Ano e Classe (Plenário Virtual e Plenário Presencial)",
        "Sustentação Oral por Ano e Classe",
        "Barras agrupadas por classe (ADI, ADPF, ADC, ADO) com linha do total "
        "no eixo secundário. Selecione o âmbito.",
        gs5_sust_classe_filtravel,
    ),
    (
        "S7 — Sustentações por Ano e Tipo de Questão",
        "Sustentação Oral por Ano e Tipo de Questão",
        "Barras agrupadas por tipo de questão (PR / RC / QI) com linha do total. "
        "IJ renomeado para QI. Selecione o âmbito.",
        gs7_sust_tipo_filtravel,
    ),
    (
        "S8 — Taxa de Sustentação por Ano e Ambiente (%)",
        "Taxa de Sustentação Oral por Ano e Ambiente (%)",
        "Percentual de inclusões com sustentação oral em cada ano, comparando "
        "Plenário Virtual e Plenário Presencial lado a lado.",
        gs8_taxa_ambiente,
    ),
    (
        "S9 — Tabulador Interativo",
        "Tabulador Interativo — Sustentação Oral (2020–2025)",
        "Configure livremente os eixos, agrupamento, métrica e modo de barras.",
        None,
    ),
]
_LABELS = [item[0] for item in _CATALOGO]

_SUMARIO = {
    "Período total (S1/S2)": [
        "S1/S2 — proporção com/sem sustentação (Plenário Virtual e Plenário Presencial)",
    ],
    "Evolução anual (S3/S4)": [
        "S3/S4 — volume de sustentações por ano (Plenário Virtual e Plenário Presencial)",
    ],
    "Por classe e tipo (S5–S7)": [
        "S5/S6 — sustentações por ano e classe (Plenário Virtual e Plenário Presencial)",
        "S7 — sustentações por ano e tipo de questão",
    ],
    "Comparação e exploração (S8–S9)": [
        "S8 — taxa de sustentação (%) por ano e ambiente",
        "S9 — tabulador interativo (eixos livres)",
    ],
}

_DIMS_LABEL = list(DIMENSOES.keys())

_PREDEFINIDOS_SUST = [
    ("Ambiente × Classe (inclusões, agrupado)",           "ambiente",        "classe",            "inclusoes", "group"),
    ("Ambiente × Sustentação (inclusões, agrupado)",      "ambiente",        "teve_sustentacao",  "inclusoes", "group"),
    ("Ano × Sustentação (inclusões, empilhado 100%)",     "ano",             "teve_sustentacao",  "inclusoes", "100%"),
    ("Classe × Sustentação (inclusões, empilhado 100%)",  "classe",          "teve_sustentacao",  "inclusoes", "100%"),
    ("Tipo de Questão × Sustentação (inclusões)",         "tipo_questao",    "teve_sustentacao",  "inclusoes", "group"),
    ("Macro-Desfecho × Sustentação (inclusões)",          "macro_desfecho",  "teve_sustentacao",  "inclusoes", "group"),
]
_LABELS_PRE = [p[0] for p in _PREDEFINIDOS_SUST]

_TABELA_SPECS: dict[int, tuple[str, str | None]] = {
    0: ("ambiente", "teve_sustentacao"),
    1: ("ano", "teve_sustentacao"),
    2: ("ano", "classe"),
    3: ("ano", "tipo_questao"),
    4: ("ambiente", "teve_sustentacao"),
}


def _build_tabela(df: pd.DataFrame, spec: tuple[str, str | None]) -> pd.DataFrame:
    col_linha, col_grupo = spec
    d = df.copy()
    d["tipo_questao"] = d["tipo_questao"].replace({"IJ": "QI"})
    d["teve_sustentacao"] = d["teve_sustentacao"].map(
        {True: "Com sustentação", False: "Sem sustentação"}
    )
    tab = d.groupby([col_linha, col_grupo], observed=True).size().reset_index(name="n")
    pvt = tab.pivot_table(index=col_linha, columns=col_grupo, values="n", fill_value=0)
    pvt["Total"] = pvt.sum(axis=1)
    pvt.loc["Total"] = pvt.sum()
    pvt = pvt.reset_index()
    pvt[pvt.columns[0]] = pvt[pvt.columns[0]].astype(str)
    return pvt


def _render_tabela(df: pd.DataFrame, idx: int) -> None:
    spec = _TABELA_SPECS.get(idx)
    if spec is None:
        return
    with st.expander("📊 Dados da tabulação"):
        tab = _build_tabela(df, spec)
        fmt = {c: "{:,.0f}" for c in tab.columns if c != tab.columns[0]}
        st.dataframe(tab.style.format(fmt, na_rep="—"), width="stretch", height=280)


def _render_interactive_tabulador(df: pd.DataFrame) -> None:
    st.subheader("Tabulador Interativo")
    st.caption("Configure livremente os eixos, agrupamento e modo de barras.")

    col_pre, _ = st.columns([2, 1])
    with col_pre:
        pre_escolha = st.selectbox(
            "🔖 Pré-definidos",
            options=["— ou configure manualmente abaixo —"] + _LABELS_PRE,
            index=0,
            key="sust_predefinido",
        )

    if pre_escolha.startswith("—"):
        def_x, def_g, def_m, def_bm = 0, 1, 0, 0
    else:
        _, px, pg, pm, pbm = next(p for p in _PREDEFINIDOS_SUST if p[0] == pre_escolha)
        def_x  = _DIMS_LABEL.index(next(k for k, v in DIMENSOES.items() if v == px))
        def_g  = _DIMS_LABEL.index(next(k for k, v in DIMENSOES.items() if v == pg))
        def_m  = ["inclusoes", "processos"].index(pm)
        def_bm = ["group", "stack", "100%"].index(pbm)

    c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 1])
    with c1:
        eixo_x_lbl = st.selectbox("Eixo X",    _DIMS_LABEL, index=def_x, key="sust_tab_x")
    with c2:
        grupo_lbl  = st.selectbox("Cor/Grupo", _DIMS_LABEL, index=def_g, key="sust_tab_g")
    with c3:
        metrica = st.selectbox(
            "Métrica", ["inclusoes", "processos"], index=def_m, key="sust_tab_m",
            format_func=lambda v: "Inclusões em pauta" if v == "inclusoes" else "Processos distintos",
        )
    with c4:
        barmode = st.selectbox(
            "Modo", ["group", "stack", "100%"], index=def_bm, key="sust_tab_bm",
            format_func=lambda v: {"group": "Agrupado", "stack": "Empilhado", "100%": "Empilhado 100%"}[v],
        )
    with c5:
        show_values = st.checkbox("Exibir valores", value=False, key="sust_tab_sv")

    eixo_x = DIMENSOES[eixo_x_lbl]
    grupo  = DIMENSOES[grupo_lbl]

    if eixo_x == grupo:
        st.warning("Eixo X e Cor/Grupo não podem ser a mesma dimensão.")
        return

    st.plotly_chart(gt10_tabulador(df, eixo_x, grupo, metrica, barmode, show_values), width="stretch")

    st.markdown("---")
    st.subheader("Tabela — mesmos eixos")
    d = df.copy()
    d["tipo_questao"] = d["tipo_questao"].replace({"IJ": "QI"})
    if metrica == "processos":
        d = d.drop_duplicates("incidente")
    tab = d.groupby([eixo_x, grupo], observed=True).size().reset_index(name="n")
    if barmode == "100%":
        totais = tab.groupby(eixo_x)["n"].transform("sum")
        tab["n"] = (tab["n"] / totais * 100).round(1)
    pvt = tab.pivot_table(index=eixo_x, columns=grupo, values="n", fill_value=0)
    pvt["Total"] = pvt.sum(axis=1)
    pvt.loc["Total"] = pvt.sum()
    pvt = pvt.reset_index()
    pvt[pvt.columns[0]] = pvt[pvt.columns[0]].astype(str)
    fmt = {c: "{:,.0f}" for c in pvt.columns if pvt[c].dtype.kind in "iuf"}
    st.dataframe(pvt.style.format(fmt, na_rep="—"), width="stretch", height=280)


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

    if fn is None:
        _render_interactive_tabulador(df)
        return

    st.subheader(subtitulo)
    st.caption(descricao)

    show_values = st.checkbox("Exibir valores", value=True, key=f"sust_sv_{idx}")

    if idx <= 3:
        ambiente = st.selectbox(
            "Âmbito", ["Plenário Virtual", "Plenário Presencial"],
            key=f"sust_amb_{idx}",
        )
        fig = fn(df, show_values=show_values, ambiente=ambiente)
    else:
        fig = fn(df, show_values=show_values)
    st.plotly_chart(fig, width="stretch")

    _render_tabela(df, idx)
