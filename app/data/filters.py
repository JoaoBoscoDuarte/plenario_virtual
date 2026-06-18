"""Camada de dados: lógica pura de filtragem (sem Streamlit).

Reexporta src.filters para satisfazer `from data.filters import ...`
(exatamente como descrito em filters.md), mantendo src/ como fonte única de verdade.

Pode ser usado em:
- páginas do Streamlit (após bootstrap)
- notebooks
- testes
- scripts

Funções sempre retornam .copy() para evitar mutação inesperada.
"""
from __future__ import annotations

from typing import Any

try:
    # Preferido após `pip install -e .`
    from src.filters import (
        filter_by_date_range,
        filter_by_values,
        filter_by_text_search,
        filter_by_year_range,
    )
except ImportError:
    # Fallback para execução direta de páginas (streamlit run app/pages/...)
    # ou ambientes sem o pacote instalado no path.
    import sys
    from pathlib import Path

    _proj = Path(__file__).resolve().parents[2]
    if str(_proj) not in sys.path:
        sys.path.insert(0, str(_proj))
        
    from src.filters import (
        filter_by_date_range,
        filter_by_values,
        filter_by_text_search,
        filter_by_year_range,
    )

__all__ = [
    "filter_by_date_range",
    "filter_by_values",
    "filter_by_text_search",
    "filter_by_year_range",
]
