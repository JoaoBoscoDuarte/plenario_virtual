"""Renderização da página de Sustentação Oral."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import (
    gs1_pizza_pv, gs2_pizza_pp,
    gs3_anual_pv, gs4_anual_pp,
    gs5_classe_pv, gs6_classe_pp,
    gs7_tipo_pv, gs8_taxa_ambiente,
)
from pages.tramitacao.plots import gt10_tabulador, DIMENSOES

_CATALOGO = [
    (
        "S1 — Proporção com/sem sustentação — PV (período total)",
        "Sustentação Oral — Plenário Virtual (período total)",
        "Pizza com a proporção de inclusões que tiveram sustentação oral realizada "
        "no Plenário Virtual ao longo de todo o período (2020–2025).",
        gs1_pizza_pv,
    ),
    (
        "S2 — Proporção com/sem sustentação — PP (período total)",
        "Sustentação Oral — Plenário Presencial (período total)",
        "Mesmo recorte do S1 para o Plenário Presencial.",
        gs2_pizza_pp,
    ),
    (
        "S3 — Sustentações por Ano — PV",
        "Sustentação Oral por Ano — Plenário Virtual",
        "Volume anual de inclusões com sustentação oral no PV. "
        "Anos sem ocorrência aparecem com valor zero.",
        gs3_anual_pv,
    ),
    (
        "S4 — Sustentações por Ano — PP",
        "Sustentação Oral por Ano — Plenário Presencial",
        "Mesmo recorte do S3 para o Plenário Presencial.",
        gs4_anual_pp,
    ),
    (
        "S5 — Sustentações por Ano e Classe — PV",
        "Sustentação Oral por Ano e Classe — Plenário Virtual",
        "Barras agrupadas por classe (ADI, ADPF, ADC, ADO) com linha do total no eixo secundário. PV.",
        gs5_classe_pv,
    ),
    (
        "S6 — Sustentações por Ano e Classe — PP",
        "Sustentação Oral por Ano e Classe — Plenário Presencial",
        "Mesmo recorte do S5 para o Plenário Presencial.",
        gs6_classe_pp,
    ),
    (
        "S7 — Sustentações por Ano e Tipo de Questão — PV",
        "Sustentação Oral por Ano e Tipo de Questão — Plenário Virtual",
        "Barras agrupadas por tipo de questão (PR / RC / QI) com linha do total. "
        "IJ renomeado para QI na exibição. Apenas PV.",
        gs7_tipo_pv,
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
    "Período total (S1–S2)": [
        "S1 — proporção com/sem sustentação — PV",
        "S2 — proporção com/sem sustentação — PP",
    ],
    "Evolução anual (S3–S4)": [
        "S3 — volume de sustentações por ano — PV",
        "S4 — volume de sustentações por ano — PP",
    ],
    "Por classe e tipo (S5–S7)": [
        "S5 — sustentações por ano e classe — PV",
        "S6 — sustentações por ano e classe — PP",
        "S7 — sustentações por ano e tipo de questão — PV",
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


# ── helpers ───────────────────────────────────────────────────────────────────

def _build_dados_brutos(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "nome_processo", "classe", "relator", "ano", "ambiente",
        "tipo_questao", "desfecho", "macro_desfecho", "teve_sustentacao",
    ]
    tab = df[cols].copy()
    tab["tipo_questao"] = tab["tipo_questao"].replace({"IJ": "QI"})
    return tab.rename(columns={
        "nome_processo":   "Processo",
        "classe":          "Classe",
        "relator":         "Relator",
        "ano":             "Ano",
        "ambiente":        "Ambiente",
        "tipo_questao":    "Tipo",
        "desfecho":        "Desfecho",
        "macro_desfecho":  "Macro-Desfecho",
        "teve_sustentacao": "Sustentação",
    }).sort_values(["Ano", "Processo"]).reset_index(drop=True)


def _build_tabulador(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for ano in sorted(df["ano"].unique()):
        df_ano = df[df["ano"] == ano]
        row: dict = {"Ano": int(ano)}
        for amb_label, amb_key in [("PV", "Plenário Virtual"), ("PP", "Plenário Presencial")]:
            df_amb = df_ano[df_ano["ambiente"] == amb_key]
            total = len(df_amb)
            com   = int(df_amb["teve_sustentacao"].sum())
            taxa  = round(com / total * 100, 1) if total else 0.0
            row[f"{amb_label} — Total"] = total
            row[f"{amb_label} — Com sustentação"] = com
            row[f"{amb_label} — Taxa (%)"]        = taxa
            for cls in ["ADI", "ADPF", "ADC", "ADO"]:
                row[f"{amb_label} — {cls}"] = int(
                    df_amb[df_amb["classe"] == cls]["teve_sustentacao"].sum()
                )
        row["Total — Com sustentação"] = int(df_ano["teve_sustentacao"].sum())
        row["Total — Taxa (%)"]        = round(
            df_ano["teve_sustentacao"].sum() / len(df_ano) * 100, 1
        ) if len(df_ano) else 0.0
        rows.append(row)
    return pd.DataFrame(rows).set_index("Ano")


def _render_tabulador_grafico(df: pd.DataFrame) -> None:
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


def _render_tabela_consolidada(df: pd.DataFrame) -> None:
    st.subheader("Tabulador Consolidado por Ano")
    st.caption("Contagem de inclusões com sustentação oral por ano, ambiente e classe.")

    col_a, col_b, col_c = st.columns([3, 2, 2])
    with col_a:
        anos = sorted(df["ano"].unique())
        periodo = st.slider(
            "Período", int(min(anos)), int(max(anos)),
            (int(min(anos)), int(max(anos))), step=1, key="stab_periodo",
        )
    with col_b:
        classes_sel = st.multiselect(
            "Classes", ["ADI", "ADPF", "ADC", "ADO"],
            default=["ADI", "ADPF", "ADC", "ADO"], key="stab_classes",
        )
    with col_c:
        ambientes_sel = st.multiselect(
            "Ambientes", ["PV", "PP"], default=["PV", "PP"], key="stab_amb",
        )

    ai, af  = periodo
    sel_cls = classes_sel  if classes_sel  else ["ADI", "ADPF", "ADC", "ADO"]
    sel_amb = ambientes_sel if ambientes_sel else ["PV", "PP"]
    amb_map = {"PV": "Plenário Virtual", "PP": "Plenário Presencial"}

    df_f = df[
        df["ano"].between(ai, af) &
        df["classe"].isin(sel_cls) &
        df["ambiente"].isin([amb_map[a] for a in sel_amb])
    ]

    tabela = _build_tabulador(df_f)
    keep = []
    for col in tabela.columns:
        partes = col.split(" — ")
        if partes[0] == "Total":
            keep.append(col)
        elif partes[0] in sel_amb:
            if len(partes) < 2 or partes[1] in sel_cls or partes[1] in ("Total", "Com sustentação", "Taxa (%)"):
                keep.append(col)
    tabela = tabela[[c for c in keep if c in tabela.columns]]
    fmt = {c: "{:.1f}%" if "Taxa" in c else "{:,.0f}" for c in tabela.columns}
    st.caption(f"{len(tabela):,} anos exibidos")
    st.dataframe(tabela.style.format(fmt, na_rep="—"), width="stretch", height=320)


def _render_dados_brutos(df: pd.DataFrame) -> None:
    st.subheader("Dados Brutos")
    st.caption("Uma linha por inclusão em pauta. Use os filtros para explorar.")

    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        anos = sorted(df["ano"].unique())
        periodo = st.slider(
            "Período", int(min(anos)), int(max(anos)),
            (int(min(anos)), int(max(anos))), step=1, key="sbruto_periodo",
        )
    with col_b:
        classes_sel = st.multiselect("Classe", sorted(df["classe"].unique()), key="sbruto_classe")
    with col_c:
        amb_sel = st.multiselect("Ambiente", sorted(df["ambiente"].unique()), key="sbruto_amb")
    with col_d:
        sust_sel = st.selectbox(
            "Sustentação", ["Todos", "Com sustentação", "Sem sustentação"], key="sbruto_sust",
        )

    ai, af = periodo
    tab = _build_dados_brutos(df)
    tab = tab[tab["Ano"].between(ai, af)]
    if classes_sel:
        tab = tab[tab["Classe"].isin(classes_sel)]
    if amb_sel:
        tab = tab[tab["Ambiente"].isin(amb_sel)]
    if sust_sel == "Com sustentação":
        tab = tab[tab["Sustentação"]]
    elif sust_sel == "Sem sustentação":
        tab = tab[~tab["Sustentação"]]

    st.caption(f"{len(tab):,} inclusões exibidas")
    st.dataframe(
        tab,
        width="stretch",
        hide_index=True,
        column_config={
            "Processo":    st.column_config.TextColumn(width="medium"),
            "Relator":     st.column_config.TextColumn(width="medium"),
            "Desfecho":    st.column_config.TextColumn(width="large"),
            "Sustentação": st.column_config.CheckboxColumn(width="small"),
            "Ano":         st.column_config.NumberColumn(width="small"),
        },
    )


# ── Ponto de entrada ──────────────────────────────────────────────────────────

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

    st.subheader(subtitulo)
    st.caption(descricao)

    if idx == len(_CATALOGO) - 1:  # S9 — tabulador
        _render_tabulador_grafico(df)
    else:
        show_values = st.checkbox("Exibir valores", value=True, key=f"sust_sv_{idx}")
        fig = fn(df, show_values=show_values)
        st.plotly_chart(fig, width="stretch")

    st.markdown("---")
    _render_tabela_consolidada(df)

    st.markdown("---")
    _render_dados_brutos(df)
