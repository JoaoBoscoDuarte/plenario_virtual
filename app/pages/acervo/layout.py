"""Renderização da página de Acervo — filtros por gráfico, sem sidebar."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from data.filters import filter_by_values, prepare_class_or_geral
from .plots import fig_total_por_ano, fig_evolucao_acervo, fig_composicao_proporcional


def _year_range(df: pd.DataFrame) -> tuple[int, int]:
    years = pd.to_numeric(df["ano"], errors="coerce").dropna().astype(int)
    return int(years.min()), int(years.max())


def _render_total_por_ano(df: pd.DataFrame) -> None:
    st.subheader("Evolução anual do acervo (Geral)")
    st.caption("Soma de todas as classes de Controle Concentrado ao final de cada ano.")
    with st.expander("Critério / Caminho dos dados"):
        st.markdown(
            "- **Fonte:** `data/processed/evolucao_acervo.parquet`  \n"
            "- **Agregação:** soma de ADI + ADC + ADO + ADPF por ano  \n"
            "- **Referência:** 31/12 de cada ano"
        )

    c1, c2, c3 = st.columns([3, 2, 1])
    with c1:
        y_min, y_max = _year_range(df)
        periodo = st.slider(
            "Período",
            min_value=y_min,
            max_value=y_max,
            value=(y_min, y_max),
            step=1,
            key="total_periodo",
        )
    with c2:
        chart_type = st.radio(
            "Tipo", ["Linhas", "Barras"], horizontal=True, key="total_chart_type"
        )
    with c3:
        st.write("&nbsp;", unsafe_allow_html=True)
        show_values = st.checkbox("Valores", value=False, key="total_show_values")

    ai, af = periodo
    df_f = df[df["ano"].between(ai, af)].copy()
    st.plotly_chart(
        fig_total_por_ano(df_f, chart_type=chart_type, show_values=show_values),
        use_container_width=True,
    )


def _render_evolucao(df: pd.DataFrame) -> None:
    st.subheader("Evolução anual do acervo por classe")
    st.caption(
        "Quantidade de processos ativos ao final de cada ano, por classe processual."
    )
    with st.expander("Critério / Caminho dos dados"):
        st.markdown(
            "- **Fonte:** `data/processed/evolucao_acervo.parquet`  \n"
            "- **Referência:** 31/12 de cada ano  \n"
            "- **Unidade:** processo  \n"
            "> Excluídos processos com baixa definitiva ou processo findo."
        )

    opcoes = sorted(df["classe"].dropna().unique().tolist())
    c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
    with c1:
        y_min, y_max = _year_range(df)
        periodo = st.slider(
            "Período",
            min_value=y_min,
            max_value=y_max,
            value=(y_min, y_max),
            step=1,
            key="evol_periodo",
        )
    with c2:
        classes_sel = st.multiselect(
            "Classes", options=opcoes, default=opcoes, key="evol_classes"
        )
    with c3:
        chart_type = st.radio(
            "Tipo",
            ["Linhas", "Barras", "Barras Empilhadas"],
            horizontal=True,
            key="evol_chart_type",
        )
    with c4:
        st.write("&nbsp;", unsafe_allow_html=True)  # alinha verticalmente
        show_values = st.checkbox("Valores", value=False, key="evol_show_values")

    ai, af = periodo
    sel = classes_sel if classes_sel else opcoes
    df_f = df[df["ano"].between(ai, af) & df["classe"].isin(sel)].copy()

    st.plotly_chart(
        fig_evolucao_acervo(df_f, chart_type=chart_type, show_values=show_values),
        use_container_width=True,
    )


def _render_tabela(df: pd.DataFrame) -> None:
    st.subheader("Dados Brutos por Ano e Classe")
    st.caption(
        "Valores absolutos e participação percentual de cada classe no total anual."
    )
    with st.expander("Critério / Caminho dos dados"):
        st.markdown(
            "- **Fonte:** `data/processed/evolucao_acervo.parquet`  \n"
            "- **Percentual:** participação de cada classe no total de processos ativos do ano"
        )

    opcoes = sorted(df["classe"].dropna().unique().tolist())
    c1, c2 = st.columns([3, 3])
    with c1:
        y_min, y_max = _year_range(df)
        periodo = st.slider(
            "Período",
            min_value=y_min,
            max_value=y_max,
            value=(y_min, y_max),
            step=1,
            key="tab_periodo",
        )
    with c2:
        classes_sel = st.multiselect(
            "Classes", options=opcoes, default=opcoes, key="tab_classes"
        )

    ai, af = periodo
    sel = classes_sel if classes_sel else opcoes
    df_f = df[df["ano"].between(ai, af) & df["classe"].isin(sel)].copy()

    # Pivot: linhas = ano, colunas = classe
    pivot = df_f.pivot_table(
        index="ano", columns="classe", values="quantidade_ativos", aggfunc="sum"
    )
    pivot = pivot.reindex(sorted(pivot.columns), axis=1)
    pivot["Total"] = pivot.sum(axis=1)

    # Percentuais por classe
    pct_cols = {}
    for col in [c for c in pivot.columns if c != "Total"]:
        pct_cols[f"{col} (%)"] = (pivot[col] / pivot["Total"] * 100).round(1)
    pct_df = pd.DataFrame(pct_cols)

    # Intercala valor absoluto + percentual por classe, depois Total
    classes_ord = [c for c in pivot.columns if c != "Total"]
    cols_intercaladas = []
    for c in classes_ord:
        cols_intercaladas.append(c)
        if f"{c} (%)" in pct_df.columns:
            cols_intercaladas.append(f"{c} (%)")

    tabela = pd.concat([pivot[classes_ord], pct_df, pivot[["Total"]]], axis=1)
    tabela = tabela[cols_intercaladas + ["Total"]]
    tabela.index.name = "Ano"
    tabela = tabela.sort_index(ascending=False)

    # Formatação: inteiros para absolutos, 1 decimal para percentuais
    fmt = {c: "{:,.0f}" for c in classes_ord + ["Total"]}
    fmt.update({c: "{:.1f}%" for c in pct_df.columns})

    st.dataframe(
        tabela.style.format(fmt, na_rep="—"),
        use_container_width=True,
        height=460,
    )


def render_graficos(df: pd.DataFrame) -> None:
    """Renderiza todos os gráficos e diagnóstico da página de Acervo."""

    st.markdown("---")
    _render_total_por_ano(df)

    st.markdown("---")
    _render_evolucao(df)

    st.markdown("---")
    _render_tabela(df)

    st.markdown("---")
    with st.expander(
        "Diagnóstico Analítico e Conclusões da Série Histórica", expanded=True
    ):
        st.markdown("""
