"""
src package — STF Plenário Virtual (pure library + orchestration).

Design (after 2026-06 refactoring):
- json_transforme.py  : pure, side-effect-free transforms only.
- cleaning.py         : high-level pipeline orchestration + public API + thin CLI.
- filters.py / viz.py : reusable helpers for dashboard and notebooks.

After `pip install -e .` (recommended), imports are clean:
    from src.cleaning import run_pipeline
    from src import json_transforme
    from app.data_loader import load_andamentos
"""

from .cleaning import (
    load_raw_csv,
    parse_liminar,
    parse_assuntos,
    prepare_processos_base,
    run_pipeline,
)

from .json_transforme import (
    explodir_json,
    processar_andamentos,
    processar_decisoes,
    processar_deslocamentos,
)

from . import filters as filters  # reexport module: from src.filters import ...

__all__ = [
    "load_raw_csv",
    "parse_liminar",
    "parse_assuntos",
    "prepare_processos_base",
    "run_pipeline",
    "explodir_json",
    "processar_andamentos",
    "processar_decisoes",
    "processar_deslocamentos",
    "filters",
]
