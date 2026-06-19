# Estrutura do Projeto

> Este documento descreve a organização do projeto, a responsabilidade de cada camada e as regras que devem ser seguidas ao adicionar novas funcionalidades. Serve como referência para qualquer pessoa ou modelo que precise trabalhar no código.

---

## Árvore de Arquivos

```
app/
├── components/
│   ├── __init__.py
│   └── filters.py          # Widgets reutilizáveis do sidebar (UI apenas)
│
├── data/
│   ├── __init__.py
│   ├── filters.py          # Lógica pura de filtragem (sem Streamlit)
│   └── loader.py           # Carregamento e cache dos datasets
│
├── pages/
│   ├── __init__.py
│   ├── acervo/             # Página: Acervo Histórico
│   │   ├── acervo.py       # Orquestrador da página
│   │   ├── plots.py        # Constrói figuras Plotly (sem Streamlit)
│   │   └── layout.py       # Renderiza figuras e textos com st.*
│   │
│   └── visal_geral/        # Página: Visão Geral (mesma estrutura)
│
├── app.py                  # Entrada da aplicação
├── config.py               # Constantes e configurações globais
└── requirements.txt
```

---

## Responsabilidade de Cada Camada

### `app.py`

Ponto de entrada da aplicação. Define navegação entre páginas e configurações globais que se aplicam a toda a aplicação. Não contém lógica de dados nem construção de gráficos.

---

### `config.py`

Constantes globais do projeto: nomes de colunas padrão, paletas de cores, intervalos de ano, URLs de datasets, chaves de secrets. Qualquer valor que apareça em mais de um arquivo deve vir daqui.

```python
# Exemplo do que pertence aqui
ANO_MIN = 1988
ANO_MAX = 2025
CLASSES = ["ADI", "ADC", "ADO", "ADPF"]
COLUNA_ANO = "ano"
COLUNA_QUANTIDADE = "quantidade_ativos"
COLUNA_CLASSE = "classe"
```

---

### `data/loader.py`

Responsável por carregar os datasets e aplicar cache. Não filtra, não agrega, não renderiza. Retorna sempre um dataframe bruto.

```python
# Padrão esperado
@st.cache_data
def load_evolucao_acervo() -> pd.DataFrame:
    ...
```

---

### `data/filters.py`

Lógica pura de filtragem. Não importa Streamlit. Recebe dataframes e parâmetros, devolve dataframes. Pode ser usada em notebooks e testes sem nenhuma dependência de UI.

Funções disponíveis:

- `filter_by_values(df, column, values)` — filtra por lista de valores
- `filter_by_date_range(df, date_col, start, end)` — filtra por intervalo de datas
- `filter_by_text_search(df, columns, query)` — busca textual em múltiplas colunas

---

### `components/filters.py`

Renderiza widgets no sidebar e retorna os valores selecionados. Não filtra dados, não acessa arquivos. A função principal é `render_sidebar_filters(df)`, que retorna um dicionário com todos os valores dos filtros ativos.

```python
# O que retorna
{
    "periodo": (2000, 2025),
    "classes": ["ADI", "ADPF"],
}
```

Funções adicionais disponíveis:

- `class_selector_with_geral(df)` — seletor de classe com opção de visão agregada
- `show_values_toggle()` — toggle global para exibir valores nos gráficos
- `prepare_class_or_geral(df, value_col, class_col, selection)` — agrega ou não conforme seleção

---

### `pages/<nome_pagina>/`

Cada página é uma pasta com três arquivos:

#### `plots.py`

Constrói e retorna objetos `go.Figure` do Plotly. Não importa Streamlit. Recebe um dataframe já filtrado e parâmetros de exibição, devolve a figura pronta.

```python
# Assinatura padrão
def fig_nome_do_grafico(df: pd.DataFrame, **opcoes) -> go.Figure:
    ...
    return fig
```

#### `layout.py`

Renderiza a página usando `st.*`. Importa as funções de `plots.py` e chama `st.plotly_chart`. Contém também subheaders, captions, expanders e textos analíticos. Não contém lógica de filtragem nem construção de figuras.

```python
# Assinatura padrão
def render_graficos(df: pd.DataFrame, show_values: bool) -> None:
    ...
```

#### `<nome_pagina>.py`

Orquestrador da página. Faz exatamente três coisas: carrega os dados, aplica os filtros e chama o layout. Não constrói gráficos, não renderiza widgets avulsos, não contém lógica de negócio.

```python
# Estrutura padrão de uma página
df = load_...()           # 1. Carrega
filtros = render_sidebar_filters(df)
df_filtrado = ...         # 2. Filtra
render_graficos(df_filtrado, ...)  # 3. Renderiza
```

---

## Fluxo de Dados

```
loader.py
    │
    ▼
<pagina>.py  ──► data/filters.py ──► df filtrado
    │
    ▼
layout.py  ──► plots.py ──► go.Figure
    │
    ▼
st.plotly_chart(fig)
```

Os dados sempre fluem para baixo. Nenhuma camada inferior conhece a camada superior.

---

## Como Adicionar uma Nova Página

1. Criar a pasta `pages/<nome>/`
2. Criar `plots.py` com as funções de figura
3. Criar `layout.py` com `render_graficos(df, ...)`
4. Criar `<nome>.py` seguindo o padrão de orquestração
5. Registrar a página em `app.py`

Nenhum outro arquivo precisa ser alterado.

---

## Como Adicionar um Novo Filtro

1. Criar o widget em `components/filters.py`
2. Adicionar o valor retornado ao dicionário de `render_sidebar_filters`
3. Aplicar o filtro na página usando as funções de `data/filters.py`

Nenhum outro arquivo precisa ser alterado.

---

## Como Adicionar um Novo Gráfico a uma Página Existente

1. Criar a função `fig_novo_grafico(df, ...)` em `plots.py`
2. Chamar a função e renderizar em `layout.py`

O arquivo de orquestração (`<pagina>.py`) não precisa ser alterado.

---

## Regras Fundamentais

| Arquivo                 | Pode usar `st.*`   | Pode usar Plotly       | Pode filtrar dados |
| ----------------------- | ------------------ | ---------------------- | ------------------ |
| `data/filters.py`       | Não                | Não                    | Sim                |
| `data/loader.py`        | Só `st.cache_data` | Não                    | Não                |
| `components/filters.py` | Sim                | Não                    | Não                |
| `plots.py`              | Não                | Sim                    | Não                |
| `layout.py`             | Sim                | Só para receber figura | Não                |
| `<pagina>.py`           | Só configuração    | Não                    | Só orquestração    |

---

## O Que Não Fazer

- Não construir figuras Plotly dentro de `<pagina>.py` ou `layout.py`
- Não importar `streamlit` em `data/filters.py` ou `plots.py`
- Não filtrar dados dentro de `components/filters.py`
- Não colocar constantes fixas (anos, nomes de colunas, cores) espalhadas nos arquivos — use `config.py`
- Não criar fallbacks de `ImportError` nas páginas — se um componente não existe, ele deve ser criado, não simulado inline
