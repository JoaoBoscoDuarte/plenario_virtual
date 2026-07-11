# Gráficos de Desfecho — Inclusões em Pauta STF (2020–2025)

Coleção de gráficos para análise de inclusões em pauta no controle concentrado
de constitucionalidade (ADI, ADPF, ADC, ADO) do STF.

## Contexto e dependências

Todos os gráficos operam sobre o DataFrame `df_final`, que contém uma linha por
inclusão em pauta, com as seguintes colunas relevantes:

- `ano` — ano da inclusão (2020–2025)
- `ambiente` — `"Plenário Virtual"` ou `"Plenário Físico"`
- `classe` — `ADI`, `ADPF`, `ADC`, `ADO`
- `tipo_questao` — `PR`, `RC`, `IJ` (renomeado para `QI` na exibição)
- `desfecho` — desfecho detalhado da inclusão
- `macro_desfecho` — `"Concluído"` ou `"Não concluído"`

Valores possíveis de `desfecho`:
- `Concluído - decisão unânime`
- `Concluído - decisão maioria com o relator`
- `Concluído - decisão maioria, vencido o relator`
- `Não concluído - pedido de vista`
- `Não concluído - destaque`
- `Não concluído - retirado de pauta`
- `Não concluído - motivos diversos`

## Função de plotagem (pré-existente)

```python
def plotar_barras_stf(df_dados, col_x, col_y, col_grupo=None,
                      titulo='', label_y='Inclusões em pauta',
                      mostrar_linha_total=False, df_total=None,
                      cores=None):
    """
    Função base de plotagem padronizada (barras empilhadas Plotly).

    Parâmetros:
      df_dados            : DataFrame já agrupado (colunas col_x, col_grupo, col_y)
      col_x               : coluna do eixo X (ex: 'ano' ou 'tipo_questao')
      col_y               : coluna de valores (ex: 'n')
      col_grupo           : coluna de agrupamento para barras empilhadas
      titulo              : título do gráfico
      label_y             : rótulo do eixo Y
      mostrar_linha_total : se True, adiciona linha cinza com total geral
      df_total            : DataFrame com totais para a linha (colunas: col_x, col_y='n')
      cores               : dict {grupo: cor} ou None
    """
```

Observação importante sobre exibição: quando a última expressão de uma célula é
uma chamada a `plotar_barras_stf`, prefixe com `_ =` para suprimir o auto-display
do Jupyter e evitar gráfico duplicado.

## Convenções de renomeação e cores

```python
# Renomeação de tipo de questão para exibição
# IJ (Questão Incidental) → QI
df['tipo_questao'] = df['tipo_questao'].replace({'IJ': 'QI'})

# Cores por tipo de questão
CORES_TIPO = {
    'PR': '#2563eb',   # azul
    'RC': '#f59e0b',   # laranja
    'QI': '#16a34a',   # verde
}

# Cores por categoria de desfecho CONCLUÍDO (+ bloco não concluído)
CORES_CATEGORIA = {
    '1 - Unânime':                    '#16a34a',  # verde
    '2 - Maioria (relator vencedor)': '#2563eb',  # azul
    '3 - Maioria (relator vencido)':  '#f59e0b',  # laranja
    '4 - Não concluído (bloco)':      '#9ca3af',  # cinza
}

# Cores por categoria de desfecho NÃO CONCLUÍDO
CORES_NC = {
    '1 - Pedido de vista':    '#8b5cf6',  # roxo
    '2 - Destaque':           '#ec4899',  # rosa
    '3 - Retirado de pauta':  '#f59e0b',  # laranja
    '4 - Motivos diversos':   '#9ca3af',  # cinza
}
```

## Funções de mapeamento de categorias

