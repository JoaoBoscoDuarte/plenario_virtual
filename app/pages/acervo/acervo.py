"""Página: Acervo Histórico."""

import sys
from pathlib import Path

import streamlit as st

from data.loader import load_evolucao_acervo
from data.filters import filter_by_values
from components.filters import (
    render_sidebar_filters,
    class_selector_with_geral,
    show_values_toggle,
    prepare_class_or_geral,
)
from .layout import render_graficos

# ── Path setup ───────────────────────────────────────────────────────────────
_here = Path(__file__).resolve()
_root = _here.parent.parent.parent  # /app
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

# ── Configuração ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Acervo Histórico",
    page_icon="⚖️",
    layout="wide",
)

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
st.markdown(
    "Evolução anual do acervo geral de Controle Concentrado (ADI, ADC, ADO e ADPF), "
    "período 1988–2025, referência 31/12 de cada ano. Unidade: processo."
)
with st.expander("Critério / Caminho dos dados"):
    st.markdown("""
- **Período:** 1988 a 2025.
- **Data de referência:** 31/12 de cada ano.
- **Unidade:** processo.
> Excluídos processos com andamentos de "baixa ao arquivo", "baixa definitiva dos autos",
> "baixa dos autos" ou "processo findo" ao longo do ano.
    """)

# ── Filtros ───────────────────────────────────────────────────────────────────
filtros = render_sidebar_filters(df)
class_sel = class_selector_with_geral(df)
show_values = show_values_toggle()

ai, af = filtros.get("periodo", (int(df["ano"].min()), int(df["ano"].max())))
df_filtrado = filter_by_values(df, "classe", filtros.get("classes"))
df_filtrado = df_filtrado[df_filtrado["ano"].between(ai, af)].copy()
df_filtrado = prepare_class_or_geral(
    df_filtrado, value_col="quantidade_ativos", class_col="classe", selection=class_sel
)

if df_filtrado.empty:
    st.warning("Nenhum registro após aplicação dos filtros.")
    st.stop()

st.caption(f"Mostrando {len(df_filtrado)} registros após filtros (período {ai}–{af}).")

# ── Renderização ──────────────────────────────────────────────────────────────
render_graficos(df_filtrado, show_values=show_values)
