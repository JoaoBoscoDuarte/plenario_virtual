"""Renderização da página de Acervo — filtros por gráfico, sem sidebar."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import (
    fig_total_geral_por_ano,
    fig_total_geral_por_classe,
    fig_total_por_ano,
    fig_evolucao_acervo,
    fig_total_inativos_por_ano,
    fig_inativos_por_classe,
    fig_composicao_proporcional,
)

_TIPOS_GERAL = ["Linhas", "Barras"]
_TIPOS_CLASSE = ["Linhas", "Barras", "Barras Empilhadas"]


def _year_range(df: pd.DataFrame) -> tuple[int, int]:
    years = pd.to_numeric(df["ano"], errors="coerce").dropna().astype(int)
    return int(years.min()), int(years.max())


def _controles_geral(key_prefix: str, df: pd.DataFrame) -> tuple[pd.DataFrame, str, bool]:
    """Filtros para gráficos de série única (sem classe)."""
    c1, c2, c3 = st.columns([3, 2, 1])
    with c1:
        y_min, y_max = _year_range(df)
        periodo = st.slider("Período", y_min, y_max, (y_min, y_max), step=1, key=f"{key_prefix}_periodo")
    with c2:
        chart_type = st.radio("Tipo", _TIPOS_GERAL, horizontal=True, key=f"{key_prefix}_tipo")
    with c3:
        st.write("&nbsp;", unsafe_allow_html=True)
        show_values = st.checkbox("Valores", value=False, key=f"{key_prefix}_valores")
    ai, af = periodo
    return df[df["ano"].between(ai, af)].copy(), chart_type, show_values


def _controles_classe(key_prefix: str, df: pd.DataFrame) -> tuple[pd.DataFrame, str, bool]:
    """Filtros para gráficos desagregados por classe."""
    opcoes = sorted(df["classe"].dropna().unique().tolist())
    c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
    with c1:
        y_min, y_max = _year_range(df)
        periodo = st.slider("Período", y_min, y_max, (y_min, y_max), step=1, key=f"{key_prefix}_periodo")
    with c2:
        classes_sel = st.multiselect("Classes", opcoes, default=opcoes, key=f"{key_prefix}_classes")
    with c3:
        chart_type = st.radio("Tipo", _TIPOS_CLASSE, horizontal=True, key=f"{key_prefix}_tipo")
    with c4:
        st.write("&nbsp;", unsafe_allow_html=True)
        show_values = st.checkbox("Valores", value=False, key=f"{key_prefix}_valores")
    ai, af = periodo
    sel = classes_sel if classes_sel else opcoes
    return df[df["ano"].between(ai, af) & df["classe"].isin(sel)].copy(), chart_type, show_values


def _section(title: str, caption: str, fonte: str):
    st.subheader(title)
    st.caption(caption)
    with st.expander("Critério / Caminho dos dados"):
        st.markdown(f"- **Fonte:** `data/processed/acervo/evolucao_acervo.parquet`  \n- **Referência:** 31/12 de cada ano  \n{fonte}")


# ── Seções de plotagem ────────────────────────────────────────────────────────

def _render_total_geral_ano(df: pd.DataFrame) -> None:
    _section(
        "Evolução Total do Acervo por Ano",
        "Soma de todas as classes (ADI + ADC + ADO + ADPF) ao final de cada ano.",
        "- **Métrica:** `total_geral` — soma de ativos e inativos",
    )
    df_f, ct, sv = _controles_geral("tga", df)
    st.plotly_chart(fig_total_geral_por_ano(df_f, ct, sv), use_container_width=True)


def _render_total_geral_classe(df: pd.DataFrame) -> None:
    _section(
        "Evolução Total do Acervo por Classe",
        "Total de processos (ativos + inativos) por classe processual ao longo dos anos.",
        "- **Métrica:** `total_geral` por classe",
    )
    df_f, ct, sv = _controles_classe("tgc", df)
    st.plotly_chart(fig_total_geral_por_classe(df_f, ct, sv), use_container_width=True)


def _render_ativo_ano(df: pd.DataFrame) -> None:
    _section(
        "Evolução do Acervo Ativo por Ano",
        "Processos ativos ao final de cada ano, agregando todas as classes.",
        "- **Métrica:** `quantidade_ativos` — processos sem baixa definitiva",
    )
    df_f, ct, sv = _controles_geral("ata", df)
    st.plotly_chart(fig_total_por_ano(df_f, ct, sv), use_container_width=True)


def _render_ativo_classe(df: pd.DataFrame) -> None:
    _section(
        "Evolução do Acervo Ativo por Classe",
        "Desagregação dos processos ativos por classe processual ao longo dos anos.",
        "- **Métrica:** `quantidade_ativos` por classe",
    )
    df_f, ct, sv = _controles_classe("atc", df)
    st.plotly_chart(fig_evolucao_acervo(df_f, ct, sv), use_container_width=True)


def _render_inativo_ano(df: pd.DataFrame) -> None:
    _section(
        "Evolução do Acervo Inativo por Ano",
        "Processos encerrados (baixa definitiva) acumulados ao final de cada ano.",
        "- **Métrica:** `quantidade_inativos` — processos com baixa definitiva",
    )
    df_f, ct, sv = _controles_geral("ina", df)
    st.plotly_chart(fig_total_inativos_por_ano(df_f, ct, sv), use_container_width=True)


def _render_inativo_classe(df: pd.DataFrame) -> None:
    _section(
        "Evolução do Acervo Inativo por Classe",
        "Desagregação dos processos encerrados por classe processual ao longo dos anos.",
        "- **Métrica:** `quantidade_inativos` por classe",
    )
    df_f, ct, sv = _controles_classe("inc", df)
    st.plotly_chart(fig_inativos_por_classe(df_f, ct, sv), use_container_width=True)


def _render_composicao(df: pd.DataFrame) -> None:
    _section(
        "Composição Proporcional por Classe",
        "Distribuição empilhada do acervo ativo por classe processual.",
        "- **Métrica:** `quantidade_ativos` — empilhamento absoluto por classe",
    )
    opcoes = sorted(df["classe"].dropna().unique().tolist())
    c1, c2, c3 = st.columns([3, 3, 1])
    with c1:
        y_min, y_max = _year_range(df)
        periodo = st.slider("Período", y_min, y_max, (y_min, y_max), step=1, key="comp_periodo")
    with c2:
        classes_sel = st.multiselect("Classes", opcoes, default=opcoes, key="comp_classes")
    with c3:
        st.write("&nbsp;", unsafe_allow_html=True)
        show_values = st.checkbox("Valores", value=False, key="comp_valores")
    ai, af = periodo
    sel = classes_sel if classes_sel else opcoes
    df_f = df[df["ano"].between(ai, af) & df["classe"].isin(sel)].copy()
    if df_f.empty:
        st.warning("Nenhum registro para os filtros selecionados.")
        return
    st.plotly_chart(fig_composicao_proporcional(df_f, show_values), use_container_width=True)


def _render_tabela(df: pd.DataFrame) -> None:
    st.subheader("Dados Brutos por Ano e Classe")
    st.caption("Valores absolutos (total, ativos, inativos) e participação percentual de cada classe no total anual.")
    with st.expander("Critério / Caminho dos dados"):
        st.markdown(
            "- **Fonte:** `data/processed/acervo/evolucao_acervo.parquet`  \n"
            "- **Percentual:** participação de cada classe no `total_geral` do ano"
        )

    opcoes = sorted(df["classe"].dropna().unique().tolist())
    c1, c2 = st.columns([3, 3])
    with c1:
        y_min, y_max = _year_range(df)
        periodo = st.slider("Período", y_min, y_max, (y_min, y_max), step=1, key="tab_periodo")
    with c2:
        classes_sel = st.multiselect("Classes", opcoes, default=opcoes, key="tab_classes")

    ai, af = periodo
    sel = classes_sel if classes_sel else opcoes
    df_f = df[df["ano"].between(ai, af) & df["classe"].isin(sel)].copy()

    total_ano = df_f.groupby("ano")["total_geral"].sum().rename("total_ano")
    df_f = df_f.join(total_ano, on="ano")

    rows = []
    for ano, grp in df_f.groupby("ano"):
        row = {"Ano": ano}
        for _, r in grp.iterrows():
            c = r["classe"]
            row[f"{c} Total"] = int(r["total_geral"])
            row[f"{c} Ativos"] = int(r["quantidade_ativos"])
            row[f"{c} Inativos"] = int(r["quantidade_inativos"])
            row[f"{c} (%)"] = round(r["total_geral"] / r["total_ano"] * 100, 1) if r["total_ano"] else 0.0
        row["Total Geral"] = int(grp["total_geral"].sum())
        row["Total Ativos"] = int(grp["quantidade_ativos"].sum())
        row["Total Inativos"] = int(grp["quantidade_inativos"].sum())
        rows.append(row)

    tabela = pd.DataFrame(rows).sort_values("Ano", ascending=False).set_index("Ano")

    int_cols = [c for c in tabela.columns if "%" not in c]
    pct_cols = [c for c in tabela.columns if "%" in c]
    fmt = {c: "{:,.0f}" for c in int_cols}
    fmt.update({c: "{:.1f}%" for c in pct_cols})

    st.dataframe(tabela.style.format(fmt, na_rep="—"), use_container_width=True, height=460)


# ── Ponto de entrada ──────────────────────────────────────────────────────────

def render_graficos(df: pd.DataFrame) -> None:
    st.markdown("---")
    _render_total_geral_ano(df)

    st.markdown("---")
    _render_total_geral_classe(df)

    st.markdown("---")
    _render_ativo_ano(df)

    st.markdown("---")
    _render_ativo_classe(df)

    st.markdown("---")
    _render_inativo_ano(df)

    st.markdown("---")
    _render_inativo_classe(df)

    st.markdown("---")
    with st.expander("Diagnóstico Analítico e Conclusões da Série Histórica", expanded=True):
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

    st.markdown("---")
    _render_tabela(df)
