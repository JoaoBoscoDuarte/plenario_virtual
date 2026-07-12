Sim, mas com uma nuance importante para cada gráfico.

## Gráfico 1 (pizza — geral) — só precisa da coluna `tramitacao`

Mas com um cuidado: você precisa contar **processos distintos**, não inclusões. Se plotar direto a coluna, cada processo é contado várias vezes (uma por inclusão). Então:

```python
# Correto: uma linha por processo
serie_tram = (
    df_final.drop_duplicates('incidente')['tramitacao']
    .value_counts()
)

CORES_TRAM = {
    'Ambos os ambientes': '#8b5cf6',
    'Só Virtual':         '#2563eb',
    'Só Físico':          '#f59e0b',
}

_ = plotar_pizza_reajuste(
    serie_tram,
    titulo='Tramitação por ambiente — processos CC (2020–2025)',
    cores=CORES_TRAM,
)
```

O `drop_duplicates('incidente')` garante que cada processo conte uma vez só. Só com a coluna `tramitacao` (e o `incidente` que já existe), esse gráfico sai.

## Gráfico 2 (por tipo de questão) — precisa da `tramitacao` + `tipo_questao`

Aqui a coluna `tipo_questao` já existe no `df_final`, então também funciona. Mas de novo, contando processos distintos:

```python
# Processos que tramitaram em ambos, um por incidente, com seu tipo de questão
ambos = (
    df_final[df_final['tramitou_ambos']]
    .drop_duplicates('incidente')
    .copy()
)
ambos['tipo_questao'] = ambos['tipo_questao'].replace({'IJ': 'QI'})

tab_tipo = ambos['tipo_questao'].value_counts().reset_index()
tab_tipo.columns = ['tipo_questao', 'n']

CORES_TIPO = {'PR': '#2563eb', 'RC': '#f59e0b', 'QI': '#16a34a'}

_ = plotar_barras_reajuste(
    tab_tipo, col_x='tipo_questao', col_grupo=None,
    titulo='Processos em ambos os ambientes, por tipo de questão (2020–2025)',
    label_y='Processos',
    cores=CORES_TIPO,
)
```

## Resumo

| Gráfico | Colunas necessárias | Já no dataset? |
|---|---|---|
| 1 — Pizza geral | `incidente` + `tramitacao` | ✅ Sim |
| 2 — Por tipo de questão | `incidente` + `tramitacao`/`tramitou_ambos` + `tipo_questao` | ✅ Sim |

Então **sim** — com as duas colunas novas (`tramitacao` e `tramitou_ambos`) mais as que já existem (`incidente`, `tipo_questao`), os dois gráficos saem completos.

O único cuidado real é o `drop_duplicates('incidente')` — porque a pergunta é sobre **processos** que tramitaram nos dois ambientes, e o `df_final` tem uma linha por inclusão. Sem o drop, você contaria o mesmo processo várias vezes e os números ficariam inflados.

Uma ressalva sobre o tipo de questão no gráfico 2: como o processo tramitou em dois ambientes, ele pode ter tipos diferentes em cada inclusão. O `drop_duplicates('incidente')` pega o tipo da primeira linha — que pode não ser representativo. Se quiser precisão nesse ponto, me diz que ajusto para pegar, por exemplo, o tipo da inclusão virtual (já que o tipo é mais confiável no virtual).