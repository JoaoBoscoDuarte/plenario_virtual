"""Funções de recorte e filtragem reutilizáveis.

Usado pelo dashboard Streamlit (sidebar global e páginas) e por notebooks
de análise. Mantém a lógica de filtros fora do app para fácil teste e reuso.
"""
from __future__ import annotations

from typing import Any

import pandas as pd


def filter_by_date_range(
    df: pd.DataFrame,
    date_col: str,
    start: Any | None = None,
    end: Any | None = None,
) -> pd.DataFrame:
    
    """Filtra df por coluna de data (datetime) entre start e end (inclusive)."""
    if date_col not in df.columns:
        return df
    
    mask = pd.Series([True] * len(df), index=df.index)

    if start is not None:
        mask &= df[date_col] >= pd.to_datetime(start)

    if end is not None:
        mask &= df[date_col] <= pd.to_datetime(end)

    return df[mask].copy()


def filter_by_values(df: pd.DataFrame, column: str, values: list | set | None) -> pd.DataFrame:
    """Mantém apenas linhas cujo valor da coluna está em values (se values não vazio)."""

    if not values or column not in df.columns:
        return df
    
    return df[df[column].isin(values)].copy()


def filter_by_text_search(df: pd.DataFrame, columns: list[str], query: str | None) -> pd.DataFrame:
    """Busca simples case-insensitive em uma ou mais colunas de texto."""
    if not query or not columns:
        return df
    q = str(query).lower().strip()

    if not q:
        return df
    mask = pd.Series([False] * len(df), index=df.index)

    for col in columns:
        if col in df.columns:
            mask |= df[col].astype(str).str.lower().str.contains(q, na=False)
            
    return df[mask].copy()
