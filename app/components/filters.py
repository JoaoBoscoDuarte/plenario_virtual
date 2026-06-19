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


# ------------------------------------------------------------------
# Novos componentes globais exigidos para a lista de gráficos
# (regras de toggle de valores, classe + Geral, etc.)
# ------------------------------------------------------------------

def show_values_toggle() -> bool:
    """Checkbox global 'Exibir valores nos gráficos'.

    Default = False (sem poluição visual).
    Retorna True quando o usuário quer ver os rótulos numéricos.
    """
    return st.sidebar.checkbox(
        "Exibir valores nos gráficos",
        value=False,
        help="Quando marcado, mostra os valores totais sobre barras/pontos nos gráficos (respeitando os filtros aplicados)."
    )


def class_selector_with_geral(df: pd.DataFrame, col: str = "classe") -> dict[str, Any]:
    """Seletor de classe com suporte explícito a 'Geral (todas as classes)'.

    Retorna:
      {
        "selected": list[str] | None,   # None ou lista de classes específicas
        "use_geral": bool               # True quando deve agregar tudo
      }

    Comportamento:
    - Se o usuário marcar "Geral (todas as classes)", use_geral=True e selected pode ser ignorado (soma).
    - Caso contrário, usa as classes selecionadas no multiselect.
    """
    opcoes = [str(x) for x in _safe_unique_sorted(df, col)]
    if not opcoes:
        return {"selected": [], "use_geral": False}

    use_geral = st.sidebar.checkbox(
        "Geral (todas as classes)",
        value=False,
        help="Quando marcado, o gráfico mostra apenas a série agregada (soma de todas as classes)."
    )

    if use_geral:
        # Quando Geral está marcado, o multiselect fica desabilitado visualmente (mas ainda mostramos para referência)
        st.sidebar.multiselect(
            "Classe processual (ignorada no modo Geral)",
            options=opcoes,
            default=opcoes,
            disabled=True
        )
        return {"selected": opcoes, "use_geral": True}

    selected = st.sidebar.multiselect(
        "Classe processual",
        options=opcoes,
        default=opcoes
    )
    return {"selected": selected, "use_geral": False}


def prepare_class_or_geral(
    df: pd.DataFrame,
    value_col: str,
    class_col: str = "classe",
    selection: dict[str, Any] | None = None
) -> pd.DataFrame:
    """Prepara o DataFrame para plot conforme seleção de classe/Geral.

    - Se use_geral=True: agrupa por ano (ou outra chave temporal) somando value_col e cria coluna "classe" = "Geral".
    - Caso contrário: filtra para as classes selecionadas.

    Retorna cópia do df pronto para uso no gráfico.
    """
    if df is None or df.empty:
        return df

    work = df.copy()

    if selection is None:
        return work

    use_geral = selection.get("use_geral", False)
    selected = selection.get("selected", [])

    if use_geral:
        # Agregar tudo (mantendo colunas de ano/outros se existirem)
        group_keys = [c for c in work.columns if c != class_col and c != value_col]
        if not group_keys:
            # fallback: tentar encontrar coluna de ano
            for c in ["ano", "year"]:
                if c in work.columns:
                    group_keys = [c]
                    break
        if group_keys:
            agg = work.groupby(group_keys, as_index=False)[value_col].sum()
            agg[class_col] = "Geral"
            return agg
        else:
            # último recurso
            total = work[value_col].sum()
            return pd.DataFrame({class_col: ["Geral"], value_col: [total]})

    if selected:
        work = work[work[class_col].astype(str).isin([str(s) for s in selected])]

    return work
