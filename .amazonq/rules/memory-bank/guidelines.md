# Development Guidelines

## Code Quality Standards

### Module-level docstrings
Every file starts with a triple-quoted docstring describing its purpose and responsibility:
```python
"""Figuras Plotly para a página de Inclusões em Pauta."""
"""Camada de dados: lógica pura de filtragem (sem Streamlit).

Fonte da verdade para todas as funções de filtragem do projeto.
Não importa Streamlit. Funções sempre retornam .copy().
"""
```

### Future annotations
All files use `from __future__ import annotations` as the first import, enabling PEP 604 union types (`X | Y`) on Python 3.10+.

### Explicit `__all__`
Public API modules declare `__all__` to restrict what pages can import:
```python
__all__ = ["render_sidebar_filters"]
__all__ = ["filter_by_date_range", "filter_by_values", ...]
```

### Defensive returns
Filter functions always return a copy and handle edge cases gracefully:
```python
if not values or column not in df.columns:
    return df          # passthrough, never raises
return df[df[column].isin(values)].copy()  # always .copy()
```

### Type annotations
All public functions are fully annotated with return types:
```python
def filter_by_values(df: pd.DataFrame, column: str, values: list | set | None) -> pd.DataFrame:
def load_parquet(repo_id: str, filename: str) -> pd.DataFrame:
def render_sidebar_filters(df: pd.DataFrame) -> dict[str, Any]:
```

---

## Structural Conventions

### Strict layer separation (enforced)
| File | `st.*` | Plotly | Filter data |
|------|--------|--------|-------------|
| `data/filters.py` | ❌ | ❌ | ✅ |
| `data/loader.py` | Only `@st.cache_data` | ❌ | ❌ |
| `components/filters.py` | ✅ | ❌ | ❌ |
| `pages/*/plots.py` | ❌ | ✅ | ❌ |
| `pages/*/layout.py` | ✅ | Receive only | ❌ |
| `pages/*/<page>.py` | Config only | ❌ | Orchestration only |

### Page orchestrator pattern (3 steps only)
```python
df = load_...()                          # 1. Load
filtros = render_sidebar_filters(df)
df_filtrado = apply_filters(df, filtros) # 2. Filter
render_graficos(df_filtrado, ...)        # 3. Render
```

### Private helpers with underscore prefix
Internal helpers are prefixed with `_` and never exported:
```python
def _bar_fig(barmode: str = "group") -> go.Figure: ...
def _pizza(series, titulo, ...) -> go.Figure: ...
def _safe_unique_sorted(df, col) -> list: ...
def _get_hf_token() -> str | None: ...
```

### Section separators with visual hierarchy
Code sections are separated with ASCII box-drawing comments:
```python
# ── helpers ───────────────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICOS 5–17  (bloco INCLUSÕES EM PAUTA)
# ═══════════════════════════════════════════════════════════════════════════════
# ── Ponto de entrada único ────────────────────────────────────────────────────
```

---

## Naming Conventions

### Color palette constants (module-level dicts)
Color maps are defined as module-level dicts with ALL_CAPS names:
```python
CORES_CLASSE = {"ADI": "#2563eb", "ADPF": "#f59e0b", "ADC": "#16a34a", "ADO": "#ef4444"}
CORES_MACRO  = {"Concluído": "#16a34a", "Não concluído": "#ef4444"}
COR_PV = "#2563eb"
COR_PP = "#94a3b8"
```

### Plot function naming
Public plot functions follow `g<number>_<description>_<scope>` pattern:
```python
def g5_anual_ambiente(df): ...
def g6_pv_por_classe(df): ...
def g10_macro_anual_pv(df): ...
```

### Private prep functions
Data transformation helpers before plotting use `_prep_<name>`:
```python
def _prep_tipo(df): ...   # normalizes tipo_questao values
def _prep_cat(df): ...    # adds categoria column
def _prep_nc(df): ...     # filters non-concluded + adds categoria_nc
```

### Shared layout constants
Reusable Plotly layout dicts are module-level private constants:
```python
_LEGEND = dict(orientation="h", yanchor="bottom", y=1.02, ...)
_LAYOUT = dict(template="plotly_white", height=500, margin=dict(...), ...)
```

---

## Plotly Patterns

### Standard bar figure factory
```python
def _bar_fig(barmode: str = "group") -> go.Figure:
    fig = go.Figure()
    fig.update_layout(**_LAYOUT, barmode=barmode)
    return fig
```

### Dual-axis figure (bar + line)
```python
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(...), secondary_y=False)
fig.add_trace(go.Scatter(..., mode="lines+markers"), secondary_y=True)
```

### Pie/donut chart
```python
go.Pie(labels=series.index, values=series.values, hole=0.4,
       textinfo="label+percent+value", textposition="outside",
       marker=dict(colors=cores, line=dict(color="white", width=2)))
```

### Bar trace with value labels
```python
go.Bar(x=d[col_x], y=d["n"], name=g,
       marker_color=cores[g],
       text=d["n"], textposition="outside", cliponaxis=False)
```

### Conditional show_values
```python
text=df_total[coluna_metrica] if show_values else None,
textposition="outside",
cliponaxis=False,
```

### Fake traces for legend entries
When shapes/vrects need legend entries, add invisible scatter traces:
```python
fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines",
                         line=dict(color=color, dash="dash"), name=label))
```

### Standard layout update
```python
fig.update_layout(
    title_text="...",
    template="plotly_white",
    height=500,
    margin=dict(t=120, b=80, l=60, r=60),
    legend=_LEGEND,
    xaxis=dict(dtick=1, title="Ano", tickangle=-45),
)
```

---

## Data Layer Patterns

### Loader: local-first, HF fallback
```python
local = _try_local_parquet(filename)
if local is not None:
    return local
# ... then try HF with multiple candidate paths
```

### Cache only at load_parquet level
`@st.cache_data(ttl=3600)` is applied only to `load_parquet`. Specific loaders are plain wrappers:
```python
def load_inclusoes_em_pauta() -> pd.DataFrame:
    """Carrega o dataset de inclusões em pauta (2020–2025)."""
    return load_parquet(HF_REPO_ID, HF_FILES["inclusoes_em_pauta"])
```

### Filter functions always return `.copy()`
Every filter function returns `df[mask].copy()` to prevent downstream mutation.

### Sidebar filter return contract
`render_sidebar_filters(df)` always returns this exact shape:
```python
{
    "periodo":     (ano_inicio, ano_fim),   # tuple[int, int]
    "classes":     ["ADI", "ADC", ...],     # list[str]
    "class_sel":   {"selected": [...], "use_geral": bool},
    "show_values": bool,
}
```

---

## What NOT to Do

- Never import `streamlit` in `data/filters.py` or `pages/*/plots.py`
- Never build Plotly figures inside `layout.py` or `<page>.py`
- Never filter data inside `components/filters.py`
- Never hardcode colors, column names, or year ranges outside `config.py` or the module-level color dicts in `plots.py`
- Never add `@st.cache_data` to specific loader functions — cache lives in `load_parquet` only
- Never create `ImportError` fallbacks inline in pages — missing components must be created properly
- Never skip `.copy()` on filtered DataFrames returned from `data/filters.py`
