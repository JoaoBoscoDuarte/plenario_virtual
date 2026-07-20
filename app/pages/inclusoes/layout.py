"""Renderização da página de Inclusões em Pauta."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import (
    g5_anual_ambiente, g6_classe_filtravel, g8_desfecho_filtravel,
    g10_macro_anual_filtravel, g12_concluidos_filtravel,
    g14_nao_concluidos_classe_filtravel, g16_concluidos_classe_filtravel,
    g18_nc_tipo_filtravel, g20_c_tipo_filtravel,
    g22_cat_periodo_filtravel, g24_cat_anual_filtravel,
    g26_cat_tipo_periodo_filtravel, g28_cat_tipo_anual_filtravel,
    g30_nc_cat_anual_filtravel, g32_nc_cat_classe_filtravel,
    g34_nc_cat_tipo_filtravel,
    _categoria_desfecho, _categoria_nc, _refinar_motivos_diversos,
    g_pauta_concluidos,
)
from pages.tramitacao.plots import gt10_tabulador, DIMENSOES

_DIMS_LABEL = list(DIMENSOES.keys())

_PREDEFINIDOS_TAB = [
    ("Ano × Ambiente (inclusões, agrupado)",           "ano",      "ambiente",       "inclusoes", "group"),
    ("Ano × Classe (inclusões, empilhado)",            "ano",      "classe",         "inclusoes", "stack"),
    ("Ano × Tipo de Questão (inclusões, agrupado)",    "ano",      "tipo_questao",   "inclusoes", "group"),
    ("Ambiente × Classe (inclusões, agrupado)",         "ambiente", "classe",         "inclusoes", "group"),
    ("Ambiente × Macro-Desfecho (inclusões, 100%)",    "ambiente", "macro_desfecho", "inclusoes", "100%"),
    ("Classe × Macro-Desfecho (inclusões, agrupado)",   "classe",   "macro_desfecho", "inclusoes", "group"),
    ("Classe × Desfecho Detalhado (inclusões)",         "classe",   "desfecho",       "inclusoes", "group"),
    ("Tipo de Questão × Macro-Desfecho (inclusões)",    "tipo_questao", "macro_desfecho", "inclusoes", "group"),
    ("Tipo de Questão × Desfecho Detalhado (inclusões)","tipo_questao", "desfecho",     "inclusoes", "group"),
]
_LABELS_PRE_TAB = [p[0] for p in _PREDEFINIDOS_TAB]

# Catálogo: (label do selectbox, subtítulo, descrição, callable)
# Para gráficos que retornam dict, o callable retorna dict e _render trata.
_CATALOGO: list[tuple[str, str, str, object]] = [
    # ── Inclusões em Pauta ────────────────────────────────────────────────────
    (
        "G5 — Inclusões por Ano e Ambiente (Plenário Virtual vs Plenário Presencial)",
        "Inclusões em Pauta por Ano e Ambiente",
        "Comparação anual do volume de inclusões em pauta entre o Plenário Virtual e o Plenário Presencial. "
        "Inclui pizza com a proporção acumulada no período.",
        g5_anual_ambiente,
    ),
    (
        "G6/G7 — Inclusões por Classe (Plenário Virtual e Plenário Presencial)",
        "Inclusões por Classe",
        "Barras agrupadas por classe (ADI, ADPF, ADC, ADO) com linha do total geral no eixo secundário. "
        "Selecione o âmbito (Plenário Virtual / Plenário Presencial) e filtre as classes desejadas. "
        "Inclui pizza com a distribuição por classe no período.",
        g6_classe_filtravel,
    ),
    (
        "G8/G9 — Desfecho Geral (Plenário Virtual e Plenário Presencial)",
        "Desfecho Geral",
        "Pizza com a proporção de concluídos e não concluídos, mais desfecho detalhado (PV) "
        "ou apenas macro (Plenário Presencial). Selecione o âmbito.",
        g8_desfecho_filtravel,
    ),
    (
        "G10/G11 — Macro-Desfecho Anual (Plenário Virtual e Plenário Presencial)",
        "Macro-Desfecho Anual",
        "Evolução anual do volume de inclusões concluídas e não concluídas. Selecione o âmbito.",
        g10_macro_anual_filtravel,
    ),
    (
        "G12/G13 — Concluídos por Ano (Plenário Virtual e Plenário Presencial)",
        "Inclusões Concluídas por Ano",
        "Fluxo anual de inclusões com desfecho concluído. Selecione o âmbito.",
        g12_concluidos_filtravel,
    ),
    (
        "G14/G15 — Não Concluídos por Classe (Plenário Virtual e Plenário Presencial)",
        "Não Concluídos por Classe",
        "Barras por classe com linha do total de não concluídos. Selecione o âmbito.",
        g14_nao_concluidos_classe_filtravel,
    ),
    (
        "G16/G17 — Concluídos por Classe (Plenário Virtual e Plenário Presencial)",
        "Concluídos por Classe",
        "Barras por classe com linha do total de concluídos. Selecione o âmbito.",
        g16_concluidos_classe_filtravel,
    ),
    # ── Tipo de Questão ───────────────────────────────────────────────────────
    (
        "G18/G19 — Não Concluídos por Tipo de Questão (Plenário Virtual e Plenário Presencial)",
        "Não Concluídos por Tipo de Questão",
        "Barras por tipo de questão (PR / RC / QI) com linha do total de não concluídos. "
        "IJ renomeado para QI na exibição. Selecione o âmbito.",
        g18_nc_tipo_filtravel,
    ),
    (
        "G20/G21 — Concluídos por Tipo de Questão (Plenário Virtual e Plenário Presencial)",
        "Concluídos por Tipo de Questão",
        "Barras por tipo de questão (PR / RC / QI) com linha do total de concluídos. Selecione o âmbito.",
        g20_c_tipo_filtravel,
    ),
    # ── Desfecho Concluído por Categoria ─────────────────────────────────────
    (
        "G22/G23 — Categoria de Desfecho (Plenário Virtual e Plenário Presencial)",
        "Categoria de Desfecho",
        "Pizza com as 4 categorias: Unânime, Maioria (relator vencedor), Maioria (relator vencido) "
        "e Não concluído (bloco agregado). Selecione o âmbito.",
        g22_cat_periodo_filtravel,
    ),
    (
        "G24/G25 — Categoria de Desfecho por Ano (Plenário Virtual e Plenário Presencial)",
        "Categoria de Desfecho por Ano",
        "Evolução anual das 4 categorias de desfecho. Selecione o âmbito.",
        g24_cat_anual_filtravel,
    ),
    (
        "G26/G27 — Categoria × Tipo de Questão (Plenário Virtual e Plenário Presencial)",
        "Categoria de Desfecho por Tipo de Questão",
        "Uma pizza por tipo de questão (PR/RC/QI) com as 4 categorias de desfecho. Período total. "
        "Processos sem tipo de questão classificados como PR. Selecione o âmbito.",
        g26_cat_tipo_periodo_filtravel,
    ),
    (
        "G28/G29 — Categoria × Tipo de Questão por Ano (Plenário Virtual e Plenário Presencial)",
        "Categoria de Desfecho por Tipo de Questão e Ano",
        "Um gráfico por tipo de questão (PR, RC, QI) mostrando a evolução anual das categorias. "
        "Selecione o âmbito e o tipo na sub-aba.",
        g28_cat_tipo_anual_filtravel,
    ),
    # ── Desfecho Não Concluído por Categoria ──────────────────────────────────
    (
        "G30/G31 — Não Concluídos por Categoria e Ano (Plenário Virtual e Plenário Presencial)",
        "Não Concluídos por Categoria e Ano",
        "Evolução anual das 4 categorias de não conclusão: Pedido de vista, Destaque, "
        "Retirado de pauta e Motivos diversos. Selecione o âmbito.",
        g30_nc_cat_anual_filtravel,
    ),
    (
        "G32/G33 — Não Concluídos por Categoria e Classe (Plenário Virtual e Plenário Presencial)",
        "Não Concluídos por Categoria e Classe",
        "Um gráfico por classe (ADI, ADPF, ADC, ADO) com as categorias de não conclusão. "
        "Selecione o âmbito e a classe na sub-aba.",
        g32_nc_cat_classe_filtravel,
    ),
    (
        "G34/G35 — Não Concluídos por Categoria e Tipo (Plenário Virtual e Plenário Presencial)",
        "Não Concluídos por Categoria e Tipo de Questão",
        "Um gráfico por tipo de questão (PR, RC, QI) com as categorias de não conclusão. "
        "Selecione o âmbito e o tipo na sub-aba.",
        g34_nc_cat_tipo_filtravel,
    ),
    # ── Pauta vs Concluídos ──────────────────────────────────────────────────────
    (
        "G_PV — Pauta vs Julgamentos Concluídos (PV, período total)",
        "PV: Pauta vs Julgamentos Concluídos",
        "Duas barras do PV no período: participação na pauta (63,9%) e participação nos "
        "julgamentos concluídos (91,3%). Contraste que mostra a concentração do PV nas conclusões.",
        g_pauta_concluidos,
    ),
    # ── Tabulador ──────────────────────────────────────────────────────────────
    (
        "G36 — Tabulador Interativo",
        "Tabulador Interativo",
        "Configure livremente os eixos, agrupamento e modo de barras. "
        "A tabela abaixo reflete a mesma seleção.",
        None,
    ),
]

_LABELS = [item[0] for item in _CATALOGO]

_SUMARIO = {
    "Inclusões em Pauta (G5, G6/G7, G8/G9, G10/G11, G12/G13, G14/G15, G16/G17)": [
        "G5 — volume anual por ambiente (Plenário Virtual vs Plenário Presencial)",
        "G6/G7 — volume por classe e ano (Plenário Virtual / Plenário Presencial selecionável)",
        "G8/G9 — desfecho geral no período (Plenário Virtual / Plenário Presencial selecionável)",
        "G10/G11 — macro-desfecho anual (Plenário Virtual e Plenário Presencial)",
        "G12/G13 — concluídos por ano (Plenário Virtual e Plenário Presencial)",
        "G14/G15 — não concluídos por classe (Plenário Virtual e Plenário Presencial)",
        "G16/G17 — concluídos por classe (Plenário Virtual e Plenário Presencial)",
    ],
    "Tipo de Questão (G18/G19, G20/G21)": [
        "G18/G19 — não concluídos por tipo PR/RC/QI (Plenário Virtual e Plenário Presencial)",
        "G20/G21 — concluídos por tipo PR/RC/QI (Plenário Virtual e Plenário Presencial)",
    ],
    "Desfecho Concluído por Categoria (G22/G23, G24/G25, G26/G27, G28/G29)": [
        "G22/G23 — distribuição por categoria no período (PV/PP selecionável)",
        "G24/G25 — evolução anual por categoria (PV/PP selecionável)",
        "G26/G27 — categoria × tipo de questão no período (PV/PP selecionável)",
        "G28/G29 — categoria × tipo de questão por ano (PV/PP selecionável)",
    ],
    "Desfecho Não Concluído por Categoria (G30/G31, G32/G33, G34/G35)": [
        "G30/G31 — categorias de não conclusão por ano (Plenário Virtual e Plenário Presencial)",
        "G32/G33 — categorias de não conclusão por classe (Plenário Virtual e Plenário Presencial)",
        "G34/G35 — categorias de não conclusão por tipo de questão (Plenário Virtual e Plenário Presencial)",
    ],
    "Pauta vs Concluídos (G_PV)": [
        "G_PV — PV: participação na pauta (63,9%) vs concluídos (91,3%)",
    ],
    "Tabulador (G36)": [
        "G36 — tabulador interativo: gráfico + tabela com eixos configuráveis",
    ],
}


_TABELA_SPECS: dict[int, tuple[str, str | None, str | None]] = {
    0: ("ano", "ambiente", None),
    1: ("ano", "classe", "PV"),
    2: ("macro_desfecho", None, "PV"),
    3: ("ano", "macro_desfecho", "PV"),
    4: ("ano", None, "PV"),
    5: ("ano", "classe", "NC_PV"),
    6: ("ano", "classe", "C_PV"),
    7: ("ano", "tipo_questao", "NC_PV"),
    8: ("ano", "tipo_questao", "C_PV"),
    9: ("categoria", None, "PV"),
    10: ("ano", "categoria", "PV"),
    11: ("tipo_questao", "categoria", "PV"),
    12: ("ano", "categoria", "PV"),
    13: ("ano", "categoria_nc", "PV"),
    14: ("ano", "categoria_nc", "PV"),
    15: ("ano", "categoria_nc", "PV"),
}


def _build_tabela(df: pd.DataFrame, spec: tuple[str, str | None, str | None]) -> pd.DataFrame:
    col_linha, col_grupo, filtro = spec
    d = df.copy()

    if "categoria" in (col_linha, col_grupo) and "categoria" not in d.columns:
        d["categoria"] = d["desfecho"].apply(_categoria_desfecho)
    if "categoria_nc" in (col_linha, col_grupo) and "categoria_nc" not in d.columns:
        d["categoria_nc"] = d["desfecho"].apply(_categoria_nc)

    if filtro == "PV":
        d = d[d["ambiente"] == "Plenário Virtual"]
    elif filtro == "PP":
        d = d[d["ambiente"] == "Plenário Presencial"]
    elif filtro == "NC_PV":
        d = d[(d["ambiente"] == "Plenário Virtual") & (d["macro_desfecho"] == "Não concluído")]
    elif filtro == "NC_PP":
        d = d[(d["ambiente"] == "Plenário Presencial") & (d["macro_desfecho"] == "Não concluído")]
    elif filtro == "C_PV":
        d = d[(d["ambiente"] == "Plenário Virtual") & (d["macro_desfecho"] == "Concluído")]
    elif filtro == "C_PP":
        d = d[(d["ambiente"] == "Plenário Presencial") & (d["macro_desfecho"] == "Concluído")]

    if col_grupo:
        tab = d.groupby([col_linha, col_grupo], observed=True).size().reset_index(name="n")
        tab = tab.pivot_table(index=col_linha, columns=col_grupo, values="n", fill_value=0)
        tab["Total"] = tab.sum(axis=1)
        tab.loc["Total"] = tab.sum()
    else:
        tab = d.groupby(col_linha, observed=True).size().reset_index(name="n")
        tab.columns = [col_linha, "Total"]
        tab.loc["Total"] = {col_linha: "Total", "Total": tab["Total"].sum()}
    tab = tab.reset_index()
    tab[col_linha] = tab[col_linha].astype(str)
    if col_grupo:
        for c in tab.columns:
            if c not in (col_linha, "Total"):
                tab[f"{c} (%)"] = (tab[c] / tab["Total"] * 100).round(1)
    return tab


def _render_tabela(df: pd.DataFrame, idx: int) -> None:
    if idx == 16:
        tab = pd.DataFrame({
            "Métrica": ["Participação na pauta", "Participação nos julgamentos concluídos"],
            "PV": ["63,9% (4.807 de 7.517)", "91,3% (2.911 de 3.187)"],
            "PP": ["36,1% (2.710 de 7.517)", "8,7% (276 de 3.187)"],
        })
        with st.expander("📊 Dados da visualização"):
            st.dataframe(tab, width="stretch", height=280)
        return
    spec = _TABELA_SPECS.get(idx)
    if spec is None:
        return
    with st.expander("📊 Dados da visualização"):
        tab = _build_tabela(df, spec)
        _sub = {c: "{:,.0f}" for c in tab.columns
                if not c.endswith("(%)") and tab[c].dtype.kind in "iuf"}
        st.dataframe(tab.style.format(_sub, na_rep="—"), width="stretch", height=280)


def _render(fn, df: pd.DataFrame, show_values: bool | None = None, proporcao: bool = False,
            **kwargs) -> None:
    if show_values is not None:
        result = fn(df, show_values=show_values, proporcao=proporcao, **kwargs)
    else:
        result = fn(df)
    if isinstance(result, dict):
        if not result:
            st.info("Sem dados para exibir.")
            return
        subtabs = st.tabs(list(result.keys()))
        for tab, fig in zip(subtabs, result.values()):
            with tab:
                st.plotly_chart(fig, width="stretch")
    elif isinstance(result, tuple):
        for fig in result:
            st.plotly_chart(fig, width="stretch")
    elif isinstance(result, list):
        cols = st.columns(len(result))
        for col, fig in zip(cols, result):
            with col:
                st.plotly_chart(fig, width="stretch")
    else:
        st.plotly_chart(result, width="stretch")


def _render_interactive_tabulador(df: pd.DataFrame) -> None:
    st.subheader("Tabulador Gráfico Interativo")
    st.caption("Configure livremente os eixos, agrupamento e modo de barras.")

    col_pre, _ = st.columns([2, 1])
    with col_pre:
        pre_escolha = st.selectbox(
            "🔖 Pré-definidos",
            options=["— ou configure manualmente abaixo —"] + _LABELS_PRE_TAB,
            index=0,
            key="inc_tab_predef",
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
        eixo_x_lbl = st.selectbox("Eixo X", _DIMS_LABEL, index=def_x, key="inc_tab_x")
    with c2:
        eixo_y_lbl = st.selectbox("Eixo Y (cor/grupo)", _DIMS_LABEL, index=def_g, key="inc_tab_y")
    with c3:
        metrica = st.selectbox(
            "Métrica", ["inclusoes", "processos"], index=def_m, key="inc_tab_m",
            format_func=lambda v: "Inclusões em pauta" if v == "inclusoes" else "Processos distintos",
        )
    with c4:
        barmode = st.selectbox(
            "Modo", ["group", "stack", "100%"], index=def_bm, key="inc_tab_bm",
            format_func=lambda v: {"group": "Agrupado", "stack": "Empilhado", "100%": "Empilhado 100%"}[v],
        )
    with c5:
        show_values_tab = st.checkbox("Exibir valores", value=False, key="inc_tab_sv")

    eixo_x = DIMENSOES[eixo_x_lbl]
    eixo_y = DIMENSOES[eixo_y_lbl]

    if eixo_x == eixo_y:
        st.warning("Eixo X e Eixo Y não podem ser a mesma dimensão.")
        return

    fig = gt10_tabulador(df, eixo_x, eixo_y, metrica, barmode, show_values_tab)
    st.plotly_chart(fig, width="stretch")

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


def render_graficos(df: pd.DataFrame, df_dec: pd.DataFrame | None = None) -> None:
    df = _refinar_motivos_diversos(df, df_dec if df_dec is not None else pd.DataFrame())

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
        key="inclusoes_selectbox",
    )

    idx = _LABELS.index(escolha)
    _, subtitulo, descricao, fn = _CATALOGO[idx]

    if fn is None:
        _render_interactive_tabulador(df)
        return

    st.subheader(subtitulo)
    st.caption(descricao)

    show_values = st.checkbox("Exibir valores", value=True, key=f"inc_sv_{idx}")

    if idx == 1:
        amb = st.selectbox("Âmbito", ["Plenário Virtual", "Plenário Presencial"],
                           key="inc_amb_classe")
        todas = sorted(df["classe"].dropna().unique())
        sel = st.multiselect("Classes", todas, default=todas, key="inc_cls_filtro")
        modo = st.selectbox("Conteúdo da pizza", ["Ambos", "Valores", "Percentual"],
                            index=0, key="inc_pizza_modo")
        mapa = {"Ambos": "percent+value", "Valores": "value", "Percentual": "percent"}
        _render(fn, df, show_values=show_values, ambiente=amb, classes=sel,
                pizza_textinfo=mapa[modo])
    elif idx == 2:
        amb = st.selectbox("Âmbito", ["Plenário Virtual", "Plenário Presencial"],
                           key="inc_amb_desfecho")
        modo = st.selectbox("Conteúdo da pizza", ["Ambos", "Valores", "Percentual"],
                            index=0, key="inc_desfecho_modo")
        mapa = {"Ambos": "percent+value", "Valores": "value", "Percentual": "percent"}
        _render(fn, df, show_values=show_values, ambiente=amb,
                pizza_textinfo=mapa[modo])
    elif idx in (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15):
        amb = st.selectbox("Âmbito", ["Plenário Virtual", "Plenário Presencial"],
                           key=f"inc_amb_{idx}")
        _render(fn, df, show_values=show_values, ambiente=amb)
    else:
        _render(fn, df, show_values=show_values)
    _render_tabela(df, idx)
