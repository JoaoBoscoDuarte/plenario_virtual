"""Renderização da página de Acervo — só usa st.*, não constrói figuras."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from .plots import fig_evolucao_acervo, fig_composicao_proporcional


def render_controles_evolucao(show_values: bool) -> tuple[bool, bool]:
    """
    Renderiza os controles específicos do gráfico de evolução.
    Retorna (use_bar, local_line_labels).
    """
    chart_type = st.radio(
        "Tipo de visualização (Evolução do Acervo)",
        options=["Gráfico de Linhas", "Gráfico de Barras"],
        horizontal=True,
        index=0,
    )
    local_line_labels = st.checkbox(
        "Exibir rótulos nos pontos",
        value=show_values,
        disabled=not show_values,
        help=(
            "Ativa rótulos nos pontos da linha. "
            "Desabilitado quando o toggle global está desligado."
        ),
    )
    return chart_type == "Gráfico de Barras", local_line_labels


def render_graficos(df: pd.DataFrame, show_values: bool) -> None:
    """Renderiza todos os gráficos e textos da página de Acervo."""

    # Gráfico 1 — Evolução
    st.markdown("---")
    st.subheader("Evolução do Acervo Ativo")
    use_bar, show_labels = render_controles_evolucao(show_values)

    st.plotly_chart(
        fig_evolucao_acervo(df, use_bar=use_bar, show_values=show_labels),
        use_container_width=True,
    )

    # Gráfico 2 — Composição proporcional
    st.markdown("---")
    st.subheader("Composição Proporcional do Volume")
    st.caption("Volumetria total acumulada ano a ano, por classe.")
    st.plotly_chart(
        fig_composicao_proporcional(df, show_values=show_values),
        use_container_width=True,
    )

    # Diagnóstico
    st.markdown("---")
    with st.expander(
        "Diagnóstico Analítico e Conclusões da Série Histórica", expanded=True
    ):
        st.markdown("""
### 1. Crescimento Ininterrupto do Acervo Total
O estoque total saltou de apenas **11 processos em 1988** para **9.142 processos ativos em 2025**.
O crescimento linear e contínuo sinaliza que a taxa de entrada de novas ações e o tempo de
tramitação superam consistentemente a capacidade de baixa definitiva do tribunal.

### 2. A Hegemonia Absoluta da ADI
A ADI é o principal motor do controle concentrado. Em 2025, com 7.678 processos,
as **ADIs sozinhas respondem por aproximadamente 84% de todo o acervo ativo**.

### 3. A Ascensão Meteórica da ADPF
A ADPF surge no ano 2000 e apresentou o crescimento proporcional mais agressivo,
atingindo **1.279 processos em 2025**, impulsionado pelo uso estratégico da classe
para contestar atos do poder executivo e omissões governamentais.

### 4. O Papel Residual de ADCs e ADOs
ADCs e ADOs mantêm volumes marginais (95 e 90 processos em 2025, respectivamente),
refletindo o caráter mais restrito de suas hipóteses de cabimento.
        """)
