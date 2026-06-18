import sys
import bootstrap
import plotly.express as px
import streamlit as st
from pathlib import Path
from data.loader import load_evolucao_acervo

# ── Path setup ───────────────────────────────────────────────────────────────
_here = Path(__file__).resolve()
_root = _here.parent.parent if _here.parent.name == "pages" else _here.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

# ── Configuração da página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Acervo Histórico - STF",
    page_icon="⚖️",
    layout="wide",
)

st.title("Evolução e Perfil do Acervo")
st.markdown(
    "Análise evolutiva do estoque de processos ativos do Controle Concentrado "
    "(ADI, ADC, ADO e ADPF) entre 1988 e 2025."
)

# ── Carregamento dos dados ───────────────────────────────────────────────────
try:
    df = load_evolucao_acervo()
except Exception as e:
    st.error(f"Erro ao conectar com o Data Lake do Hugging Face: {e}")
    st.info("Se o repositório for privado, configure HF_TOKEN nos Secrets do Streamlit Cloud.")
    st.stop()

# ── Validação defensiva ──────────────────────────────────────────────────────
colunas_esperadas = {"ano", "quantidade_ativos", "classe"}
if not colunas_esperadas.issubset(df.columns):
    st.error(f"Colunas esperadas não encontradas. Colunas disponíveis: {list(df.columns)}")
    st.stop()

if df.empty:
    st.warning("O dataframe retornou vazio.")
    st.stop()

# ── Gráfico 1: Linha do tempo ────────────────────────────────────────────────
st.markdown("---")
st.subheader("Linha do Tempo por Classe")
st.caption("Clique na legenda para isolar uma classe processual.")

fig_linha = px.line(
    df,
    x="ano",
    y="quantidade_ativos",
    color="classe",
    markers=True,
    labels={
        "ano": "Ano de Referência",
        "quantidade_ativos": "Processos Ativos",
        "classe": "Classe",
    },
)
fig_linha.update_layout(
    template="plotly_white",
    xaxis=dict(dtick=4),
    margin=dict(l=20, r=20, t=20, b=20),
)
st.plotly_chart(fig_linha, use_container_width=True)

# ── Gráfico 2: Composição proporcional ──────────────────────────────────────
st.markdown("---")
st.subheader("Composição Proporcional do Volume")
st.caption("Volumetria total acumulada ano a ano, por classe.")

fig_barra = px.bar(
    df,
    x="ano",
    y="quantidade_ativos",
    color="classe",
    labels={
        "ano": "Ano",
        "quantidade_ativos": "Volume Total",
        "classe": "Classe",
    },
)
fig_barra.update_layout(
    template="plotly_white",
    xaxis=dict(dtick=4),
    margin=dict(l=20, r=20, t=20, b=20),
)
st.plotly_chart(fig_barra, use_container_width=True)

# ── Diagnóstico analítico ────────────────────────────────────────────────────
st.markdown("---")
with st.expander("Diagnóstico Analítico e Conclusões da Série Histórica", expanded=True):
    st.markdown("""
### 1. Crescimento Ininterrupto do Acervo Total
O estoque total saltou de apenas **11 processos em 1988** para **9.142 processos ativos em 2025**.
O crescimento linear e contínuo sinaliza que a taxa de entrada de novas ações e o tempo de
tramitação superam consistentemente a capacidade de baixa definitiva do tribunal.

### 2. A Hegemonia Absoluta da ADI
A Ação Direta de Inconstitucionalidade (ADI) é o principal motor do controle concentrado.
Em 2025, com 7.678 processos, as **ADIs sozinhas respondem por aproximadamente 84% de todo o acervo ativo**.

### 3. A Ascensão Meteórica da ADPF
A ADPF surge no ano 2000 e apresentou o crescimento proporcional mais agressivo, atingindo
**1.279 processos em 2025**. O maior salto ocorreu na última década, impulsionado pelo uso
estratégico da classe para contestar atos do poder executivo e omissões governamentais.

### 4. O Papel Residual de ADCs e ADOs
Tanto as ADCs quanto as ADOs mantêm volumes estritamente controlados e marginais
(95 e 90 processos em 2025, respectivamente), refletindo o caráter mais restrito de suas
hipóteses de cabimento.
    """)