```python
# Categoria de desfecho concluído (3 tipos de conclusão + bloco não concluído)
def categoria_desfecho(d):
    if d == 'Concluído - decisão unânime':
        return '1 - Unânime'
    if d == 'Concluído - decisão maioria com o relator':
        return '2 - Maioria (relator vencedor)'
    if d == 'Concluído - decisão maioria, vencido o relator':
        return '3 - Maioria (relator vencido)'
    return '4 - Não concluído (bloco)'

# Categoria de desfecho não concluído (4 categorias)
def categoria_nao_concluido(d):
    if d == 'Não concluído - pedido de vista':
        return '1 - Pedido de vista'
    if d == 'Não concluído - destaque':
        return '2 - Destaque'
    if d == 'Não concluído - retirado de pauta':
        return '3 - Retirado de pauta'
    return '4 - Motivos diversos'
```

---

# GRUPO 1 — Tipo de questão, por ano

## 1.1 — Não concluídos por tipo de questão (PV e PP)

Inclusões **não concluídas**, quebradas por tipo de questão (PR/RC/QI), anual.

```python
df_nc = df_final[df_final['macro_desfecho'] == 'Não concluído'].copy()
df_nc['tipo_questao'] = df_nc['tipo_questao'].replace({'IJ': 'QI'})

for ambiente, sigla in [('Plenário Virtual', 'Virtual'), ('Plenário Físico', 'Físico')]:
    sub = df_nc[df_nc['ambiente'] == ambiente]
    tab = sub.groupby(['ano', 'tipo_questao']).size().reset_index(name='n')
    total = sub.groupby('ano').size().reset_index(name='n')

    _ = plotar_barras_stf(
        df_dados=tab, col_x='ano', col_y='n', col_grupo='tipo_questao',
        titulo=f'Inclusões não concluídas por tipo de questão — {ambiente} (2020–2025)',
        label_y='Inclusões em pauta',
        mostrar_linha_total=True, df_total=total, cores=CORES_TIPO,
    )
```

## 1.2 — Concluídos por tipo de questão (PV e PP)

Inclusões **concluídas**, quebradas por tipo de questão (PR/RC/QI), anual.

```python
df_c = df_final[df_final['macro_desfecho'] == 'Concluído'].copy()
df_c['tipo_questao'] = df_c['tipo_questao'].replace({'IJ': 'QI'})

for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    sub = df_c[df_c['ambiente'] == ambiente]
    tab = sub.groupby(['ano', 'tipo_questao']).size().reset_index(name='n')
    total = sub.groupby('ano').size().reset_index(name='n')

    _ = plotar_barras_stf(
        df_dados=tab, col_x='ano', col_y='n', col_grupo='tipo_questao',
        titulo=f'Inclusões concluídas por tipo de questão — {ambiente} (2020–2025)',
        label_y='Inclusões em pauta',
        mostrar_linha_total=True, df_total=total, cores=CORES_TIPO,
    )
```

---

# GRUPO 2 — Desfecho concluído por categoria

As 3 categorias de conclusão (unânime, maioria vencedor, maioria vencido) mais
o bloco agregado de não concluído.

## 2.1 — Por categoria, período agregado (PV e PP) — PIZZA

Distribuição das 4 categorias no período inteiro (sem eixo temporal).

```python
df_cat = df_final.copy()
df_cat['categoria'] = df_cat['desfecho'].apply(categoria_desfecho)

for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    serie = (df_cat[df_cat['ambiente'] == ambiente]['categoria']
             .value_counts().sort_index())
    _ = plotar_pizza_stf(
        serie,
        titulo=f'Desfecho por categoria — {ambiente} (2020–2025, período total)',
    )
```

Observação: usa `plotar_pizza_stf(series, titulo, buraco)`, função pré-existente.

## 2.2 — Por categoria, por ano (PV e PP) — BARRAS

Evolução anual das 4 categorias.

```python
df_cat = df_final.copy()
df_cat['categoria'] = df_cat['desfecho'].apply(categoria_desfecho)

for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    sub = df_cat[df_cat['ambiente'] == ambiente]
    tab = sub.groupby(['ano', 'categoria']).size().reset_index(name='n')
    total = sub.groupby('ano').size().reset_index(name='n')

    _ = plotar_barras_stf(
        df_dados=tab, col_x='ano', col_y='n', col_grupo='categoria',
        titulo=f'Desfecho por categoria — {ambiente} (2020–2025)',
        label_y='Inclusões em pauta',
        mostrar_linha_total=True, df_total=total, cores=CORES_CATEGORIA,
    )
```

