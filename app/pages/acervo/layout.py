"""Renderização da página de Acervo — filtros por gráfico, sem sidebar."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import fig_total_ativo_anual, fig_ativo_por_classe


def _year_range(df: pd.DataFrame) -> tuple[int, int]:
    years = pd.to_numeric(df["ano"], errors="coerce").dropna().astype(int)
    return int(years.min()), int(years.max())


def _render_total_ativo(df: pd.DataFrame) -> None:
    st.subheader("Evolução do Acervo Ativo Anual")
    st.caption("Total de processos ativos ao final de cada ano, somando todas as classes.")
    with st.expander("Critério / Caminho dos dados"):
        st.markdown(
            "- **Fonte:** `data/processed/acervo/evolucao_acervo.parquet`  \n"
            "- **Métrica:** `quantidade_ativos` — soma de ADI + ADC + ADO + ADPF  \n"
            "- **Referência:** 31/12 de cada ano  \n"
            "- **Marcos:** ER 51/2016, ER 52/2019, ER 53/2020 e ESPIN (2020–2022)"
        )
    show_values = st.checkbox("Exibir valores", value=False, key="total_show_values")
    st.plotly_chart(fig_total_ativo_anual(df, show_values), use_container_width=True)


def _render_por_classe(df: pd.DataFrame) -> None:
    st.subheader("Evolução do Acervo Ativo Anual por Classe")
    st.caption("Barras da classe selecionada com linha do total geral no eixo secundário.")
    with st.expander("Critério / Caminho dos dados"):
        st.markdown(
            "- **Fonte:** `data/processed/acervo/evolucao_acervo.parquet`  \n"
            "- **Eixo esquerdo:** `quantidade_ativos` da classe  \n"
            "- **Eixo direito:** total geral do STF (todas as classes)  \n"
            "- **Marcos:** ER 51/2016, ER 52/2019, ER 53/2020 e ESPIN (2020–2022)"
        )
    show_values = st.checkbox("Exibir valores", value=False, key="classe_show_values")

    classes = sorted(df["classe"].dropna().unique().tolist())
    tabs = st.tabs(classes)
    for tab, classe in zip(tabs, classes):
        with tab:
            st.plotly_chart(fig_ativo_por_classe(df, classe, show_values), use_container_width=True)


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


def render_graficos(df: pd.DataFrame) -> None:
    st.markdown("---")
    _render_total_ativo(df)

    st.markdown("---")
    _render_por_classe(df)

    st.markdown("---")
    _render_tabela(df)

    st.markdown("---")
    with st.expander("Diagnóstico Analítico e Conclusões da Série Histórica", expanded=True):
        st.markdown("""
### 1. O Impacto das Reformas Regimentais (ER 51, 52 e 53)
Diferente de uma visão puramente cumulativa, os gráficos de acervo ativo revelam que o tribunal iniciou um processo de "limpeza" e aceleração de baixas a partir de 2016.

- **ER 51/2016 e ER 52/2019:** Marcam o início de uma tendência de estabilização e posterior queda no estoque pendente, ao conferir maior agilidade aos julgamentos monocráticos e virtuais.
- **ER 53/2020:** Este é o marco mais visível. Mesmo durante a pandemia, a expansão do Plenário Virtual permitiu que o STF reduzisse o acervo ativo de forma drástica, revertendo a curva de crescimento que durava décadas.

### 2. Bipolaridade: ADI vs. ADPF
O perfil da litigiosidade concentrada mudou de face:

- **Hegemonia da ADI:** Embora continue sendo a classe majoritária, a ADI apresentou sua primeira queda sustentada de volume na última década, saindo de picos históricos para níveis mais controláveis em 2025.
- **Protagonismo da ADPF:** Enquanto as ADIs estabilizaram, as ADPFs tornaram-se o instrumento preferencial para questões urgentes e direitos fundamentais, mantendo uma curva de relevância alta mesmo com os esforços de redução de acervo.

### 3. O Efeito ESPIN (2020–2022)
O período da Emergência em Saúde Pública (ESPIN) não paralisou o tribunal. Pelo contrário, os dados mostram que a produtividade em ambiente virtual superou a entrada de novos casos no período. O sombreado no gráfico demonstra que o acervo continuou a cair durante a crise sanitária, provando a resiliência operacional do modelo de julgamento digital adotado.

### 4. Eficiência Operacional e Acervo Residual
A queda acentuada nos últimos 5 anos sugere que o tribunal está conseguindo enfrentar o "estoque histórico". O desafio para 2025 em diante deixa de ser apenas o volume bruto e passa a ser a gestão das novas ações que entram com complexidade jurídica cada vez maior, exigindo que a celeridade do Plenário Virtual não comprometa a densidade dos debates.
        """)
