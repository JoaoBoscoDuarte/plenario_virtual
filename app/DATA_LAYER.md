# Camada de Dados — Data Layer

> Este documento descreve como os dados fluem no dashboard: de onde vêm, como são carregados, como são filtrados e o que fazer em cada situação. Serve como referência para qualquer pessoa ou modelo que precise adicionar, modificar ou depurar dados no projeto.

---

## Visão Geral

O dashboard consome dados armazenados no **Hugging Face Datasets**, uma plataforma de hospedagem de datasets compatível com acesso via API. Em desenvolvimento local, os mesmos arquivos podem ser lidos diretamente do disco, sem nenhuma alteração no código.

Todo o acesso a dados passa por dois módulos:

```
data/
├── loader.py     # Carrega os dados (Hugging Face ou local)
└── filters.py    # Filtra e transforma os dados
```

Nenhuma página ou componente acessa dados diretamente — sempre via esses dois módulos.

---

## Onde os Dados Vivem

### Produção — Hugging Face

Os datasets ficam em um repositório do tipo **Dataset** no Hugging Face:

```
Repositório: JoaoBoscoooo/plenario_virtual  (configurável via HF_REPO)
Tipo:        dataset
Estrutura:   processed/
               acervo/
                 evolucao_acervo.parquet
               <outros datasets aqui>
```

O acesso é feito via `hf_hub_download`, que baixa o arquivo e o coloca em cache local automaticamente. Em repositórios privados, é necessário um token de autenticação (ver seção de configuração).

### Desenvolvimento Local

Durante o desenvolvimento, o `loader.py` procura o arquivo localmente antes de tentar o Hugging Face. Os caminhos buscados são:

```
data/processed/<nome_do_arquivo>
data/processed/acervo/<nome_do_arquivo>
../data/processed/<nome_do_arquivo>
../data/processed/acervo/<nome_do_arquivo>
```

Se o arquivo for encontrado em qualquer um desses caminhos, o download é ignorado. Isso significa que **em desenvolvimento, nenhuma configuração de token é necessária** desde que o arquivo exista localmente.

---

## Configuração

### Variáveis de Ambiente

| Variável   | Descrição                                     | Padrão                          |
| ---------- | --------------------------------------------- | ------------------------------- |
| `HF_REPO`  | ID do repositório no Hugging Face             | `JoaoBoscoooo/plenario_virtual` |
| `HF_TOKEN` | Token de autenticação (repositórios privados) | —                               |

### Streamlit Cloud

No Streamlit Cloud, as variáveis são configuradas em **Settings → Secrets**:

```toml
HF_TOKEN = "hf_..."
HF_REPO  = "JoaoBoscoooo/plenario_virtual"   # opcional se usar o padrão
```

O `loader.py` lê o token automaticamente tanto de variável de ambiente quanto de `st.secrets`, sem nenhuma configuração adicional no código.

---

## Como o Loader Funciona

### `load_parquet(repo_id, filename)`

Função base que centraliza todo o acesso a dados. O fluxo interno é:

```
1. Busca o arquivo localmente (data/processed/...)
      ↓ encontrou → retorna imediatamente
      ↓ não encontrou
2. Obtém o token (env → st.secrets → None)
3. Tenta baixar do Hugging Face com o caminho exato
      ↓ falhou
4. Tenta variações do caminho (basename, processed/basename)
      ↓ falhou em todos
5. Lança RuntimeError com detalhes de todas as tentativas
```

O resultado é cacheado por 1 hora via `@st.cache_data(ttl=3600)`. Chamadas subsequentes com os mesmos argumentos retornam o cache sem novo download.

### Funções específicas de loader

Cada dataset tem sua própria função wrapper, sem lógica adicional:

```python
def load_evolucao_acervo() -> pd.DataFrame:
    return load_parquet(HF_REPO_ID, HF_FILES["evolucao_acervo"])
```

Essas funções **não carregam `@st.cache_data`** — o cache já está em `load_parquet`.

---

## Adicionando um Novo Dataset

### 1. Registrar o caminho em `config.py`

```python
HF_FILES = {
    "evolucao_acervo": "processed/acervo/evolucao_acervo.parquet",
    "novo_dataset":    "processed/<subpasta>/<arquivo>.parquet",  # novo
}
```