---

# GRUPO 3 — Desfecho concluído por categoria e tipo de questão

Cruzamento das categorias de desfecho com o tipo de questão.

## 3.1 — Categoria × tipo de questão, período agregado (PV e PP)

Eixo X = tipo de questão; barras empilhadas pelas 4 categorias. Período total.

```python
df_cat = df_final.copy()
df_cat['categoria'] = df_cat['desfecho'].apply(categoria_desfecho)
df_cat['tipo_questao'] = df_cat['tipo_questao'].replace({'IJ': 'QI'})

for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    sub = df_cat[df_cat['ambiente'] == ambiente]
    tab = sub.groupby(['tipo_questao', 'categoria']).size().reset_index(name='n')
    total = sub.groupby('tipo_questao').size().reset_index(name='n')

    _ = plotar_barras_stf(
        df_dados=tab, col_x='tipo_questao', col_y='n', col_grupo='categoria',
        titulo=f'Desfecho por categoria e tipo de questão — {ambiente} (2020–2025)',
        label_y='Inclusões em pauta',
        mostrar_linha_total=True, df_total=total, cores=CORES_CATEGORIA,
    )
```

## 3.2 — Categoria × tipo de questão, por ano (PV e PP)

Um gráfico por tipo de questão (PR, RC, QI), mostrando a evolução anual das
4 categorias. Gera até 3 gráficos por ambiente.

```python
df_cat = df_final.copy()
df_cat['categoria'] = df_cat['desfecho'].apply(categoria_desfecho)
df_cat['tipo_questao'] = df_cat['tipo_questao'].replace({'IJ': 'QI'})

TIPOS = ['PR', 'RC', 'QI']

for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    sub_amb = df_cat[df_cat['ambiente'] == ambiente]
    for tipo in TIPOS:
        sub = sub_amb[sub_amb['tipo_questao'] == tipo]
        if sub.empty:
            continue
        tab = sub.groupby(['ano', 'categoria']).size().reset_index(name='n')
        total = sub.groupby('ano').size().reset_index(name='n')

        _ = plotar_barras_stf(
            df_dados=tab, col_x='ano', col_y='n', col_grupo='categoria',
            titulo=f'Desfecho por categoria — {tipo} — {ambiente} (2020–2025)',
            label_y='Inclusões em pauta',
            mostrar_linha_total=True, df_total=total, cores=CORES_CATEGORIA,
        )
```

---

# GRUPO 4 — Desfecho não concluído por categoria

As 4 categorias de não conclusão: pedido de vista, destaque, retirado de pauta,
motivos diversos. (No Plenário Físico não há destaques — sempre zero.)

## 4.1 — Não concluído por categoria, anual (PV e PP)

```python
df_nc = df_final[df_final['macro_desfecho'] == 'Não concluído'].copy()
df_nc['categoria_nc'] = df_nc['desfecho'].apply(categoria_nao_concluido)

for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    sub = df_nc[df_nc['ambiente'] == ambiente]
    tab = sub.groupby(['ano', 'categoria_nc']).size().reset_index(name='n')
    total = sub.groupby('ano').size().reset_index(name='n')

    _ = plotar_barras_stf(
        df_dados=tab, col_x='ano', col_y='n', col_grupo='categoria_nc',
        titulo=f'Não concluídos por categoria — {ambiente} (2020–2025)',
        label_y='Inclusões em pauta',
        mostrar_linha_total=True, df_total=total, cores=CORES_NC,
    )
```

## 4.2 — Não concluído por categoria, anual, por classe (PV e PP)

Um gráfico por classe (ADI, ADPF, ADC, ADO). Gera até 4 gráficos por ambiente.

