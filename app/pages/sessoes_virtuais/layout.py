"""Renderização da página de Sessões Virtuais."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import (
    g1_1_sessoes_por_mes, g1_3_sessoes_trimestre_ano,
    g2_1_sessoes_relator, g2_2_taxa_conclusao_relator,
    g2_3_macro_desfecho_relator, g2_4_sessoes_relator_classe,
    g3_1_distribuicao_sessoes, g3_2_faixa_sessoes_classe,
    g3_3_taxa_conclusao_primeira, g3_4_taxa_conclusao_posicao,
    g4_2_sessoes_classe_tipo, g4_3_macro_ano_tipo,
    g4_4_macro_ano_classe, g4_5_taxa_conclusao_classe_tipo,
    g5_1_distribuicao_duracao, g5_2_duracao_mediana_classe,
    g5_3_duracao_mediana_tipo,
    prep_duracao, ORDEM_FAIXA, ORDEM_DUR, _prep_sessoes_por_processo,
)
from pages.tramitacao.plots import gt10_tabulador

_DIMS_SV = {
    "Classe":           "classe",
    "Tipo de questão":  "tipo_questao",
    "Macro-desfecho":   "macro_desfecho",
    "Desfecho detalhado": "desfecho",
    "Ano":              "ano",
    "Relator":          "relator",
}
_DIMS_LABEL = list(_DIMS_SV.keys())

_PREDEFINIDOS = [
    ("Ano × Classe (sessões, agrupado)",              "ano",      "classe",         "sessoes", "group"),
    ("Ano × Tipo (sessões, agrupado)",                "ano",      "tipo_questao",   "sessoes", "group"),
    ("Ano × Macro-desfecho (sessões, empilhado)",     "ano",      "macro_desfecho", "sessoes", "stack"),
    ("Classe × Tipo (sessões, agrupado)",             "classe",   "tipo_questao",   "sessoes", "group"),
    ("Classe × Macro-desfecho (sessões, 100%)",       "classe",   "macro_desfecho", "sessoes", "100%"),
    ("Classe × Desfecho (sessões, agrupado)",         "classe",   "desfecho",       "sessoes", "group"),
    ("Relator × Classe (sessões, agrupado)",          "relator",  "classe",         "sessoes", "group"),
    ("Relator × Macro-desfecho (sessões, agrupado)",  "relator",  "macro_desfecho", "sessoes", "group"),
]
_LABELS_PRE = [p[0] for p in _PREDEFINIDOS]

_CATALOGO = [
    (
        "G1.1 — Sessões virtuais por mês",
        "Sessões Virtuais por Mês",
        "Distribuição mensal das sessões virtuais (Jan–Dez). "
        "Recessos judiciários em janeiro e julho são visíveis.",
        g1_1_sessoes_por_mes,
    ),
    (
        "G1.2 — Sessões por mês e ano (tabela)",
        "Sessões por Mês e Ano — Tabela",
        "Tabela de referência com o volume mensal de sessões por ano.",
        "tabela_mes_ano",
    ),
    (
        "G1.3 — Sessões por trimestre e ano",
        "Sessões por Trimestre e Ano",
        "Barras agrupadas por trimestre (T1–T4) com linha do total no eixo secundário.",
        g1_3_sessoes_trimestre_ano,
    ),
    (
        "G2.1 — Sessões por relator (Top 10)",
        "Sessões por Relator — Top 10 (2020–2025)",
        "Volume de sessões por relator, limitado aos 10 com maior participação.",
        g2_1_sessoes_relator,
    ),
    (
        "G2.2 — Taxa de conclusão por relator (Top 10)",
        "Taxa de Conclusão por Relator — Top 10 (2020–2025)",
        "Percentual de sessões concluídas, ordenado da maior para a menor taxa.",
        g2_2_taxa_conclusao_relator,
    ),
    (
        "G2.3 — Macro-desfecho por relator (Top 10)",
        "Macro-Desfecho por Relator — Top 10 (2020–2025)",
        "Sessões concluídas vs não concluídas para os 10 relatores com maior volume.",
        g2_3_macro_desfecho_relator,
    ),
    (
        "G2.4 — Sessões por relator e classe (Top 10)",
        "Sessões por Relator e Classe — Top 10 (2020–2025)",
        "Distribuição das sessões por classe processual para os 10 maiores relatores.",
        g2_4_sessoes_relator_classe,
    ),
    (
        "G3.1 — Distribuição de sessões por processo",
        "Distribuição de Sessões por Processo (2020–2025)",
        "Quantos processos tiveram 1, 2–3, 4–5 ou 6+ sessões virtuais.",
        g3_1_distribuicao_sessoes,
    ),
    (
        "G3.2 — Faixa de sessões por classe",
        "Número de Sessões por Processo e Classe (2020–2025)",
        "Distribuição das faixas de sessões por classe processual.",
        g3_2_faixa_sessoes_classe,
    ),
    (
        "G3.3 — Taxa de conclusão: 1ª vs posteriores",
        "Taxa de Conclusão: 1ª Sessão vs Sessões Posteriores (2020–2025)",
        "Comparação da taxa de conclusão entre a primeira sessão e as sessões seguintes.",
        g3_3_taxa_conclusao_primeira,
    ),
    (
        "G3.4 — Taxa de conclusão por posição da sessão",
        "Taxa de Conclusão por Posição da Sessão (2020–2025)",
        "Taxa de conclusão para a 1ª, 2ª, 3ª e 4ª+ sessão no histórico do processo.",
        g3_4_taxa_conclusao_posicao,
    ),
    (
        "G4.1 — Classe × tipo de questão (tabela)",
        "Classe × Tipo de Questão — Tabela",
        "Tabela de referência com o volume de sessões por classe e tipo de questão.",
        "tabela_classe_tipo",
    ),
    (
        "G4.2 — Sessões por classe e tipo de questão",
        "Sessões por Classe e Tipo de Questão (2020–2025)",
        "Barras agrupadas por tipo de questão (PR/RC/QI) com linha do total.",
        g4_2_sessoes_classe_tipo,
    ),
    (
        "G4.3 — Macro-desfecho por ano e tipo de questão",
        "Macro-Desfecho por Ano e Tipo de Questão",
        "Barras empilhadas (Concluído/Não concluído) com linha do total. "
        "Um sub-gráfico por tipo: PR, RC e QI.",
        g4_3_macro_ano_tipo,
    ),
    (
        "G4.4 — Macro-desfecho por ano e classe",
        "Macro-Desfecho por Ano e Classe (ADI e ADPF)",
        "Barras empilhadas por ano para ADI e ADPF. ADC (79) e ADO (40) omitidos por base pequena.",
        g4_4_macro_ano_classe,
    ),
    (
        "G4.5 — Taxa de conclusão: classe × tipo de questão",
        "Taxa de Conclusão por Classe e Tipo de Questão (2020–2025)",
        "Percentual de sessões concluídas, agrupado por classe e tipo de questão.",
        g4_5_taxa_conclusao_classe_tipo,
    ),
    (
        "G5.1 — Distribuição de duração até conclusão",
        "Tempo até Conclusão (2020–2025)",
        "Distribuição do tempo decorrido entre a primeira inclusão em pauta e a sessão de "
        "conclusão, em faixas. Selecione o âmbito.",
        g5_1_distribuicao_duracao,
    ),
    (
        "G5.2 — Duração mediana por classe",
        "Tempo Mediano até Conclusão por Classe (dias)",
        "Mediana de dias entre a primeira pauta e a conclusão, por classe. Selecione o âmbito.",
        g5_2_duracao_mediana_classe,
    ),
    (
        "G5.3 — Duração mediana por tipo de questão",
        "Tempo Mediano até Conclusão por Tipo de Questão (dias)",
        "Mediana de dias entre a primeira pauta e a conclusão, por tipo. Selecione o âmbito.",
        g5_3_duracao_mediana_tipo,
    ),
    (
        "G6 — Tabulador Interativo",
        "Tabulador Interativo — Sessões Virtuais (2020–2025)",
        "Configure livremente os eixos, agrupamento, métrica e modo de barras.",
        None,
    ),
]
_LABELS = [item[0] for item in _CATALOGO]

_SUMARIO = {
    "Bloco 1 — Sazonalidade (G1.1, G1.2, G1.3)": [
        "G1.1 — sessões por mês (Jan–Dez)",
        "G1.2 — sessões por mês e ano (tabela)",
        "G1.3 — sessões por trimestre e ano",
    ],
    "Bloco 2 — Relator (G2.1, G2.2, G2.3, G2.4)": [
        "G2.1 — sessões por relator (Top 10)",
        "G2.2 — taxa de conclusão por relator (%)",
        "G2.3 — macro-desfecho por relator (empilhado)",
        "G2.4 — sessões por relator e classe (empilhado)",
    ],
    "Bloco 3 — Múltiplas sessões (G3.1, G3.2, G3.3, G3.4)": [
        "G3.1 — distribuição de sessões por processo",
        "G3.2 — faixa de sessões por classe",
        "G3.3 — taxa de conclusão: 1ª vs posteriores",
        "G3.4 — taxa de conclusão por posição da sessão",
    ],
    "Bloco 4 — Cruzamentos (G4.1, G4.2, G4.3, G4.4, G4.5)": [
        "G4.1 — classe × tipo de questão (tabela)",
        "G4.2 — sessões por classe e tipo de questão",
        "G4.3 — macro-desfecho por ano e tipo (PR, RC, QI)",
        "G4.4 — macro-desfecho por ano e classe (ADI, ADPF)",
        "G4.5 — taxa de conclusão: classe × tipo (%)",
    ],
    "Bloco 5 — Duração (G5.1, G5.2, G5.3)": [
        "G5.1 — distribuição de duração até conclusão",
        "G5.2 — duração mediana por classe (dias)",
        "G5.3 — duração mediana por tipo de questão (dias)",
    ],
    "Tabulador (G6)": [
        "G6 — tabulador interativo: gráfico + tabela com eixos configuráveis",
    ],
}

_BLOCO5_INDICES = {16, 17, 18}
_DICT_INDICES = {13, 14}
_TABLE_ONLY = {1, 11}
_TABULADOR_IDX = 19


# ── Helpers de tabela ─────────────────────────────────────────────────────────

def _build_tabela(df: pd.DataFrame, spec: tuple[str, str | None]) -> pd.DataFrame:
    col_linha, col_grupo = spec
    d = df.copy()
    if col_grupo:
        tab = d.groupby([col_linha, col_grupo], observed=True).size().reset_index(name="n")
        pvt = tab.pivot_table(index=col_linha, columns=col_grupo, values="n", fill_value=0)
        pvt["Total"] = pvt.sum(axis=1)
        pvt.loc["Total"] = pvt.sum()
    else:
        tab = d.groupby(col_linha, observed=True).size().reset_index(name="n")
        pvt = tab.set_index(col_linha)
        pvt.columns = ["Total"]
        pvt.loc["Total"] = pvt["Total"].sum()
    pvt = pvt.reset_index()
    pvt[pvt.columns[0]] = pvt[pvt.columns[0]].astype(str)
    return pvt


def _build_tabela_pct(df: pd.DataFrame, col_linha: str, col_grupo: str) -> pd.DataFrame:
    """Tabela com percentual de conclusão (para G4.5)."""
    tab = df.groupby([col_linha, col_grupo])["macro_desfecho"].apply(
        lambda x: round(100 * (x == "Concluído").mean(), 1)
    ).reset_index(name="% Concluído")
    pvt = tab.pivot_table(index=col_linha, columns=col_grupo, values="% Concluído")
    pvt = pvt.reset_index()
    pvt[pvt.columns[0]] = pvt[pvt.columns[0]].astype(str)
    return pvt


def _tabela_mes_ano(df_s: pd.DataFrame) -> pd.DataFrame:
    """Tabela G1.2: sessões por mês e ano."""
    tab = df_s.groupby(["ano", "mes"]).size().unstack(fill_value=0)
    meses = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
             7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}
    tab = tab.rename(columns=meses)
    tab["Total"] = tab.sum(axis=1)
    tab.columns.name = None
    tab = tab.reset_index()
    tab["ano"] = tab["ano"].astype(str)
    return tab


def _tabela_classe_tipo(df_s: pd.DataFrame) -> pd.DataFrame:
    """Tabela G4.1: classe × tipo de questão."""
    tab = df_s.groupby(["classe", "tipo_questao"]).size().unstack(fill_value=0)
    tab["Total"] = tab.sum(axis=1)
    tab.loc["Total"] = tab.sum()
    tab.columns.name = None
    tab = tab.reset_index()
    tab["classe"] = tab["classe"].astype(str)
    return tab


def _render_tabela_comum(df: pd.DataFrame, idx: int) -> None:
    if idx == 0:
        tab = _build_tabela(df, ("mes", None))
        fmt = {c: "{:,.0f}" for c in tab.columns if c != tab.columns[0]}
    elif idx in _TABLE_ONLY:
        return  # handled by special renderer
    elif idx == 15:
        tab = _build_tabela_pct(df, "classe", "tipo_questao")
        fmt = {c: "{:.1f}%" for c in tab.columns if c != tab.columns[0]}
    else:
        specs = {
            2: ("ano", "trimestre"),
            3: ("relator", None),
            4: ("relator", None),
            5: ("relator", "macro_desfecho"),
            6: ("relator", "classe"),
            12: ("classe", "tipo_questao"),
            13: ("ano", "macro_desfecho"),
            14: ("ano", "macro_desfecho"),
        }
        spec = specs.get(idx)
        if spec is None:
            return
        tab = _build_tabela(df, spec)
        fmt = {c: "{:,.0f}" for c in tab.columns if c != tab.columns[0]}
    with st.expander("📊 Dados da visualização"):
        st.dataframe(tab.style.format(fmt, na_rep="—"), width="stretch", height=280)


def _render_tabela_bloco3(df_s: pd.DataFrame, idx: int) -> None:
    """Tabela para gráficos do Bloco 3 (colunas computadas dinamicamente)."""
    spp, df_ord = _prep_sessoes_por_processo(df_s)
    if idx == 7:
        tab = spp["faixa"].value_counts().reindex(ORDEM_FAIXA)
        tab = tab.reset_index()
        tab.columns = ["Faixa", "Nº de processos"]
        fmt = {"Nº de processos": "{:,.0f}"}
    elif idx == 8:
        tab = spp.groupby(["classe", "faixa"]).size().reset_index(name="n")
        pvt = tab.pivot_table(index="classe", columns="faixa", values="n", fill_value=0)
        pvt = pvt[ORDEM_FAIXA]
        pvt["Total"] = pvt.sum(axis=1)
        pvt.loc["Total"] = pvt.sum()
        pvt = pvt.reset_index()
        pvt["classe"] = pvt["classe"].astype(str)
        tab = pvt
        fmt = {c: "{:,.0f}" for c in tab.columns if c not in ("classe",) and tab[c].dtype.kind in "iuf"}
    elif idx == 9:
        df_ord["posicao"] = df_ord["n_sessao"].apply(
            lambda n: "1ª sessão" if n == 1 else "Sessões posteriores"
        )
        tab = df_ord.groupby("posicao")["macro_desfecho"].apply(
            lambda x: round(100 * (x == "Concluído").mean(), 1)
        ).reindex(["1ª sessão", "Sessões posteriores"]).reset_index()
        tab.columns = ["Posição", "% Concluído"]
        fmt = {"% Concluído": "{:.1f}%"}
    elif idx == 10:
        def _pl(n):
            if n <= 3: return f"{n}ª sessão"
            return "4ª+ sessão"
        ORDEM = ["1ª sessão", "2ª sessão", "3ª sessão", "4ª+ sessão"]
        df_ord["posicao_n"] = df_ord["n_sessao"].apply(_pl)
        tab = df_ord.groupby("posicao_n")["macro_desfecho"].apply(
            lambda x: round(100 * (x == "Concluído").mean(), 1)
        ).reindex(ORDEM).reset_index()
        tab.columns = ["Posição", "% Concluído"]
        fmt = {"% Concluído": "{:.1f}%"}
    else:
        return
    with st.expander("📊 Dados da visualização"):
        st.dataframe(tab.style.format(fmt, na_rep="—"), width="stretch", height=280)


def _render_tabela_bloco5(duracao: pd.DataFrame, idx: int) -> None:
    if idx == 16:
        tab = duracao["faixa_dur"].value_counts().reindex(ORDEM_DUR)
        tab = tab.reset_index()
        tab.columns = ["Duração", "Nº de processos"]
        fmt = {"Nº de processos": "{:,.0f}"}
    elif idx == 17:
        tab = duracao.groupby("classe")["dias"].median().round(0).astype(int).reset_index()
        tab.columns = ["Classe", "Dias (mediana)"]
        fmt = {"Dias (mediana)": "{:,.0f}"}
    elif idx == 18:
        tab = duracao.groupby("tipo_questao")["dias"].median().round(0).astype(int).reset_index()
        tab.columns = ["Tipo de questão", "Dias (mediana)"]
        fmt = {"Dias (mediana)": "{:,.0f}"}
    else:
        return
    with st.expander("📊 Dados da visualização"):
        st.dataframe(tab.style.format(fmt, na_rep="—"), width="stretch", height=280)


# ── Tabulador interativo ──────────────────────────────────────────────────────

def _render_interactive_tabulador(df_s: pd.DataFrame) -> None:
    st.subheader("Tabulador Interativo")
    st.caption("Configure livremente os eixos, agrupamento e modo de barras.")

    col_pre, _ = st.columns([2, 1])
    with col_pre:
        pre_escolha = st.selectbox(
            "🔖 Pré-definidos",
            options=["— ou configure manualmente abaixo —"] + _LABELS_PRE,
            index=0,
            key="sv_predefinido",
        )

    if pre_escolha.startswith("—"):
        def_x, def_g, def_m, def_bm = 0, 1, 0, 0
    else:
        _, px, pg, pm, pbm = next(p for p in _PREDEFINIDOS if p[0] == pre_escolha)
        def_x  = _DIMS_LABEL.index(next(k for k, v in _DIMS_SV.items() if v == px))
        def_g  = _DIMS_LABEL.index(next(k for k, v in _DIMS_SV.items() if v == pg))
        def_m  = ["sessoes", "processos"].index(pm)
        def_bm = ["group", "stack", "100%"].index(pbm)

    c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 1])
    with c1:
        eixo_x_lbl = st.selectbox("Eixo X",    _DIMS_LABEL, index=def_x, key="sv_tab_x")
    with c2:
        grupo_lbl  = st.selectbox("Cor/Grupo", _DIMS_LABEL, index=def_g, key="sv_tab_g")
    with c3:
        metrica = st.selectbox(
            "Métrica", ["sessoes", "processos"], index=def_m, key="sv_tab_m",
            format_func=lambda v: "Sessões" if v == "sessoes" else "Processos distintos",
        )
    with c4:
        barmode = st.selectbox(
            "Modo", ["group", "stack", "100%"], index=def_bm, key="sv_tab_bm",
            format_func=lambda v: {"group": "Agrupado", "stack": "Empilhado", "100%": "Empilhado 100%"}[v],
        )
    with c5:
        show_values = st.checkbox("Exibir valores", value=False, key="sv_tab_sv")

    eixo_x = _DIMS_SV[eixo_x_lbl]
    grupo  = _DIMS_SV[grupo_lbl]

    if eixo_x == grupo:
        st.warning("Eixo X e Cor/Grupo não podem ser a mesma dimensão.")
        return

    gt_metrica = "processos" if metrica == "processos" else "inclusoes"
    fig = gt10_tabulador(df_s, eixo_x, grupo, gt_metrica, barmode, show_values)
    if metrica == "sessoes":
        fig.update_yaxes(title_text="Nº de sessões")
    st.plotly_chart(fig, width="stretch")

    st.markdown("---")
    st.subheader("Tabela — mesmos eixos")
    d = df_s.copy()
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


# ── Renderização principal ────────────────────────────────────────────────────

def render_graficos(df_s: pd.DataFrame, df_final: pd.DataFrame) -> None:
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
        key="sessoes_selectbox",
    )

    idx = _LABELS.index(escolha)
    _, subtitulo, descricao, fn = _CATALOGO[idx]

    # Tabulador
    if idx == _TABULADOR_IDX:
        _render_interactive_tabulador(df_s)
        return

    st.subheader(subtitulo)
    st.caption(descricao)

    # Table-only items
    if idx in _TABLE_ONLY:
        if idx == 1:
            tab = _tabela_mes_ano(df_s)
            fmt = {c: "{:,.0f}" for c in tab.columns if tab[c].dtype.kind in "iuf"}
        elif idx == 11:
            tab = _tabela_classe_tipo(df_s)
            fmt = {c: "{:,.0f}" for c in tab.columns if tab[c].dtype.kind in "iuf"}
        with st.expander("📊 Dados da visualização"):
            st.dataframe(tab.style.format(fmt, na_rep="—"), width="stretch", height=280)
        return

    show_values = st.checkbox("Exibir valores", value=True, key=f"sv_{idx}")

    # Block 5 — duração (precisa de ambiente + duracao df)
    if idx in _BLOCO5_INDICES:
        if df_final.empty or "ambiente" not in df_final.columns:
            st.warning("Dataset de inclusões em pauta não disponível. Bloco 5 requer "
                       "ambos os datasets.")
            return
        ambiente = st.selectbox(
            "Âmbito", ["Plenário Virtual", "Plenário Presencial"],
            key=f"sv_amb_{idx}",
        )
        duracao = prep_duracao(df_s, df_final, ambiente)
        fig = fn(duracao, show_values=show_values)
        st.plotly_chart(fig, width="stretch")
        _render_tabela_bloco5(duracao, idx)
        return

    # Charts that return dict (multiple subtabs)
    if idx in _DICT_INDICES:
        result = fn(df_s, show_values=show_values)
        if not result:
            st.info("Sem dados para exibir.")
            return
        subtabs = st.tabs(list(result.keys()))
        for tab, fig in zip(subtabs, result.values()):
            with tab:
                st.plotly_chart(fig, width="stretch")
        _render_tabela_comum(df_s, idx)
        return

    # Block 3 charts (need custom table)
    if idx in {7, 8, 9, 10}:
        fig = fn(df_s, show_values=show_values)
        st.plotly_chart(fig, width="stretch")
        _render_tabela_bloco3(df_s, idx)
        return

    # Standard single-chart items
    fig = fn(df_s, show_values=show_values)
    st.plotly_chart(fig, width="stretch")
    _render_tabela_comum(df_s, idx)
