"""Camada de dados: lógica pura de filtragem (sem Streamlit).

Reexporta src.filters (as funções estáveis) para satisfazer
`from data.filters import ...` conforme filters.md.

Fornece também `filter_by_year_range` de forma resiliente, mesmo que a
versão de src/filters.py no ambiente (ex: Streamlit Cloud deploy antigo)
ainda não contenha a função.

Funções sempre retornam .copy().
"""
from __future__ import annotations

from typing import Any

import pandas as pd

# ------------------------------------------------------------------
# Import das funções base (garantidas no src/filters.py original)
# ------------------------------------------------------------------
_base_imported = False

def _import_base_filters():
    """Tenta importar as 3 funções originais de src.filters de várias formas."""
    global filter_by_date_range, filter_by_values, filter_by_text_search

    # 1. Tenta import direto (pip install -e . ou PYTHONPATH configurado)
    try:
        from src.filters import (  # type: ignore
            filter_by_date_range as _d,
            filter_by_values as _v,
            filter_by_text_search as _t,
        )
        filter_by_date_range = _d
        filter_by_values = _v
        filter_by_text_search = _t
        return True
    except (ImportError, ModuleNotFoundError):
        pass

    # 2. Fallback: força o project root no sys.path
    try:
        import sys
        from pathlib import Path

        here = Path(__file__).resolve()
        # app/data/filters.py → parents[2] = project root
        proj_root = here.parents[2]
        if str(proj_root) not in sys.path:
            sys.path.insert(0, str(proj_root))

        from src.filters import (  # type: ignore
            filter_by_date_range as _d,
            filter_by_values as _v,
            filter_by_text_search as _t,
        )
        filter_by_date_range = _d
        filter_by_values = _v
        filter_by_text_search = _t
        return True
    except (ImportError, ModuleNotFoundError):
        pass

    return False


_imported_ok = _import_base_filters()

if not _imported_ok:
    # Último recurso: definir as funções localmente (cópia das originais)
    # para que o dashboard nunca quebre por causa de src.
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
        df: pd.DataFrame, column: str, values: list | set | None
    ) -> pd.DataFrame:
        if not values or column not in df.columns:
            return df
        return df[df[column].isin(values)].copy()

    def filter_by_text_search(
        df: pd.DataFrame, columns: list[str], query: str | None
    ) -> pd.DataFrame:
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


# ------------------------------------------------------------------
# filter_by_year_range — sempre fornecido pela camada app/data
# (não dependemos mais de src.filters ter esta função)
# ------------------------------------------------------------------
def filter_by_year_range(
    df: pd.DataFrame,
    year: int | None = None,
    start: int | None = None,
    end: int | None = None,
    year_col: str = "ano",
    date_col: str = "data_protocolo",
) -> pd.DataFrame:
    """Filtra por ano exato ou intervalo de anos.

    Funciona com year_col (int) ou date_col (extrai o ano).
    Sempre retorna uma cópia.
    """
    if df is None or df.empty:
        return df

    work = df.copy()

    if year_col in work.columns:
        years = pd.to_numeric(work[year_col], errors="coerce")
    elif date_col in work.columns:
        years = pd.to_datetime(work[date_col], errors="coerce").dt.year
    else:
        return work

    mask = pd.Series([True] * len(work), index=work.index)
    if year is not None:
        mask &= years == year
    if start is not None:
        mask &= years >= start
    if end is not None:
        mask &= years <= end

    return work[mask].copy()


__all__ = [
    "filter_by_date_range",
    "filter_by_values",
    "filter_by_text_search",
    "filter_by_year_range",
]
