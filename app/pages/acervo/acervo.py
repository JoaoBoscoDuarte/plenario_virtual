"""Página: Acervo Histórico."""

import sys
from pathlib import Path

import streamlit as st

# ── Path setup ───────────────────────────────────────────────────────────────
# Precisa vir antes dos imports locais (data, components, pages.acervo.layout)
# porque st.navigation executa este arquivo via exec(), sem pacote pai —
# imports relativos (from .layout import ...) não funcionam aqui.
_here = Path(__file__).resolve()
_root = _here.parent.parent.parent  # /app
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from data.loader import load_evolucao_acervo
from pages.acervo.layout import render_graficos

# ── Dados ────────────────────────────────────────────────────────────────────
try:
    df = load_evolucao_acervo()
except Exception as e:
    st.error(f"Erro ao conectar com o Data Lake do Hugging Face: {e}")
    st.info(
        "Configure HF_TOKEN nos Secrets do Streamlit Cloud se o repositório for privado."
    )
    st.stop()

colunas_esperadas = {"ano", "quantidade_ativos", "classe"}
if not colunas_esperadas.issubset(df.columns):
    st.error(f"Colunas esperadas não encontradas. Disponíveis: {list(df.columns)}")
    st.stop()
if df.empty:
    st.warning("O dataframe retornou vazio.")
    st.stop()

# ── Cabeçalho ────────────────────────────────────────────────────────────────
st.title("Acervo")
st.markdown("""
Esta seção analisa o **acervo histórico de Controle Concentrado** do STF, compreendendo as 
quatro classes processuais de competência originatária do tribunal: ADI, ADC, ADO e ADPF. 
O acervo é medido como o estoque de processos **ativos ao final de cada ano** (referência 31/12), 
construindo uma série histórica desde a promulgação da Constituição de 1988 até 2025.

O objetivo é revelar a dinâmica de crescimento, a distribuição por classe e os padrões 
de litigiosidade que moldam a pauta do tribunal ao longo do tempo.
""")

st.markdown("""
**Nesta seção:**
- **Evolução do Acervo Ativo Anual** — total de processos ativos por ano (todas as classes), com marcos dos Regimentos Internos e período da ESPIN.
- **Evolução por Classe** — barras de cada classe com linha do total geral no eixo secundário.
- **Dados Brutos** — tabela com valores absolutos e percentuais por classe e ano.
""")

# ── Renderização ──────────────────────────────────────────────────────────────
render_graficos(df)