```python
df_nc = df_final[df_final['macro_desfecho'] == 'Não concluído'].copy()
df_nc['categoria_nc'] = df_nc['desfecho'].apply(categoria_nao_concluido)

CLASSES = ['ADI', 'ADPF', 'ADC', 'ADO']

for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    sub_amb = df_nc[df_nc['ambiente'] == ambiente]
    for classe in CLASSES:
        sub = sub_amb[sub_amb['classe'] == classe]
        if sub.empty:
            continue
        tab = sub.groupby(['ano', 'categoria_nc']).size().reset_index(name='n')
        total = sub.groupby('ano').size().reset_index(name='n')

        _ = plotar_barras_stf(
            df_dados=tab, col_x='ano', col_y='n', col_grupo='categoria_nc',
            titulo=f'Não concluídos por categoria — {classe} — {ambiente} (2020–2025)',
            label_y='Inclusões em pauta',
            mostrar_linha_total=True, df_total=total, cores=CORES_NC,
        )
```

## 4.3 — Não concluído por categoria, anual, por tipo de questão (PV e PP)

Um gráfico por tipo de questão (PR, RC, QI). Gera até 3 gráficos por ambiente.

```python
df_nc = df_final[df_final['macro_desfecho'] == 'Não concluído'].copy()
df_nc['tipo_questao'] = df_nc['tipo_questao'].replace({'IJ': 'QI'})
df_nc['categoria_nc'] = df_nc['desfecho'].apply(categoria_nao_concluido)

TIPOS = ['PR', 'RC', 'QI']

for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    sub_amb = df_nc[df_nc['ambiente'] == ambiente]
    for tipo in TIPOS:
        sub = sub_amb[sub_amb['tipo_questao'] == tipo]
        if sub.empty:
            continue
        tab = sub.groupby(['ano', 'categoria_nc']).size().reset_index(name='n')
        total = sub.groupby('ano').size().reset_index(name='n')

        _ = plotar_barras_stf(
            df_dados=tab, col_x='ano', col_y='n', col_grupo='categoria_nc',
            titulo=f'Não concluídos por categoria — {tipo} — {ambiente} (2020–2025)',
            label_y='Inclusões em pauta',
            mostrar_linha_total=True, df_total=total, cores=CORES_NC,
        )
```

---

# Índice completo dos gráficos

| # | Grupo | Descrição | Eixo X | Facetas | Ambientes |
|---|-------|-----------|--------|---------|-----------|
| 1.1 | Tipo de questão | Não concluídos por tipo | ano | — | PV, PP |
| 1.2 | Tipo de questão | Concluídos por tipo | ano | — | PV, PP |
| 2.1 | Categoria concluído | Período agregado (pizza) | — | — | PV, PP |
| 2.2 | Categoria concluído | Por ano (barras) | ano | — | PV, PP |
| 3.1 | Categoria × tipo | Período agregado | tipo_questao | — | PV, PP |
| 3.2 | Categoria × tipo | Por ano | ano | por tipo | PV, PP |
| 4.1 | Categoria não concluído | Anual | ano | — | PV, PP |
| 4.2 | Categoria não concluído | Anual, por classe | ano | por classe | PV, PP |
| 4.3 | Categoria não concluído | Anual, por tipo | ano | por tipo | PV, PP |

## Notas de implementação

- **Unidade de análise**: inclusão em pauta (contagem de linhas de `df_final`),
  não processos distintos.
- **Renomeação IJ → QI**: aplicada apenas na exibição, via `.replace()` numa cópia;
  não altera `df_final`.
- **Retirado de pauta**: tratado como categoria própria nos gráficos de não
  concluído (não agrupado em "motivos diversos").
- **Plenário Físico**: não possui destaques (categoria sempre zero). Além disso,
  a classificação de desfecho do físico tem limitação conhecida — proporção alta
  de "motivos diversos" devido à natureza fragmentada e plurianual das sessões
  presenciais, onde a decisão frequentemente ocorre muito após a inclusão em pauta.
- **Supressão de auto-display**: prefixar chamadas finais de `plotar_barras_stf`
  com `_ =` para evitar gráficos duplicados no Jupyter.