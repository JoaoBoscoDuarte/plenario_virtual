"""Componentes de filtro reutilizáveis para o sidebar do Streamlit.

Cada função renderiza um widget no sidebar e retorna os valores selecionados.
A aplicação dos filtros e transformações de dados fica a cargo de data/filters.py.

Ponto de entrada único: render_sidebar_filters(df).
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

# ── Helpers internos ─────────────────────────────────────────────────────────


def _safe_unique_sorted(df: pd.DataFrame, col: str) -> list:
    """Retorna lista única ordenada da coluna. Retorna [] defensivamente."""
    if df is None or df.empty or col not in df.columns:
        return []
    try:
        vals = df[col].dropna().unique().tolist()
        return sorted(
            vals,
            key=lambda x: x if isinstance(x, (int, float)) else str(x),
        )
    except Exception:
        return []


def _get_year_series(
    df: pd.DataFrame,
    col: str = "ano",
    date_fallback: str = "data_protocolo",
) -> pd.Series:
    """Retorna Series de anos (int) a partir de coluna de ano ou de data."""
    if df is None or df.empty:
        return pd.Series(dtype="int")
    if col in df.columns:
        s = pd.to_numeric(df[col], errors="coerce").dropna().astype(int)
        if not s.empty:
            return s
    if date_fallback in df.columns:
        try:
            return (
                pd.to_datetime(df[date_fallback], errors="coerce")
                .dt.year.dropna()
                .astype(int)
            )
        except Exception:
            pass
    return pd.Series(dtype="int")


# ── Widgets primitivos (privados) ─────────────────────────────────────────────


def _widget_periodo_ano(
    df: pd.DataFrame,
    col: str = "ano",
    date_col_fallback: str = "data_protocolo",
) -> tuple[int, int]:
    """Slider de intervalo de anos. Retorna (ano_inicio, ano_fim)."""
    years = _get_year_series(df, col=col, date_fallback=date_col_fallback)
    if years.empty:
        return (0, 0)
    y_min, y_max = int(years.min()), int(years.max())
    if y_min == y_max:
        # Slider com range único não permite arrasto — retorna diretamente
        return (y_min, y_max)
    return st.sidebar.slider(
        "Período (ano)",
        min_value=y_min,
        max_value=y_max,
        value=(y_min, y_max),
        step=1,
    )


def _widget_classe(df: pd.DataFrame, col: str = "classe") -> list[str]:
    """Multiselect de classes processuais. Retorna lista de strings."""
    opcoes = [str(x) for x in _safe_unique_sorted(df, col)]
    if not opcoes:
        return []
    return st.sidebar.multiselect("Classe processual", options=opcoes, default=opcoes)


def _widget_show_values() -> bool:
    """Checkbox global de exibição de valores nos gráficos. Retorna bool."""
    return st.sidebar.checkbox(
        "Exibir valores nos gráficos",
        value=False,
        help="Mostra os valores totais sobre barras e pontos nos gráficos.",
    )


def _widget_class_selector_with_geral(
    df: pd.DataFrame, col: str = "classe"
) -> dict[str, Any]:
    """Seletor de classe com opção de visão agregada (Geral).

    Retorna:
        {
            "selected": list[str],
            "use_geral": bool,
        }
    """
    opcoes = [str(x) for x in _safe_unique_sorted(df, col)]
    if not opcoes:
        return {"selected": [], "use_geral": False}

    use_geral = st.sidebar.checkbox(
        "Geral (todas as classes)",
        value=False,
        help="Agrega todas as classes em uma única série somada.",
    )

    if use_geral:
        st.sidebar.multiselect(
            "Classe processual (ignorada no modo Geral)",
            options=opcoes,
            default=opcoes,
            disabled=True,
        )
        return {"selected": opcoes, "use_geral": True}

    selected = st.sidebar.multiselect(
        "Classe processual", options=opcoes, default=opcoes
    )
    return {"selected": selected, "use_geral": False}


# ── Ponto de entrada único ────────────────────────────────────────────────────


def render_sidebar_filters(df: pd.DataFrame) -> dict[str, Any]:
    """Renderiza todos os filtros do sidebar e retorna os valores selecionados.

    É o único símbolo que as páginas precisam importar deste módulo.

    Retorna:
        {
            "periodo":     (ano_inicio, ano_fim),
            "classes":     ["ADI", "ADC", ...],
            "class_sel":   {"selected": [...], "use_geral": bool},
            "show_values": bool,
        }

    Uso na página:
        from components.filters import render_sidebar_filters
        from data.filters import filter_by_values, prepare_class_or_geral

        filtros = render_sidebar_filters(df)

        ai, af = filtros["periodo"]
        df_filtrado = filter_by_values(df, "classe", filtros["classes"])
        df_filtrado = df_filtrado[df_filtrado["ano"].between(ai, af)]
        df_filtrado = prepare_class_or_geral(
            df_filtrado, value_col="quantidade_ativos", selection=filtros["class_sel"]
        )
        show_values = filtros["show_values"]
    """
    with st.sidebar:
        st.header("Filtros")
        periodo = _widget_periodo_ano(df)
        class_sel = _widget_class_selector_with_geral(df)
        show_values = _widget_show_values()

    return {
        "periodo": periodo,
        "classes": class_sel["selected"],
        "class_sel": class_sel,
        "show_values": show_values,
    }


# ── API pública ───────────────────────────────────────────────────────────────
# Apenas render_sidebar_filters deve ser importado pelas páginas.
# Os demais símbolos abaixo existem para uso em testes unitários.

__all__ = ["render_sidebar_filters"]
