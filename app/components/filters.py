"""Componentes de filtro reutilizáveis para o sidebar do Streamlit.

Cada função renderiza um widget no sidebar e retorna os valores selecionados.
A aplicação dos filtros fica a cargo da página, usando data/filters.py.

Suporta tanto datasets agregados (ex: evolucao_acervo com coluna "ano")
quanto a tabela principal (data_protocolo + classe, tipo_processo etc).
"""
from __future__ import annotations

from typing import Any

import streamlit as st
import pandas as pd


def _safe_unique_sorted(df: pd.DataFrame, col: str) -> list:
    """Retorna lista única ordenada da coluna. Retorna [] defensivamente."""
    if df is None or df.empty or col not in df.columns:
        return []
    
    try:
        vals = df[col].dropna().unique().tolist()
        return sorted(vals, key=lambda x: (str(x) if not isinstance(x, (int, float)) else x))
    
    except Exception:
        return []


def _get_year_series(df: pd.DataFrame, col: str = "ano", date_fallback: str = "data_protocolo") -> pd.Series:
    """Retorna Series de anos (int) a partir de col de ano ou derivando de data."""
    if df is None or df.empty:
        return pd.Series(dtype="int")
    
    if col in df.columns:
        s = pd.to_numeric(df[col], errors="coerce").dropna().astype(int)
        if not s.empty:
            return s
        
    # fallback: derivar ano de coluna de data
    if date_fallback in df.columns:
        try:
            dt = pd.to_datetime(df[date_fallback], errors="coerce")
            return dt.dt.year.dropna().astype(int)
        
        except Exception:
            pass

    return pd.Series(dtype="int")


def multiselect_filter(df: pd.DataFrame, col: str, label: str | None = None) -> list[str]:
    """Multiselect genérico. Retorna lista de valores selecionados (strings).

    Se a coluna não existir ou df vazio, retorna [] (página decide o que fazer).
    """
    opcoes = [str(x) for x in _safe_unique_sorted(df, col)]
    if not opcoes:
        return []
    
    display_label = label or col.replace("_", " ").title()
    return st.sidebar.multiselect(display_label, options=opcoes, default=opcoes)


def year_range_filter(
    df: pd.DataFrame, col: str = "ano", date_col_fallback: str = "data_protocolo"
) -> tuple[int, int]:
    """Slider de intervalo de anos.

    Funciona com coluna de ano (int) ou deriva o intervalo de uma coluna de data.
    Retorna (ano_inicio, ano_fim). Se impossível determinar, retorna (0, 0).
    """
    years = _get_year_series(df, col=col, date_fallback=date_col_fallback)
    if years.empty:
        # fallback seguro: não quebra a página
        return (0, 0)
    
    y_min, y_max = int(years.min()), int(years.max())

    if y_min == y_max:
        # slider de 1 valor precisa de range maior; devolve o mesmo duas vezes
        return (y_min, y_max)
    
    return st.sidebar.slider(
        "Período (ano)",
        min_value=y_min,
        max_value=y_max,
        value=(y_min, y_max),
        step=1,
    )


# ------------------------------------------------------------------
# Filtros específicos (mantidos por compatibilidade com acervo + docs)
# ------------------------------------------------------------------

def filtro_periodo_ano(df: pd.DataFrame, col: str = "ano") -> tuple[int, int]:
    """Slider de intervalo de anos (específico). Delega para year_range_filter."""
    return year_range_filter(df, col=col, date_col_fallback="data_protocolo")


def filtro_classe(df: pd.DataFrame, col: str = "classe") -> list[str]:
    """Multiselect de classes processuais. Delega para multiselect_filter."""
    # Mantém o label exato do filters.md para consistência visual
    opcoes = [str(x) for x in _safe_unique_sorted(df, col)]

    if not opcoes:
        return []
    
    return st.sidebar.multiselect(
        "Classe processual",
        options=opcoes,
        default=opcoes,
    )


def render_sidebar_filters(df: pd.DataFrame) -> dict[str, Any]:
    """Renderiza os filtros padrão da página de acervo (ano + classe).

    Ponto de entrada conveniente. Retorna dict pronto para aplicação.

    Uso recomendado na página:
        from components.filters import render_sidebar_filters
        from data.filters import filter_by_values

        filtros = render_sidebar_filters(df)
        df_filtrado = filter_by_values(df, "classe", filtros["classes"])
        ai, af = filtros["periodo"]
        df_filtrado = df_filtrado[df_filtrado["ano"].between(ai, af)]
    """
    with st.sidebar:
        st.header("Filtros")
        periodo = filtro_periodo_ano(df)
        classes = filtro_classe(df)

    return {
        "periodo": periodo,   # (ano_inicio, ano_fim)
        "classes": classes,   # ["ADI", "ADC", ...]
    }
