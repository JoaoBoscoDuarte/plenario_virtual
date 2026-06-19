import sys
import bootstrap
import plotly.express as px
import streamlit as st

from pathlib import Path
from data.loader import load_evolucao_acervo
from components.filters import (
    render_sidebar_filters,
    class_selector_with_geral,
    show_values_toggle,
    prepare_class_or_geral,
)
from data.filters import filter_by_values

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

with st.expander("Critério / Caminho dos dados (Gráficos 1 e 2)"):
    st.markdown("""
**Gráfico 1 (Geral) e Gráfico 2 (por classe):**
- Período: 1988 a 2025 (ou a partir de 2000 se dados iniciais inconsistentes).
- Data de referência: 31/12 de cada ano.
- Unidade: processo.
- Exclui processos com andamentos de “baixa ao arquivo”, “baixa definitiva dos autos”, “baixa dos autos” ou “processo findo” ao longo do ano (ou usa critério de processos que tiveram algum andamento no ano).
- Fonte principal: `evolucao_acervo.parquet` (pré-computado) com filtros dinâmicos de ano e classe/Geral aplicados no app.
""")

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

# ── Filtros globais (novos componentes exigidos) ─────────────────────────────
filtros = render_sidebar_filters(df)

# Novo seletor de classe com opção "Geral"
class_sel = class_selector_with_geral(df)

# Toggle global de exibição de valores
show_values = show_values_toggle()

df_filtrado = filter_by_values(df, "classe", filtros.get("classes"))

ai, af = filtros.get("periodo", (int(df["ano"].min()), int(df["ano"].max())))
if "ano" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["ano"].between(ai, af)].copy()

# Aplicar lógica de "Geral" (agregação) ou classes específicas
df_filtrado = prepare_class_or_geral(
    df_filtrado,
    value_col="quantidade_ativos",
    class_col="classe",
    selection=class_sel
)

if df_filtrado.empty:
    st.warning("Nenhum registro após aplicação dos filtros.")
    st.stop()

st.caption(f"Mostrando {len(df_filtrado)} registros após filtros (período {ai}–{af}).")

# ── Controles específicos do Gráfico de Evolução do Acervo ───────────────────
st.markdown("---")

# Radio específico exigido para o Gráfico de Evolução anual do acervo por classe
chart_type = st.radio(
    "Tipo de visualização (Evolução do Acervo)",
    options=["Gráfico de Linhas", "Gráfico de Barras"],
    horizontal=True,
    index=0
)

# Checkbox específico para rótulos em linha (sincronizado com o global)
labels_disabled = not show_values
local_line_labels = st.checkbox(
    "Exibir rótulos nos pontos",
    value=show_values,
    disabled=labels_disabled,
    help="Ativa rótulos nos pontos da linha. Desabilitado quando o toggle global 'Exibir valores nos gráficos' está desligado."
)

# ── Gráfico principal de Evolução (suporta Linha/Barras + toggle de valores) ─
st.subheader("Evolução do Acervo Ativo")

use_bar = chart_type == "Gráfico de Barras"

fig = px.line(
    df_filtrado,
    x="ano",
    y="quantidade_ativos",
    color="classe",
    markers=True,
    labels={
        "ano": "Ano de Referência",
        "quantidade_ativos": "Processos Ativos",
        "classe": "Classe",
    },
    title="Evolução anual do acervo – por classe / Geral",
)

if use_bar:
    # Reconstrói como barras quando o usuário escolher
    fig = px.bar(
        df_filtrado,
        x="ano",
        y="quantidade_ativos",
        color="classe",
        labels={
            "ano": "Ano de Referência",
            "quantidade_ativos": "Processos Ativos",
            "classe": "Classe",
        },
        title="Evolução anual do acervo – por classe / Geral",
    )

# Controle de rótulos de valor (global + específico da linha)
if show_values:
    text_val = df_filtrado["quantidade_ativos"] if "quantidade_ativos" in df_filtrado.columns else None
    fig.update_traces(
        text=text_val,
        textposition="top center" if not use_bar else "outside"
    )

fig.update_layout(
    template="plotly_white",
    xaxis=dict(dtick=1),
    yaxis=dict(autorange=True),
    margin=dict(l=20, r=20, t=40, b=20),
)

st.plotly_chart(fig, use_container_width=True)

# ── Gráfico secundário (composição) ──────────────────────────────────────────
st.markdown("---")
st.subheader("Composição Proporcional do Volume")
st.caption("Volumetria total acumulada ano a ano, por classe.")

fig_barra = px.bar(
    df_filtrado,
    x="ano",
    y="quantidade_ativos",
    color="classe",
    labels={
        "ano": "Ano",
        "quantidade_ativos": "Volume Total",
        "classe": "Classe",
    },
)

if show_values:
    fig_barra.update_traces(text=df_filtrado["quantidade_ativos"], textposition="outside")

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