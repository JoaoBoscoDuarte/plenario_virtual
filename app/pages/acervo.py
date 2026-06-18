# Garante que "data" e "bootstrap" sejam importáveis no Streamlit Cloud
import sys
import bootstrap
import plotly.express as px
import streamlit as st

from pathlib import Path
from data.loader import load_evolucao_acervo

_here = Path(__file__).resolve()
_root = _here.parent.parent if _here.parent.name == "pages" else _here.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))


# 1. Configuração da Página para modo Expandido (Wide)
st.set_page_config(
    page_title="Acervo Histórico - STF",
    page_icon="",
    layout="wide"
)

st.title("Evolução e Perfil do Acervo")
st.markdown(
    "Análise evolutiva do estoque de processos ativos do Controle Concentrado (ADI, ADC, ADO e ADPF) entre 1988 e 2025."
)

# 2. Carregamento Seguro dos Dados
try:
    df_evolucao_acervo = load_evolucao_acervo()

except Exception as e:
    st.error(f"Erro crítico ao conectar com o Data Lake do Hugging Face: {e}")
    st.info("Dica: Se o repositório for privado, configure HF_TOKEN nos Secrets do Streamlit Cloud.")
    st.stop()

st.markdown("---")

# 3. Construção do Layout em Colunas Lado a Lado
col1, col2 = st.columns(2)

with col1:
    st.subheader("Linha do Tempo por Classe")
    st.caption("Valores marcados nos nós. Clique na legenda lateral para isolar uma classe processual.")

    fig1 = px.line(
        df_evolucao_acervo,
        x="ano",
        y="quantidade_ativos",
        color="classe",
        text_auto=False,
        #text="quantidade_ativos",
        labels={
            "ano": "Ano de Referência",
            "quantidade_ativos": "Processos Ativos",
            "classe": "Classe",
        },
        markers=True,
    )
    fig1.update_traces(textposition="top center")
    fig1.update_layout(
        template="plotly_white",
        xaxis=dict(dtick=4),
        margin=dict(l=20, r=20, t=20, b=20),
    )

    # Renderiza o gráfico nativamente no Streamlit ocupando 100% da sua coluna
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Composição Proporcional do Volume")
    st.caption("Visão empilhada demonstrando a volumetria total acumulada ano a ano.")

    fig2 = px.bar(
        df_evolucao_acervo,
        x="ano",
        y="quantidade_ativos",
        color="classe",
        text_auto=False,
        labels={
            "ano": "Ano",
            "quantidade_ativos": "Volume Total",
            "classe": "Classe",
        },
    )
    fig2.update_layout(
        template="plotly_white",
        xaxis=dict(dtick=4),
        margin=dict(l=20, r=20, t=20, b=20),
    )

    st.plotly_chart(fig2, use_container_width=True)

# 4. Seção de Conclusões Metodológicas e Jurimétricas
st.markdown("---")
with st.expander("Ver Diagnóstico Analítico e Conclusões da Série Histórica", expanded=True):
    st.markdown(
        """
    ### 1. Crescimento Ininterrupto do Acervo Total
    O estoque total saltou de apenas **11 processos em 1988** para **9.142 processos ativos em 2025**. O crescimento linear e contínuo sinaliza que a taxa de entrada de novas ações e o tempo de tramitação superam consistentemente a capacidade de baixa definitiva do tribunal.
    
    ### 2. A Hegemonia Absoluta da ADI
    A Ação Direta de Inconstitucionalidade (ADI) é o principal motor do controle concentrado. Em 2025, com 7.678 processos, as **ADIs sozinhas respondem por aproximadamente 84% de todo o acervo ativo**.
    
    ### 3. A Ascensão Meteórica da ADPF
    A Arguição de Descumprimento de Preceito Fundamental (ADPF) surge no ano 2000 e apresentou o crescimento proporcional mais agressivo, atingindo **1.279 processos em 2025**. O maior salto ocorreu na última década, impulsionado pelo uso estratégico da classe para contestar atos do poder executivo e omissões governamentais.
    
    ### 4. O Papel Residual de ADCs e ADOs
    Tanto as Ações Declaratórias de Constitucionalidade (ADC) quanto as Ações Diretas por Omissão (ADO) mantêm volumes estritamente controlados e marginais (95 e 90 processos em 2025, respectivamente), refletindo o caráter mais específico e restrito de suas hipóteses de cabimento.
    """
    )