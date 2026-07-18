"""Renderização da página de Reajuste de Voto."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import (
    gr1_reajuste_filtravel, gr3_anual_filtravel, gr5_classe_filtravel,
)
from pages.tramitacao.plots import gt10_tabulador, DIMENSOES

_DIMS_LABEL = list(DIMENSOES.keys())

_PREDEFINIDOS_TAB = [
    ("Ano × Reajuste (inclusões, empilhado 100%)",    "ano",          "teve_reajuste",  "inclusoes", "100%"),
    ("Ambiente × Reajuste (inclusões, agrupado)",     "ambiente",     "teve_reajuste",  "inclusoes", "group"),
    ("Classe × Reajuste (inclusões, empilhado 100%)", "classe",       "teve_reajuste",  "inclusoes", "100%"),
    ("Tipo de Questão × Reajuste (inclusões)",        "tipo_questao", "teve_reajuste",  "inclusoes", "group"),
    ("Macro-Desfecho × Reajuste (inclusões)",         "macro_desfecho", "teve_reajuste", "inclusoes", "group"),
    ("Desfecho Detalhado × Reajuste (inclusões)",     "desfecho",       "teve_reajuste",  "inclusoes", "group"),
]
_LABELS_PRE_TAB = [p[0] for p in _PREDEFINIDOS_TAB]


def _gr_tipo_vs_reajuste(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False):
    return gt10_tabulador(df, "tipo_questao", "teve_reajuste", "inclusoes", "group", show_values)


def _gr_desfecho_vs_reajuste(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False):
    import re
    fig = gt10_tabulador(df, "desfecho", "teve_reajuste", "inclusoes", "group", show_values)
    for trace in fig.data:
        trace.x = tuple(
            re.sub(r"\s*-\s*", "\n", str(v), count=1)
            if isinstance(v, str) else v
            for v in trace.x
        )
    return fig


_CATALOGO = [
    (
        "R1/R2 — Proporção com/sem reajuste (Plenário Virtual e Plenário Presencial)",
        "Reajuste de Voto — período total",
        "Pizza com a proporção de inclusões que tiveram ao menos um reajuste de voto. "
        "Selecione o âmbito.",
        gr1_reajuste_filtravel,
    ),
    (
        "R3/R4 — Reajustes por Ano (Plenário Virtual e Plenário Presencial)",
        "Reajuste de Voto por Ano",
        "Volume anual de inclusões que registraram reajuste de voto. "
        "Anos sem ocorrência aparecem com valor zero. Selecione o âmbito.",
        gr3_anual_filtravel,
    ),
    (
        "R5/R6 — Reajustes por Ano e Classe (Plenário Virtual e Plenário Presencial)",
        "Reajuste de Voto por Ano e Classe",
        "Barras agrupadas por classe (ADI, ADPF, ADC, ADO) mostrando o volume anual "
        "de reajustes de voto. Selecione o âmbito.",
        gr5_classe_filtravel,
    ),
    (
        "R7 — Tipo de Questão × Reajuste",
        "Tipo de Questão × Reajuste (inclusões)",
        "Distribuição das inclusões com/sem reajuste por tipo de questão (PR/RC/QI).",
        _gr_tipo_vs_reajuste,
    ),
    (
        "R8 — Desfecho Detalhado × Reajuste",
        "Desfecho Detalhado × Reajuste (inclusões)",
        "Distribuição das inclusões com/sem reajuste por desfecho detalhado.",
        _gr_desfecho_vs_reajuste,
    ),
    (
        "R9 — Tabulador Gráfico Interativo",
        "Tabulador Gráfico Interativo",
        "Configure livremente eixos, agrupamento e modo de barras para explorar "
        "cruzamentos entre dimensões.",
        None,
    ),
]
_LABELS = [item[0] for item in _CATALOGO]

_SUMARIO = {
    "Período total (R1/R2)": [
        "R1/R2 — proporção com/sem reajuste (Plenário Virtual e Plenário Presencial)",
    ],
    "Evolução anual (R3/R4)": [
        "R3/R4 — volume de reajustes por ano (Plenário Virtual e Plenário Presencial)",
    ],
    "Por classe (R5/R6)": [
        "R5/R6 — reajustes por ano e classe (Plenário Virtual e Plenário Presencial)",
    ],
    "Distribuição (R7–R8)": [
        "R7 — reajuste por tipo de questão",
        "R8 — reajuste por desfecho detalhado",
    ],
    "Livre (R9)": [
        "R9 — tabulador gráfico interativo",
    ],
}

_TABELA_SPECS: dict[int, tuple[str, str | None]] = {
    0: ("ambiente", "teve_reajuste"),
    1: ("ano", "teve_reajuste"),
    2: ("ano", "classe"),
    3: ("tipo_questao", "teve_reajuste"),
    4: ("desfecho", "teve_reajuste"),
}


def _build_tabela(df: pd.DataFrame, spec: tuple[str, str | None]) -> pd.DataFrame:
    col_linha, col_grupo = spec
    d = df.copy()
    d["tipo_questao"] = d["tipo_questao"].replace({"IJ": "QI"})
    d["teve_reajuste"] = d["teve_reajuste"].map({True: "Com reajuste", False: "Sem reajuste"})

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


# ── Ponto de entrada ──────────────────────────────────────────────────────────

def _render_interactive_tabulador(df: pd.DataFrame) -> None:
    st.subheader("Tabulador Gráfico Interativo")
    st.caption("Configure livremente os eixos, agrupamento e modo de barras.")

    col_pre, _ = st.columns([2, 1])
    with col_pre:
        pre_escolha = st.selectbox(
            "🔖 Pré-definidos",
            options=["— ou configure manualmente abaixo —"] + _LABELS_PRE_TAB,
            index=0,
            key="reaj_predefinido",
        )

    if pre_escolha.startswith("—"):
        def_x, def_g, def_m, def_bm = 0, 1, 0, 0
    else:
        _, px, pg, pm, pbm = next(p for p in _PREDEFINIDOS_TAB if p[0] == pre_escolha)
        def_x  = _DIMS_LABEL.index(next(k for k, v in DIMENSOES.items() if v == px))
        def_g  = _DIMS_LABEL.index(next(k for k, v in DIMENSOES.items() if v == pg))
        def_m  = ["inclusoes", "processos"].index(pm)
        def_bm = ["group", "stack", "100%"].index(pbm)

    c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 1])
    with c1:
        eixo_x_lbl = st.selectbox("Eixo X",    _DIMS_LABEL, index=def_x, key="reaj_tab_x")
    with c2:
        eixo_y_lbl  = st.selectbox("Eixo Y", _DIMS_LABEL, index=def_g, key="reaj_tab_y")
    with c3:
        metrica = st.selectbox(
            "Métrica", ["inclusoes", "processos"], index=def_m, key="reaj_tab_m",
            format_func=lambda v: "Inclusões em pauta" if v == "inclusoes" else "Processos distintos",
        )
    with c4:
        barmode = st.selectbox(
            "Modo", ["group", "stack", "100%"], index=def_bm, key="reaj_tab_bm",
            format_func=lambda v: {"group": "Agrupado", "stack": "Empilhado", "100%": "Empilhado 100%"}[v],
        )
    with c5:
        show_values_tab = st.checkbox("Exibir valores", value=False, key="reaj_tab_sv")

    eixo_x = DIMENSOES[eixo_x_lbl]
    eixo_y  = DIMENSOES[eixo_y_lbl]

    if eixo_x == eixo_y:
        st.warning("Eixo X e Eixo Y não podem ser a mesma dimensão.")
        return

    st.plotly_chart(
        gt10_tabulador(df, eixo_x, eixo_y, metrica, barmode, show_values_tab),
        width="stretch",
    )

    st.markdown("---")
    st.subheader("Tabela — mesmos eixos")
    d = df.copy()
    d["tipo_questao"] = d["tipo_questao"].replace({"IJ": "QI"})
    if metrica == "processos":
        d = d.drop_duplicates("incidente")
    tab = d.groupby([eixo_x, eixo_y], observed=True).size().reset_index(name="n")
    if barmode == "100%":
        totais = tab.groupby(eixo_x)["n"].transform("sum")
        tab["n"] = (tab["n"] / totais * 100).round(1)
    pvt = tab.pivot_table(index=eixo_x, columns=eixo_y, values="n", fill_value=0)
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
        key="reajuste_selectbox",
    )

    idx = _LABELS.index(escolha)
    _, subtitulo, descricao, fn = _CATALOGO[idx]

    if fn is None:
        _render_interactive_tabulador(df)
        return

    st.subheader(subtitulo)
    st.caption(descricao)

    show_values = st.checkbox("Exibir valores", value=True, key=f"reajuste_sv_{idx}")

    if idx == 0:
        fig = fn(df, show_values=show_values)
    elif idx <= 2:
        ambiente = st.selectbox(
            "Âmbito", ["Plenário Virtual", "Plenário Presencial"],
            key=f"reajuste_amb_{idx}",
        )
        fig = fn(df, show_values=show_values, ambiente=ambiente)
    else:
        fig = fn(df, show_values=show_values)
    st.plotly_chart(fig, width="stretch")

    _render_tabela(df, idx)
