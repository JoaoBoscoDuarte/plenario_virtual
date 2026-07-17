"""Renderização da página de Reajuste de Voto."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import (
    gr1_pizza_pv, gr2_pizza_pp,
    gr3_anual_pv, gr4_anual_pp,
    gr5_classe_pv, gr6_classe_pp,
)
from pages.tramitacao.plots import gt10_tabulador, DIMENSOES

_DIMS_LABEL = list(DIMENSOES.keys())

_PREDEFINIDOS_REAJ = [
    ("Ano × Reajuste (inclusões, empilhado 100%)",    "ano",          "teve_reajuste",  "inclusoes", "100%"),
    ("Ambiente × Reajuste (inclusões, agrupado)",     "ambiente",     "teve_reajuste",  "inclusoes", "group"),
    ("Classe × Reajuste (inclusões, empilhado 100%)", "classe",       "teve_reajuste",  "inclusoes", "100%"),
    ("Tipo de Questão × Reajuste (inclusões)",        "tipo_questao", "teve_reajuste",  "inclusoes", "group"),
    ("Macro-Desfecho × Reajuste (inclusões)",         "macro_desfecho", "teve_reajuste", "inclusoes", "group"),
]
_LABELS_PRE_REAJ = [p[0] for p in _PREDEFINIDOS_REAJ]

_CATALOGO = [
    (
        "R1 — Proporção com/sem reajuste — PV (período total)",
        "Reajuste de Voto — Plenário Virtual (período total)",
        "Pizza com a proporção de inclusões que tiveram ao menos um reajuste de voto "
        "no Plenário Virtual ao longo de todo o período (2020–2025).",
        gr1_pizza_pv,
    ),
    (
        "R2 — Proporção com/sem reajuste — PP (período total)",
        "Reajuste de Voto — Plenário Físico (período total)",
        "Mesmo recorte do R1 para o Plenário Físico.",
        gr2_pizza_pp,
    ),
    (
        "R3 — Reajustes por Ano — PV",
        "Reajuste de Voto por Ano — Plenário Virtual",
        "Volume anual de inclusões em pauta que registraram reajuste de voto no PV. "
        "Anos sem ocorrência aparecem com valor zero.",
        gr3_anual_pv,
    ),
    (
        "R4 — Reajustes por Ano — PP",
        "Reajuste de Voto por Ano — Plenário Físico",
        "Mesmo recorte do R3 para o Plenário Físico.",
        gr4_anual_pp,
    ),
    (
        "R5 — Reajustes por Ano e Classe — PV",
        "Reajuste de Voto por Ano e Classe — Plenário Virtual",
        "Barras agrupadas por classe (ADI, ADPF, ADC, ADO) mostrando o volume anual "
        "de reajustes de voto no PV.",
        gr5_classe_pv,
    ),
    (
        "R6 — Reajustes por Ano e Classe — PP",
        "Reajuste de Voto por Ano e Classe — Plenário Físico",
        "Mesmo recorte do R5 para o Plenário Físico.",
        gr6_classe_pp,
    ),
]

_LABELS = [item[0] for item in _CATALOGO]

_SUMARIO = {
    "Período total (R1–R2)": [
        "R1 — proporção com/sem reajuste — PV",
        "R2 — proporção com/sem reajuste — PP",
    ],
    "Evolução anual (R3–R4)": [
        "R3 — volume de reajustes por ano — PV",
        "R4 — volume de reajustes por ano — PP",
    ],
    "Por classe (R5–R6)": [
        "R5 — reajustes por ano e classe — PV",
        "R6 — reajustes por ano e classe — PP",
    ],
}


# ── Tabulador consolidado ─────────────────────────────────────────────────────

def _build_tabulador(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for ano in sorted(df["ano"].unique()):
        df_ano = df[df["ano"] == ano]
        row: dict = {"Ano": int(ano)}
        for amb_label, amb_key in [("PV", "Plenário Virtual"), ("PP", "Plenário Físico")]:
            df_amb = df_ano[df_ano["ambiente"] == amb_key]
            total = len(df_amb)
            com   = int(df_amb["teve_reajuste"].sum())
            taxa  = round(com / total * 100, 1) if total else 0.0
            row[f"{amb_label} — Total"] = total
            row[f"{amb_label} — Com reajuste"] = com
            row[f"{amb_label} — Taxa (%)"]     = taxa
            for cls in ["ADI", "ADPF", "ADC", "ADO"]:
                row[f"{amb_label} — {cls}"] = int(
                    df_amb[df_amb["classe"] == cls]["teve_reajuste"].sum()
                )
        row["Total — Com reajuste"] = int(df_ano["teve_reajuste"].sum())
        row["Total — Taxa (%)"]     = round(
            df_ano["teve_reajuste"].sum() / len(df_ano) * 100, 1
        ) if len(df_ano) else 0.0
        rows.append(row)
    return pd.DataFrame(rows).set_index("Ano")


def _render_tabulador(df: pd.DataFrame) -> None:
    st.subheader("Tabulador Consolidado por Ano")
    st.caption(
        "Contagem de inclusões com reajuste de voto por ano, ambiente e classe. "
        "Use os filtros para recortar o período e as colunas de interesse."
    )

    col_a, col_b, col_c = st.columns([3, 2, 2])
    with col_a:
        anos = sorted(df["ano"].unique())
        periodo = st.slider(
            "Período", int(min(anos)), int(max(anos)),
            (int(min(anos)), int(max(anos))), step=1, key="rtab_periodo",
        )
    with col_b:
        classes_sel = st.multiselect(
            "Classes", ["ADI", "ADPF", "ADC", "ADO"],
            default=["ADI", "ADPF", "ADC", "ADO"], key="rtab_classes",
        )
    with col_c:
        ambientes_sel = st.multiselect(
            "Ambientes", ["PV", "PP"], default=["PV", "PP"], key="rtab_amb",
        )

    ai, af   = periodo
    sel_cls  = classes_sel  if classes_sel  else ["ADI", "ADPF", "ADC", "ADO"]
    sel_amb  = ambientes_sel if ambientes_sel else ["PV", "PP"]
    amb_map  = {"PV": "Plenário Virtual", "PP": "Plenário Físico"}

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
            if len(partes) < 2 or partes[1] in sel_cls or partes[1] in ("Total", "Com reajuste", "Taxa (%)"):
                keep.append(col)
    tabela = tabela[[c for c in keep if c in tabela.columns]]

    fmt = {c: "{:.1f}%" if "Taxa" in c else "{:,.0f}" for c in tabela.columns}
    st.caption(f"{len(tabela):,} anos exibidos")
    st.dataframe(tabela.style.format(fmt, na_rep="—"), width="stretch", height=320)


# ── Dados brutos ──────────────────────────────────────────────────────────────

def _build_dados_brutos(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "nome_processo", "classe", "relator", "ano", "ambiente",
        "tipo_questao", "desfecho", "macro_desfecho", "teve_reajuste",
    ]
    tab = df[cols].copy()
    tab["tipo_questao"] = tab["tipo_questao"].replace({"IJ": "QI"})
    return tab.rename(columns={
        "nome_processo":  "Processo",
        "classe":         "Classe",
        "relator":        "Relator",
        "ano":            "Ano",
        "ambiente":       "Ambiente",
        "tipo_questao":   "Tipo",
        "desfecho":       "Desfecho",
        "macro_desfecho": "Macro-Desfecho",
        "teve_reajuste":  "Reajuste",
    }).sort_values(["Ano", "Processo"]).reset_index(drop=True)


def _render_dados_brutos(df: pd.DataFrame) -> None:
    st.subheader("Dados Brutos")
    st.caption("Uma linha por inclusão em pauta. Use os filtros para explorar.")

    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        anos = sorted(df["ano"].unique())
        periodo = st.slider(
            "Período", int(min(anos)), int(max(anos)),
            (int(min(anos)), int(max(anos))), step=1, key="rbruto_periodo",
        )
    with col_b:
        classes_sel = st.multiselect(
            "Classe", sorted(df["classe"].unique()), key="rbruto_classe",
        )
    with col_c:
        amb_sel = st.multiselect(
            "Ambiente", sorted(df["ambiente"].unique()), key="rbruto_amb",
        )
    with col_d:
        reajuste_sel = st.selectbox(
            "Reajuste", ["Todos", "Com reajuste", "Sem reajuste"], key="rbruto_reajuste",
        )

    ai, af = periodo
    tab = _build_dados_brutos(df)
    tab = tab[tab["Ano"].between(ai, af)]
    if classes_sel:
        tab = tab[tab["Classe"].isin(classes_sel)]
    if amb_sel:
        tab = tab[tab["Ambiente"].isin(amb_sel)]
    if reajuste_sel == "Com reajuste":
        tab = tab[tab["Reajuste"]]
    elif reajuste_sel == "Sem reajuste":
        tab = tab[~tab["Reajuste"]]

    st.caption(f"{len(tab):,} inclusões exibidas")
    st.dataframe(
        tab,
        width="stretch",
        hide_index=True,
        column_config={
            "Processo":      st.column_config.TextColumn(width="medium"),
            "Relator":       st.column_config.TextColumn(width="medium"),
            "Desfecho":      st.column_config.TextColumn(width="large"),
            "Reajuste":      st.column_config.CheckboxColumn(width="small"),
            "Ano":           st.column_config.NumberColumn(width="small"),
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
        key="reajuste_selectbox",
    )

    idx = _LABELS.index(escolha)
    _, subtitulo, descricao, fn = _CATALOGO[idx]

    st.subheader(subtitulo)
    st.caption(descricao)
    with st.expander("Critério / Caminho dos dados"):
        st.markdown(
            "- **Fonte:** `data/processed/inclusoes_em_pauta.parquet`  \n"
            "- **Unidade:** inclusão em pauta  \n"
            "- **Período:** 2020–2025"
        )

    # Pizzas (R1/R2) não têm show_values
    is_bar = idx >= 2
    show_values = (
        st.checkbox("Exibir valores", value=True, key=f"reajuste_show_{idx}")
        if is_bar else True
    )
    fig = fn(df, show_values=show_values) if is_bar else fn(df)
    st.plotly_chart(fig, width="stretch")

    st.markdown("---")
    _render_tabulador(df)

    st.markdown("---")
    _render_dados_brutos(df)

    # ── Tabulador gráfico ──────────────────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Tabulador Gráfico Interativo")
    st.caption("Configure livremente os eixos, agrupamento e modo de barras.")

    col_pre, _ = st.columns([2, 1])
    with col_pre:
        pre_escolha = st.selectbox(
            "🔖 Pré-definidos",
            options=["— ou configure manualmente abaixo —"] + _LABELS_PRE_REAJ,
            index=0,
            key="reaj_predefinido",
        )

    if pre_escolha.startswith("—"):
        def_x, def_g, def_m, def_bm = 0, 1, 0, 0
    else:
        _, px, pg, pm, pbm = next(p for p in _PREDEFINIDOS_REAJ if p[0] == pre_escolha)
        def_x  = _DIMS_LABEL.index(next(k for k, v in DIMENSOES.items() if v == px))
        def_g  = _DIMS_LABEL.index(next(k for k, v in DIMENSOES.items() if v == pg))
        def_m  = ["inclusoes", "processos"].index(pm)
        def_bm = ["group", "stack", "100%"].index(pbm)

    c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 1])
    with c1:
        eixo_x_lbl = st.selectbox("Eixo X",    _DIMS_LABEL, index=def_x, key="reaj_tab_x")
    with c2:
        grupo_lbl  = st.selectbox("Cor/Grupo", _DIMS_LABEL, index=def_g, key="reaj_tab_g")
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
    grupo  = DIMENSOES[grupo_lbl]

    if eixo_x == grupo:
        st.warning("Eixo X e Cor/Grupo não podem ser a mesma dimensão.")
    else:
        st.plotly_chart(
            gt10_tabulador(df, eixo_x, grupo, metrica, barmode, show_values_tab),
            width="stretch",
        )
