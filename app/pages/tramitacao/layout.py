"""Renderização da página de Tramitação por Ambiente."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import (
    gt1_tramitacao,
    gt2_tram_por_classe,
    gt3_tram_por_tipo,
    gt4_ambos_por_tipo,
    gt5_macro_por_tram,
    gt6_desfecho_por_tram,
    gt7_classe_por_tram,
    gt8_tipo_por_tram,
    gt9_taxa_conclusao,
    gt10_tabulador,
    gt11_proc_ano_ambiente,
    gt12_proc_tramitacao_primeiro_ano,
    gt13_tramitacao_periodo,
    DIMENSOES,
)

# ── Catálogo T1–T9 ────────────────────────────────────────────────────────────
_CATALOGO = [
    (
        "T1 — Tramitação por Ambiente (pizza geral)",
        "Tramitação por Ambiente — Processos CC (2020–2025)",
        "Pizza com a distribuição dos processos distintos por ambiente: "
        "só PV, só PP ou ambos.",
        gt1_tramitacao,
    ),
    (
        "T2 — Tramitação por Ambiente e Classe",
        "Tramitação por Ambiente e Classe — Processos CC (2020–2025)",
        "Barras agrupadas por ambiente de tramitação (só PV / só PP / ambos) "
        "para cada classe processual (ADI, ADPF, ADC, ADO).",
        gt2_tram_por_classe,
    ),
    (
        "T3 — Tramitação por Ambiente e Tipo de Questão",
        "Tramitação por Ambiente e Tipo de Questão — Processos CC (2020–2025)",
        "Barras agrupadas por ambiente de tramitação para cada tipo de questão "
        "(PR / RC / QI). IJ renomeado para QI.",
        gt3_tram_por_tipo,
    ),
    (
        "T4 — Processos em Ambos os Ambientes por Tipo de Questão",
        "Processos em Ambos os Ambientes por Tipo de Questão (2020–2025)",
        "Recorte dos processos que tramitaram em ambos os ambientes, "
        "distribuídos por tipo de questão (PR / RC / QI).",
        gt4_ambos_por_tipo,
    ),
    (
        "T5 — Macro-Desfecho por Ambiente de Tramitação",
        "Macro-Desfecho por Ambiente de Tramitação — Inclusões (2020–2025)",
        "Volume de inclusões concluídas e não concluídas em cada "
        "grupo de tramitação (só PV / só PP / ambos).",
        gt5_macro_por_tram,
    ),
    (
        "T6 — Desfecho Detalhado por Ambiente de Tramitação",
        "Desfecho Detalhado por Ambiente de Tramitação — Inclusões (2020–2025)",
        "Os 7 desfechos detalhados (unânime, maioria, pedido de vista etc.) "
        "para cada grupo de tramitação.",
        gt6_desfecho_por_tram,
    ),
    (
        "T7 — Distribuição por Classe dentro de cada Ambiente",
        "Distribuição por Classe — por Ambiente de Tramitação (2020–2025)",
        "Uma pizza por ambiente (só PV / só PP / ambos) mostrando a composição "
        "por classe processual.",
        gt7_classe_por_tram,
    ),
    (
        "T8 — Distribuição por Tipo de Questão dentro de cada Ambiente",
        "Distribuição por Tipo de Questão — por Ambiente de Tramitação (2020–2025)",
        "Uma pizza por ambiente (só PV / só PP / ambos) mostrando a composição "
        "por tipo de questão.",
        gt8_tipo_por_tram,
    ),
    (
        "T9 — Taxa de Conclusão por Ambiente e Classe (%)",
        "Taxa de Conclusão (%) por Ambiente de Tramitação e Classe (2020–2025)",
        "Percentual de inclusões concluídas para cada combinação de ambiente de "
        "tramitação e classe processual.",
        gt9_taxa_conclusao,
    ),
    (
        "T11 — Processos por Ano e Ambiente",
        "Processos distintos por ano e ambiente (2020–2025)",
        "Cada processo aparece uma vez por ano-ambiente onde foi pautado. "
        "Barra por ambiente com total geral no eixo secundário.",
        gt11_proc_ano_ambiente,
    ),
    (
        "T12 — Processos por Tipo de Tramitação",
        "Processos por tipo de tramitação, por ano sem repetição (2020–2025)",
        "Cada processo conta uma única vez: ano da primeira inclusão, "
        "categoria conforme todo o histórico (Só Virtual / Só Físico / Ambos).",
        gt12_proc_tramitacao_primeiro_ano,
    ),
    (
        "T13 — Processos por Tipo de Tramitação (período total)",
        "Processos por tipo de tramitação — 2020–2025",
        "Cada processo aparece uma única vez, classificado pelo(s) ambiente(s) "
        "em que tramitou ao longo de todo o período.",
        gt13_tramitacao_periodo,
    ),
    (
        "T10 — Tabulador Interativo",
        "Tabulador Interativo — Tramitação por Ambiente (2020–2025)",
        "Configure livremente os eixos, agrupamento, métrica e modo de barras.",
        None,
    ),
]

_LABELS = [item[0] for item in _CATALOGO]

_SUMARIO = {
    "Visão geral (T1–T4, T13)": [
        "T1 — tramitação por ambiente (pizza)",
        "T2 — tramitação por ambiente e classe",
        "T3 — tramitação por ambiente e tipo de questão",
        "T4 — processos em ambos os ambientes por tipo",
        "T13 — processos por tipo de tramitação (período total)",
    ],
    "Detalhamento (T5–T9)": [
        "T5 — macro-desfecho por tramitação",
        "T6 — desfecho detalhado por tramitação",
        "T7 — distribuição por classe por ambiente",
        "T8 — distribuição por tipo por ambiente",
        "T9 — taxa de conclusão por tramitação e classe",
    ],
    "Temporal (T11–T12)": [
        "T11 — processos por ano e ambiente",
        "T12 — processos por tipo de tramitação (sem repetição)",
    ],
    "Livre (T10)": [
        "T10 — tabulador interativo (eixos livres)",
    ],
}

_PREDEFINIDOS = [
    ("Ambiente × Classe (inclusões, agrupado)",          "tramitacao",   "classe",         "inclusoes", "group"),
    ("Ambiente × Macro-Desfecho (inclusões, agrupado)",  "tramitacao",   "macro_desfecho", "inclusoes", "group"),
    ("Ambiente × Tipo de Questão (processos, agrupado)", "tramitacao",   "tipo_questao",   "processos", "group"),
    ("Classe × Ambiente (inclusões, empilhado 100%)",    "classe",       "tramitacao",     "inclusoes", "100%"),
    ("Classe × Macro-Desfecho (inclusões, empilhado)",   "classe",       "macro_desfecho", "inclusoes", "stack"),
    ("Ano × Ambiente (inclusões, empilhado)",            "ano",          "tramitacao",     "inclusoes", "stack"),
    ("Ano × Macro-Desfecho (inclusões, empilhado 100%)", "ano",          "macro_desfecho", "inclusoes", "100%"),
    ("Tipo de Questão × Desfecho (inclusões, agrupado)", "tipo_questao", "macro_desfecho", "inclusoes", "group"),
]
_LABELS_PRE = [p[0] for p in _PREDEFINIDOS]
_DIMS_LABEL = list(DIMENSOES.keys())

_TABELA_SPECS: dict[int, tuple[str, str | None]] = {
    0: ("tramitacao", None),
    1: ("classe", "tramitacao"),
    2: ("tipo_questao", "tramitacao"),
    4: ("tramitacao", "macro_desfecho"),
    5: ("tramitacao", "desfecho"),
    8: ("tramitacao", "classe"),
    9: ("ano", "ambiente"),
    10: ("ano", "tramitacao"),
}


def _build_tabela(df: pd.DataFrame, spec: tuple[str, str | None]) -> pd.DataFrame:
    col_linha, col_grupo = spec
    d = df.copy()
    d["tipo_questao"] = d["tipo_questao"].replace({"IJ": "QI"})
    d["ambiente"] = d["ambiente"].replace({"Plenário Presencial": "Plenário Físico"})
    if col_grupo is None:
        tab = d[col_linha].value_counts().reset_index()
        tab.columns = [col_linha, "n"]
        pvt = tab.set_index(col_linha)
        pvt.loc["Total"] = pvt["n"].sum()
        pvt = pvt.reset_index()
        pvt[pvt.columns[0]] = pvt[pvt.columns[0]].astype(str)
        return pvt
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


def _render_fig(fn, df: pd.DataFrame, show_values: bool) -> None:
    try:
        result = fn(df, show_values=show_values)
    except TypeError:
        result = fn(df)
    if isinstance(result, dict):
        if not result:
            st.info("Sem dados para exibir.")
            return
        subtabs = st.tabs(list(result.keys()))
        for tab, fig in zip(subtabs, result.values()):
            with tab:
                st.plotly_chart(fig, width="stretch")
    else:
        st.plotly_chart(result, width="stretch")


def _render_tabulador(df: pd.DataFrame, key_suffix: str) -> None:
    col_pre, _ = st.columns([2, 1])
    with col_pre:
        pre_escolha = st.selectbox(
            "🔖 Pré-definidos",
            options=["— ou configure manualmente abaixo —"] + _LABELS_PRE,
            index=0,
            key=f"tab_predefinido_{key_suffix}",
        )

    if pre_escolha.startswith("—"):
        def_x, def_g, def_m, def_bm = 0, 1, 0, 0
    else:
        _, px, pg, pm, pbm = next(p for p in _PREDEFINIDOS if p[0] == pre_escolha)
        def_x  = _DIMS_LABEL.index(next(k for k, v in DIMENSOES.items() if v == px))
        def_g  = _DIMS_LABEL.index(next(k for k, v in DIMENSOES.items() if v == pg))
        def_m  = ["inclusoes", "processos"].index(pm)
        def_bm = ["group", "stack", "100%"].index(pbm)

    c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 1])
    with c1:
        eixo_x_lbl = st.selectbox("Eixo X",    _DIMS_LABEL, index=def_x, key=f"tab_x_{key_suffix}")
    with c2:
        grupo_lbl  = st.selectbox("Cor/Grupo", _DIMS_LABEL, index=def_g, key=f"tab_g_{key_suffix}")
    with c3:
        metrica = st.selectbox(
            "Métrica", ["inclusoes", "processos"], index=def_m, key=f"tab_m_{key_suffix}",
            format_func=lambda v: "Inclusões em pauta" if v == "inclusoes" else "Processos distintos",
        )
    with c4:
        barmode = st.selectbox(
            "Modo", ["group", "stack", "100%"], index=def_bm, key=f"tab_bm_{key_suffix}",
            format_func=lambda v: {"group": "Agrupado", "stack": "Empilhado", "100%": "Empilhado 100%"}[v],
        )
    with c5:
        show_values = st.checkbox("Exibir valores", value=False, key=f"tab_sv_{key_suffix}")

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
        key="tramitacao_selectbox",
    )

    idx = _LABELS.index(escolha)
    _, subtitulo, descricao, fn = _CATALOGO[idx]

    st.subheader(subtitulo)
    st.markdown(descricao)

    if idx == len(_CATALOGO) - 1:  # T10
        _render_tabulador(df, key_suffix="main")
    else:
        show_values = st.checkbox("Exibir valores", value=False, key=f"tram_sv_{idx}")
        _render_fig(fn, df, show_values)

    _render_tabela(df, idx)
