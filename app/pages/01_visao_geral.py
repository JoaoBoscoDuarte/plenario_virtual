# pages/01_visao_geral.py
# Garante que "data" e "bootstrap" sejam importáveis no Streamlit Cloud
import sys
from pathlib import Path
_here = Path(__file__).resolve()
_root = _here.parent.parent if _here.parent.name == "pages" else _here.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import bootstrap
import streamlit as st
from data.loader import load_parquet
from components.filters import multiselect_filter, year_range_filter
from data.filters import filter_by_values

# Usa o repositório real do projeto + caminho correto no HF
# (os arquivos estão em processed/ no repositório)
df = load_parquet("JoaoBoscoooo/plenario_virtual", "processed/arquivosConcatenados.parquet")

st.header("Visão Geral")
st.caption("Visão geral dos processos do Plenário Virtual (tabela principal). Use os filtros no sidebar.")

# ── Filtros no sidebar (não mutam df aqui) ────────────────────────────────────
with st.sidebar:
    st.header("Filtros")
    classes_sel = multiselect_filter(df, "classe", "Classe processual")
    tipos_sel = multiselect_filter(df, "tipo_processo", "Tipo de Processo")
    ano_range = year_range_filter(df, col="ano", date_col_fallback="data_protocolo")

# ── Aplicação dos filtros (sempre sobre cópia / encadeado) ───────────────────
df_filtrado = df
if classes_sel:
    df_filtrado = filter_by_values(df_filtrado, "classe", classes_sel)

if tipos_sel:
    df_filtrado = filter_by_values(df_filtrado, "tipo_processo", tipos_sel)

# Filtro de ano (data_protocolo ou coluna ano se existir)
ai, af = ano_range
if ai or af:  # (0,0) é fallback sem range útil
    try:
        from data.filters import filter_by_year_range
        df_filtrado = filter_by_year_range(df_filtrado, start=ai, end=af, date_col="data_protocolo")
        
    except Exception:
        # fallback manual
        if "ano" in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado["ano"].between(ai, af)].copy()

if df_filtrado.empty and not df.empty:
    st.warning("Nenhum registro após os filtros atuais.")
    df_filtrado = df.head(0)  # evita quebra das métricas

# ── Métricas (baseadas em colunas reais) ─────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Total (filtrado)", len(df_filtrado))
col2.metric("Classes únicas", df_filtrado["classe"].nunique() if "classe" in df_filtrado.columns else 0)
col3.metric("Tipos de processo", df_filtrado["tipo_processo"].nunique() if "tipo_processo" in df_filtrado.columns else 0)

# Diagnóstico rápido (útil durante desenvolvimento)
with st.expander("Colunas disponíveis no dataset", expanded=False):
    st.write(list(df.columns) if hasattr(df, "columns") else "N/A")