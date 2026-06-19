"""Camada de dados: lógica pura de filtragem (sem Streamlit).

Fonte da verdade para todas as funções de filtragem do projeto.
Não importa Streamlit. Funções sempre retornam .copy().
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
    """Filtra df por coluna de data entre start e end (inclusive)."""
    if date_col not in df.columns:
        return df
    mask = pd.Series([True] * len(df), index=df.index)
    if start is not None:
        mask &= df[date_col] >= pd.to_datetime(start)
    if end is not None:
        mask &= df[date_col] <= pd.to_datetime(end)
    return df[mask].copy()


def filter_by_values(
    df: pd.DataFrame,
    column: str,
    values: list | set | None,
) -> pd.DataFrame:
    """Mantém apenas linhas cujo valor da coluna está em values."""
    if not values or column not in df.columns:
        return df
    return df[df[column].isin(values)].copy()


def filter_by_text_search(
    df: pd.DataFrame,
    columns: list[str],
    query: str | None,
) -> pd.DataFrame:
    """Busca case-insensitive em uma ou mais colunas de texto."""
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


def filter_by_year_range(
    df: pd.DataFrame,
    year: int | None = None,
    start: int | None = None,
    end: int | None = None,
    year_col: str = "ano",
    date_col: str = "data_protocolo",
) -> pd.DataFrame:
    """Filtra por ano exato ou intervalo de anos.

    Aceita year_col (coluna inteira de ano) ou date_col (extrai o ano da data).
    """
    if df is None or df.empty:
        return df

    if year_col in df.columns:
        years = pd.to_numeric(df[year_col], errors="coerce")
    elif date_col in df.columns:
        years = pd.to_datetime(df[date_col], errors="coerce").dt.year
    else:
        return df.copy()

    mask = pd.Series([True] * len(df), index=df.index)
    if year is not None:
        mask &= years == year
    if start is not None:
        mask &= years >= start
    if end is not None:
        mask &= years <= end

    return df[mask].copy()


def prepare_class_or_geral(
    df: pd.DataFrame,
    value_col: str,
    class_col: str = "classe",
    selection: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """Prepara o DataFrame para plot conforme seleção de classe ou visão Geral.

    - use_geral=True: agrega todas as classes somando value_col, cria coluna class_col="Geral".
    - use_geral=False: filtra pelas classes em selection["selected"].

    Sempre retorna cópia.
    """
    if df is None or df.empty:
        return df

    if selection is None:
        return df.copy()

    use_geral = selection.get("use_geral", False)
    selected = selection.get("selected", [])

    if use_geral:
        group_keys = [c for c in df.columns if c not in (class_col, value_col)]

        # Garante ao menos uma chave de agrupamento temporal
        if not group_keys:
            for c in ["ano", "year"]:
                if c in df.columns:
                    group_keys = [c]
                    break

        if group_keys:
            agg = df.groupby(group_keys, as_index=False)[value_col].sum()
            agg[class_col] = "Geral"
            return agg

        # Último recurso: linha única com total
        return pd.DataFrame({class_col: ["Geral"], value_col: [df[value_col].sum()]})

    if selected:
        return df[df[class_col].astype(str).isin([str(s) for s in selected])].copy()

    return df.copy()


__all__ = [
    "filter_by_date_range",
    "filter_by_values",
    "filter_by_text_search",
    "filter_by_year_range",
    "prepare_class_or_geral",
]
