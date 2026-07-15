"""Renderização da página de Acervo."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import plotar_grafico_stf
from pages.tramitacao.plots import gt10_tabulador, DIMENSOES

_DIMS_LABEL = list(DIMENSOES.keys())

_PREDEFINIDOS_ACERVO = [
    ("Ano × Classe (total geral, empilhado)",         "ano", "classe",        "inclusoes", "stack"),
    ("Ano × Classe (total geral, empilhado 100%)",    "ano", "classe",        "inclusoes", "100%"),
    ("Classe × Macro-Desfecho (inclusões, agrupado)", "classe", "macro_desfecho", "inclusoes", "group"),
    ("Ano × Ambiente (inclusões, empilhado)",         "ano", "ambiente",      "inclusoes", "stack"),
]
_LABELS_PRE_ACERVO = [p[0] for p in _PREDEFINIDOS_ACERVO]

# Métricas disponíveis no dataset
_METRICAS = [
    (
        "quantidade_ativos",
        "Processos Ativos",
        "Acervo Ativo",
        "Estoque de processos **sem baixa definitiva** ao final de cada ano (31/12). "
        "Mede o volume pendente de julgamento e é o principal indicador de pressão sobre a pauta do tribunal.",
    ),
    (
        "quantidade_inativos",
        "Processos Inativos",
        "Acervo Inativo",
        "Estoque **acumulado** de processos já encerrados até o final de cada ano. "
        "Representa o histórico total de casos resolvidos desde 1988.",
    ),
    (
        "total_geral",
        "Total de Processos",
        "Total Geral",
        "Soma dos processos ativos e inativos ao final de cada ano. "
        "Reflete o volume total de ações já distribuídas no tribunal desde sua criação.",
    ),
    (
        "quantidade_baixas",
        "Processos Baixados",
        "Baixas Anuais",
        "**Fluxo anual** de processos encerrados em cada ano. Diferente do acervo inativo (estoque), "
        "as baixas medem a produtividade do tribunal ano a ano — picos indicam o impacto das Emendas Regimentais e do Plenário Virtual.",
    ),
    (
        "quantidade_distribuidos",
        "Processos Distribuídos",
        "Distribuições (Entrada)",
        "**Fluxo anual** de novos processos distribuídos ao relator em cada ano. "
        "Mede a pressão de entrada no tribunal e permite comparar a taxa de entrada com a taxa de baixas.",
    ),
]


def _year_range(df: pd.DataFrame) -> tuple[int, int]:
    years = pd.to_numeric(df["ano"], errors="coerce").dropna().astype(int)
    return int(years.min()), int(years.max())


def _render_aba_metrica(df: pd.DataFrame, col: str, label: str, key_prefix: str) -> None:
    """Renderiza Total + uma aba por classe para uma dada métrica."""
    show_values = st.checkbox("Exibir valores", value=False, key=f"{key_prefix}_show")

    classes = sorted(df["classe"].dropna().unique().tolist())
    sub_tabs = st.tabs(["Total"] + classes)

    with sub_tabs[0]:
        st.plotly_chart(
            plotar_grafico_stf(df, "TOTAL", col, label, show_values),
            width="stretch",
        )

    for tab, classe in zip(sub_tabs[1:], classes):
        with tab:
            st.plotly_chart(
                plotar_grafico_stf(df, classe, col, label, show_values),
                width="stretch",
            )


def _render_tabela(df: pd.DataFrame) -> None:
    st.subheader("Tabela Consolidada do Acervo")
    st.caption("Valores absolutos por ano e classe. Use os filtros para explorar o período e as métricas de interesse.")
    with st.expander("Critério / Caminho dos dados"):
        st.markdown(
            "- **Fonte:** `data/processed/acervo/evolucao_acervo.parquet`  \n"
            "- **Referência:** 31/12 de cada ano  \n"
            "- **Percentual:** participação de cada classe no `total_geral` do ano"
        )

    opcoes_classe = sorted(df["classe"].dropna().unique().tolist())
    y_min, y_max = _year_range(df)

    # ── Filtros ──────────────────────────────────────────────────────────────────────────────
    col_a, col_b, col_c = st.columns([3, 2, 2])
    with col_a:
        periodo = st.slider(
            "Período", y_min, y_max, (y_min, y_max), step=1, key="tab_periodo"
        )
    with col_b:
        classes_sel = st.multiselect(
            "Classes", opcoes_classe, default=opcoes_classe, key="tab_classes"
        )
    with col_c:
        metricas_disp = {
            "Total Geral":    "total_geral",
            "Ativos":         "quantidade_ativos",
            "Inativos":       "quantidade_inativos",
            "Baixas":         "quantidade_baixas",
            "Distribuídos":  "quantidade_distribuidos",
        }
        metricas_sel = st.multiselect(
            "Métricas", list(metricas_disp.keys()),
            default=list(metricas_disp.keys()), key="tab_metricas"
        )

    ai, af = periodo
    sel_classes  = classes_sel  if classes_sel  else opcoes_classe
    sel_metricas = metricas_sel if metricas_sel else list(metricas_disp.keys())

    df_f = df[df["ano"].between(ai, af) & df["classe"].isin(sel_classes)].copy()

    # ── Pivot: linhas = ano, colunas = (classe, métrica) ────────────────────────────────
    cols_met = [metricas_disp[m] for m in sel_metricas]
    total_ano = df_f.groupby("ano")["total_geral"].sum().rename("total_ano")
    df_f = df_f.join(total_ano, on="ano")

    rows = []
    for ano, grp in df_f.groupby("ano"):
        row: dict = {"Ano": int(ano)}
        for _, r in grp.iterrows():
            c = r["classe"]
            for m in sel_metricas:
                col_key = metricas_disp[m]
                row[f"{c} — {m}"] = int(r[col_key])
            if "Total Geral" in sel_metricas:
                row[f"{c} — %"] = (
                    round(r["total_geral"] / r["total_ano"] * 100, 1)
                    if r["total_ano"] else 0.0
                )
        # Totais consolidados
        for m in sel_metricas:
            col_key = metricas_disp[m]
            row[f"Total — {m}"] = int(grp[col_key].sum())
        rows.append(row)

    tabela = (
        pd.DataFrame(rows)
        .sort_values("Ano", ascending=False)
        .set_index("Ano")
    )

    fmt = {c: ("{:.1f}%" if c.endswith("— %") else "{:,.0f}") for c in tabela.columns}

    st.caption(f"{len(tabela):,} anos exibidos — {len(sel_classes)} classe(s) — {len(sel_metricas)} métrica(s)")
    st.dataframe(
        tabela.style.format(fmt, na_rep="—"),
        width="stretch",
        height=460,
    )


def render_graficos(df: pd.DataFrame) -> None:
    """Ponto de entrada: abas por métrica → sub-abas Total/classe + Tabulador."""

    tab_labels = [titulo for _, _, titulo, _ in _METRICAS] + ["Tabulador Gráfico"]
    tabs = st.tabs(tab_labels)

    for tab, (col, label, titulo, descricao) in zip(tabs[:-1], _METRICAS):
        with tab:
            st.subheader(f"Evolução — {titulo}")
            st.markdown(descricao)
            with st.expander("Critério / Caminho dos dados"):
                st.markdown(
                    "- **Fonte:** `data/processed/acervo/evolucao_acervo.parquet`  \n"
                    f"- **Métrica:** `{col}`  \n"
                    "- **Referência:** 31/12 de cada ano  \n"
                    "- **Marcos:** ER 51/2016, ER 52/2019, ER 53/2020 e ESPIN (2020–2022)"
                )
            _render_aba_metrica(df, col, label, key_prefix=col)

    with tabs[-1]:
        st.subheader("Tabulador Gráfico Interativo")
        st.caption(
            "Configure livremente os eixos, agrupamento e modo de barras usando o dataset "
            "de inclusões em pauta (2020–2025). Diferente dos gráficos de evolução acima, "
            "que usam o acervo histórico (1988–2025)."
        )

        col_pre, _ = st.columns([2, 1])
        with col_pre:
            pre_escolha = st.selectbox(
                "🔖 Pré-definidos",
                options=["— ou configure manualmente abaixo —"] + _LABELS_PRE_ACERVO,
                index=0,
                key="acervo_predefinido",
            )

        if pre_escolha.startswith("—"):
            def_x, def_g, def_m, def_bm = 0, 1, 0, 0
        else:
            _, px, pg, pm, pbm = next(p for p in _PREDEFINIDOS_ACERVO if p[0] == pre_escolha)
            def_x  = _DIMS_LABEL.index(next(k for k, v in DIMENSOES.items() if v == px))
            def_g  = _DIMS_LABEL.index(next(k for k, v in DIMENSOES.items() if v == pg))
            def_m  = ["inclusoes", "processos"].index(pm)
            def_bm = ["group", "stack", "100%"].index(pbm)

        c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 1])
        with c1:
            eixo_x_lbl = st.selectbox("Eixo X",    _DIMS_LABEL, index=def_x, key="acervo_tab_x")
        with c2:
            grupo_lbl  = st.selectbox("Cor/Grupo", _DIMS_LABEL, index=def_g, key="acervo_tab_g")
        with c3:
            metrica = st.selectbox(
                "Métrica", ["inclusoes", "processos"], index=def_m, key="acervo_tab_m",
                format_func=lambda v: "Inclusões em pauta" if v == "inclusoes" else "Processos distintos",
            )
        with c4:
            barmode = st.selectbox(
                "Modo", ["group", "stack", "100%"], index=def_bm, key="acervo_tab_bm",
                format_func=lambda v: {"group": "Agrupado", "stack": "Empilhado", "100%": "Empilhado 100%"}[v],
            )
        with c5:
            show_values = st.checkbox("Exibir valores", value=False, key="acervo_tab_sv")

        eixo_x = DIMENSOES[eixo_x_lbl]
        grupo  = DIMENSOES[grupo_lbl]

        if eixo_x == grupo:
            st.warning("Eixo X e Cor/Grupo não podem ser a mesma dimensão.")
        else:
            from data.loader import load_inclusoes_em_pauta
            df_inc = load_inclusoes_em_pauta()
            st.plotly_chart(
                gt10_tabulador(df_inc, eixo_x, grupo, metrica, barmode, show_values),
                width="stretch",
            )

    st.markdown("---")
    _render_tabela(df)