### Crescimento Ininterrupto e a "Explosão" do Acervo Total
O dado mais alarmante e evidente é o crescimento estrito e contínuo do acervo total, que saltou de apenas **11 processos em 1988** para **9.142 processos ativos em 2025**. Em nenhum ano da série histórica houve redução do estoque de processos de um ano para o outro. Isso demonstra um cenário de litigiosidade acumulada: a taxa de entrada de novas ações e o tempo de tramitação superam consistentemente a capacidade de baixa definitiva do tribunal, consolidando o fenômeno da judicialização da política e das políticas públicas no Brasil pós-1988.

### A Hegemonia Absoluta da ADI
A Ação Direta de Inconstitucionalidade (ADI) é o verdadeiro motor do acervo do controle concentrado. Desde o primeiro ano, ela representa a esmagadora maioria dos casos. Em 2025, com **7.678 processos**, as ADIs sozinhas respondem por aproximadamente **84% de todo o acervo ativo** do tribunal. Isso indica que o principal uso do controle concentrado historicamente tem sido o questionamento direto e a tentativa de derrubada de leis e atos normativos federais e estaduais.

### A Ascensão Meteórica da ADPF
A Arguição de Descumprimento de Preceito Fundamental (ADPF) surge no acervo no ano 2000 com apenas 10 processos ativos (logo após sua regulamentação pela Lei nº 9.882/1999). O seu crescimento, no entanto, foi o mais agressivo proporcionalmente: chegou a **1.279 processos em 2025**, consolidando-se isoladamente como a segunda maior classe processual. O salto mais expressivo ocorreu na última década (de 314 em 2014 para 1.279 em 2025).

### O Papel Periférico e Estabilizado de ADCs e ADOs
Diferente das ADIs e ADPFs, a Ação Declaratória de Constitucionalidade (ADC) e a Ação Direta de Inconstitucionalidade por Omissão (ADO) possuem um papel nitidamente residual no volume total do acervo:

- **ADC:** Teve início em 1993 (com a Emenda Constitucional nº 3) e encerrou 2025 com apenas **95 processos**. Por ser um instrumento que visa confirmar a constitucionalidade de uma lei federal em face de controvérsia judicial relevante, seu uso é muito mais restrito e estratégico.

- **ADO:** Passou a figurar no acervo em 2008 (com a regulamentação pela Lei nº 12.063/2009) e chegou a 2025 com **90 processos ativos**. Embora trate de omissões legislativas (falta de regulamentação de direitos constitucionais), o tribunal compartilha essa demanda de forma pulverizada com o Mandado de Injunção no controle difuso, o que mantém o estoque concentrado em patamares baixos.

O perfil do acervo migrou de um modelo de classe única (focado quase que exclusivamente em ADIs entre 1988 e 1999) para um **modelo bipolarizado** a partir dos anos 2000, dividido entre ADIs (foco em leis) e ADPFs (foco em atos governamentais e direitos fundamentais). O principal desafio revelado por essa tabela é de gestão judiciária: o tribunal lida com um acervo de controle abstrato que se expande de forma linear, exigindo cada vez mais mecanismos de julgamento em bloco (como as sessões virtuais) para tentar conter o represamento dessas ações.
        """)
