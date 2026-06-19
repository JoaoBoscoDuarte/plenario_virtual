# Arquitetura de Filtros — `components/filters.py`

## Visão Geral

Este documento descreve a arquitetura de filtros adotada no projeto, a separação de responsabilidades entre os módulos envolvidos e as decisões de design pensadas para escalabilidade e manutenibilidade.

---

## Estrutura de Arquivos

```
app/
├── components/
│   └── filters.py        # Renderização dos widgets no sidebar (UI)
├── data/
│   └── filters.py        # Lógica pura de filtragem (sem Streamlit)
└── pages/
    └── acervo.py         # Página: orquestra UI + dados
```

A separação em dois arquivos distintos é intencional e reflete um princípio central: **UI e lógica de dados não devem se misturar**.

---

## Responsabilidades

### `components/filters.py` — Camada de UI

Responsável exclusivamente por renderizar widgets no sidebar e retornar os valores selecionados pelo usuário. Não filtra dados, não acessa arquivos, não conhece a estrutura interna do dataframe além das colunas que precisa listar.

```python
# components/filters.py

from __future__ import annotations
from typing import Any
import streamlit as st
import pandas as pd


def filtro_periodo_ano(df: pd.DataFrame, col: str = "ano") -> tuple[int, int]:
    """Slider de intervalo de anos. Retorna (ano_inicio, ano_fim)."""
    ano_min, ano_max = int(df[col].min()), int(df[col].max())
    return st.sidebar.slider(
        "Período (ano)",
        min_value=ano_min,
        max_value=ano_max,
        value=(ano_min, ano_max),
        step=1,
    )


def filtro_classe(df: pd.DataFrame, col: str = "classe") -> list[str]:
    """Multiselect de classes processuais. Retorna lista de classes selecionadas."""
    opcoes = sorted(df[col].unique().tolist())
    return st.sidebar.multiselect(
        "Classe processual",
        options=opcoes,
        default=opcoes,
    )


def render_sidebar_filters(df: pd.DataFrame) -> dict[str, Any]:
    """Ponto de entrada principal. Renderiza todos os filtros e retorna os valores."""
    with st.sidebar:
        st.header("Filtros")
        periodo = filtro_periodo_ano(df)
        classes = filtro_classe(df)

    return {
        "periodo": periodo,   # (ano_inicio, ano_fim)
        "classes": classes,   # ["ADI", "ADC", ...]
    }
```

### `data/filters.py` — Camada de Dados

Responsável exclusivamente pela lógica de filtragem. Não importa Streamlit, não renderiza nada, não sabe que existe uma interface. Pode ser usada em notebooks, testes e scripts sem nenhuma dependência de UI.

```python
# data/filters.py

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
```

### `pages/acervo.py` — Camada de Orquestração

A página não contém lógica de filtragem nem widgets avulsos — ela apenas conecta as duas camadas.

```python
# pages/acervo.py (trecho relevante)

from components.filters import render_sidebar_filters
from data.filters import filter_by_values

# Após carregar o df...
filtros = render_sidebar_filters(df)

ano_inicio, ano_fim = filtros["periodo"]
df_filtrado = filter_by_values(df, "classe", filtros["classes"])
df_filtrado = df_filtrado[df_filtrado["ano"].between(ano_inicio, ano_fim)]
```

---

## Por Que Essa Separação?

### Testabilidade

A lógica em `data/filters.py` pode ser testada diretamente com `pytest`, sem precisar subir uma interface Streamlit:

```python
# tests/test_filters.py

import pandas as pd
from data.filters import filter_by_values, filter_by_date_range

def test_filter_by_values_remove_classe():
    df = pd.DataFrame({"classe": ["ADI", "ADC", "ADPF"]})
    resultado = filter_by_values(df, "classe", ["ADI", "ADPF"])
    assert list(resultado["classe"]) == ["ADI", "ADPF"]

def test_filter_by_values_coluna_inexistente():
    df = pd.DataFrame({"classe": ["ADI"]})
    resultado = filter_by_values(df, "coluna_que_nao_existe", ["ADI"])
    assert len(resultado) == 1  # retorna df intacto
```

### Reuso

As funções de `data/filters.py` funcionam em qualquer contexto Python — notebooks de análise, scripts de pré-processamento, outras páginas do dashboard — sem nenhuma dependência de Streamlit.

### Manutenção

Se o widget de seleção de classe mudar (virar um `radio`, por exemplo), a alteração fica isolada em `components/filters.py`. A lógica de filtragem em `data/filters.py` não precisa ser tocada.

---

## Adicionando um Novo Filtro

O processo é sempre o mesmo, em três passos:

**1. Criar o widget em `components/filters.py`:**

```python
def filtro_relator(df: pd.DataFrame, col: str = "relator") -> list[str]:
    opcoes = sorted(df[col].dropna().unique().tolist())
    return st.sidebar.multiselect("Relator", options=opcoes, default=opcoes)
```

**2. Registrar no `render_sidebar_filters`:**

```python
def render_sidebar_filters(df: pd.DataFrame) -> dict[str, Any]:
    with st.sidebar:
        st.header("Filtros")
        periodo  = filtro_periodo_ano(df)
        classes  = filtro_classe(df)
        relatores = filtro_relator(df)      # novo

    return {
        "periodo":   periodo,
        "classes":   classes,
        "relatores": relatores,             # novo
    }
```

**3. Aplicar na página:**

```python
df_filtrado = filter_by_values(df_filtrado, "relator", filtros["relatores"])
```

Nenhuma outra parte do código precisa ser alterada.

---

## Convenções

| Convenção | Motivo |
|---|---|
| Widgets sempre no `st.sidebar` | Consistência visual entre páginas |
| Funções de widget recebem `df` e `col` | Reusáveis em qualquer coluna, sem hardcode |
| `render_sidebar_filters` retorna `dict` | Fácil de estender sem quebrar assinaturas |
| `data/filters.py` sem imports de Streamlit | Garantia de que a lógica é portável |
| Funções de filtro retornam `.copy()` | Evita mutações inesperadas no df original |

---

## Quando Não Usar Este Padrão

- **Filtros muito simples e de uso único** — se uma página tem um único widget que nunca será reaproveitado, criar o componente pode ser overhead desnecessário.
- **Filtros com estado complexo entre si** — se dois filtros precisam se comunicar (ex: selecionar um relator filtra dinamicamente as classes disponíveis), a lógica de dependência deve ficar na página, não nos componentes individuais.

---

## Referências Internas

- `components/filters.py` — implementação dos widgets
- `data/filters.py` — implementação da lógica de filtragem
- `pages/acervo.py` — exemplo de uso completo