### 2. Criar a função loader em `data/loader.py`

```python
def load_novo_dataset() -> pd.DataFrame:
    """Descrição do que esse dataset contém."""
    return load_parquet(HF_REPO_ID, HF_FILES["novo_dataset"])
```

### 3. Usar na página

```python
from data.loader import load_novo_dataset

df = load_novo_dataset()
```

Nenhum outro arquivo precisa ser alterado.

---

## Como os Filtros Funcionam

### `data/filters.py`

Contém toda a lógica de filtragem. Não importa Streamlit. Pode ser usada em notebooks e testes sem dependência de UI.

Funções disponíveis:

**`filter_by_values(df, column, values)`**
Mantém apenas as linhas cujo valor da coluna está na lista `values`. Se `values` for vazio ou `None`, retorna o dataframe intacto.

```python
df_filtrado = filter_by_values(df, "classe", ["ADI", "ADPF"])
```

**`filter_by_date_range(df, date_col, start, end)`**
Filtra por intervalo de datas (inclusive em ambas as extremidades).

```python
df_filtrado = filter_by_date_range(df, "data_protocolo", "1988-01-01", "2025-12-31")
```

**`filter_by_text_search(df, columns, query)`**
Busca case-insensitive em uma ou mais colunas de texto.

```python
df_filtrado = filter_by_text_search(df, ["relator", "assunto"], "meio ambiente")
```

**`filter_by_year_range(df, year, start, end, year_col, date_col)`**
Filtra por ano exato ou intervalo. Aceita coluna de ano inteiro ou deriva o ano de uma coluna de data.

```python
df_filtrado = filter_by_year_range(df, start=2000, end=2025)
```

**`prepare_class_or_geral(df, value_col, class_col, selection)`**
Prepara o dataframe para plotagem conforme a seleção de classe ou visão agregada (Geral). Recebe o dicionário `class_sel` retornado por `render_sidebar_filters`.

```python
df_plot = prepare_class_or_geral(
    df,
    value_col="quantidade_ativos",
    selection=filtros["class_sel"],
)
```

---

## Fluxo Completo em uma Página

```python
from data.loader import load_evolucao_acervo
from data.filters import filter_by_values, filter_by_year_range, prepare_class_or_geral
from components.filters import render_sidebar_filters

# 1. Carrega (cacheado automaticamente)
df = load_evolucao_acervo()

# 2. Renderiza filtros e coleta seleções
filtros = render_sidebar_filters(df)

# 3. Aplica filtros
ai, af = filtros["periodo"]
df_filtrado = filter_by_values(df, "classe", filtros["classes"])
df_filtrado = filter_by_year_range(df_filtrado, start=ai, end=af)
df_filtrado = prepare_class_or_geral(
    df_filtrado,
    value_col="quantidade_ativos",
    selection=filtros["class_sel"],
)

# 4. Passa para o layout
render_graficos(df_filtrado, show_values=filtros["show_values"])
```

---

## Cache

O cache é gerenciado pelo Streamlit via `@st.cache_data`. O comportamento padrão:

- **TTL:** 1 hora — após esse tempo, o dado é baixado novamente do Hugging Face
- **Chave:** baseada nos argumentos da função (`repo_id` + `filename`)
- **Invalidação manual:** Menu do Streamlit → "Clear cache", ou reiniciar a aplicação

Em desenvolvimento local o cache também é aplicado, mas como os arquivos são lidos do disco, o impacto é mínimo.

---

## Diagnóstico de Erros Comuns

**`RuntimeError: Não foi possível baixar '...'`**
O arquivo não existe localmente e o download falhou. Verifique:

- O caminho em `HF_FILES` está correto
- O repositório existe e o arquivo foi publicado
- O token está configurado se o repositório for privado

**`KeyError` ou `st.stop()` na página**
A validação defensiva da página detectou que o dataframe não tem as colunas esperadas. Verifique se o arquivo parquet no Hugging Face foi gerado com o schema correto.

**Dados desatualizados no dashboard**
O cache ainda está servindo dados antigos. Limpe o cache manualmente ou aguarde o TTL de 1 hora expirar.

**Token não reconhecido no Streamlit Cloud**
Verifique se o secret está sob a chave exata `HF_TOKEN` (maiúsculas) em Settings → Secrets, sem espaços extras.
