# Gráficos de Sustentação Oral — Inclusões em Pauta STF (2020–2025)

Guia para construção dos gráficos de sustentação oral no controle concentrado
de constitucionalidade (ADI, ADPF, ADC, ADO) do STF.

## Fonte de dados

Usar o **dataset mestre**, que já contém a coluna `teve_sustentacao` pré-calculada:

```python
import pandas as pd
from pathlib import Path

PROCESSED_PATH = Path('/content/drive/MyDrive/Plenário Virtual/data/processed')

df_final = pd.read_parquet(
    PROCESSED_PATH / 'inclusoes_em_pauta_mestre.parquet', engine='pyarrow'
)
```

Ler do dataset mestre evita reprocessar a detecção de sustentação (que varre
~505 mil andamentos). A coluna já está pronta.

## Colunas relevantes

- `incidente` — identificador do processo
- `ano` — ano da inclusão (2020–2025)
- `ambiente` — `"Plenário Virtual"` ou `"Plenário Físico"`
- `classe` — `ADI`, `ADPF`, `ADC`, `ADO`
- `tipo_questao` — `PR`, `RC`, `IJ` (renomear para `QI` na exibição)
- `teve_sustentacao` — booleano: a inclusão teve sustentação oral realizada

## Como a sustentação oral foi detectada (contexto)

A marcação `teve_sustentacao` foi construída assim:

1. Um andamento conta como sustentação oral se `and_nome == 'Sustentação Oral'`
   OU se o `and_complemento` casa o padrão `sustenta[çc]\w*\s+or`
   (captura formatos não padronizados, comuns no Plenário Físico).
2. São **excluídas** as sustentações indeferidas/rejeitadas/não realizadas —
   quando um termo de negação (indeferir/rejeitar/negar/cancelar) aparece a até
   30 caracteres da menção à sustentação.
3. Uma inclusão em pauta recebe `teve_sustentacao = True` se houver ao menos um
   andamento de sustentação entre 15 dias antes e 30 dias após a data da inclusão
   (a sustentação pode ser protocolada antes do início da sessão).

Resultado de referência: 27,4% das inclusões virtuais e 22,0% das físicas têm
sustentação oral. A detecção ampliada foi essencial — usar só `and_nome`
subestimava o físico (3,4%), pois a sustentação presencial é registrada em
formato diferente.

## Cores

```python
CORES_SUST = {
    'Com sustentação oral': '#0891b2',   # ciano
    'Sem sustentação oral': '#e5e7eb',   # cinza claro
}
CORES_CLASSE = {
    'ADI': '#2563eb', 'ADPF': '#f59e0b', 'ADC': '#16a34a', 'ADO': '#ef4444',
}
CORES_TIPO = {'PR': '#2563eb', 'RC': '#f59e0b', 'QI': '#16a34a'}
```

## Funções de plotagem (pré-existentes)

```python
def plotar_pizza_reajuste(serie, titulo, cores=None):
    """Pizza (donut) para proporção com/sem determinada característica."""

def plotar_barras_reajuste(df_dados, col_x, col_grupo=None, titulo='',
                            label_y='Inclusões', cores=None):
    """Barras (simples ou agrupadas). df_dados deve ter col_x, col_grupo e 'n'."""
```

Nota: prefixar chamadas finais com `_ =` para suprimir o auto-display do Jupyter
e evitar gráficos duplicados.

---

# GRÁFICO 1 e 2 — Sustentação oral — Período — PV e PP (pizza)

Proporção de inclusões com/sem sustentação oral no período inteiro.

```python
for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    sub = df_final[df_final['ambiente'] == ambiente]
    serie = sub['teve_sustentacao'].map({
        True:  'Com sustentação oral',
        False: 'Sem sustentação oral'
    }).value_counts()

    print(f"{ambiente}: {sub['teve_sustentacao'].sum():,} com sustentação "
          f"de {len(sub):,} ({100*sub['teve_sustentacao'].mean():.1f}%)")

    _ = plotar_pizza_reajuste(
        serie,
        titulo=f'Inclusões com sustentação oral — {ambiente} (2020–2025)',
        cores=CORES_SUST,
    )
```

# GRÁFICO 3 e 4 — Sustentação oral — Anual — PV e PP (barras por ano)

Contagem de inclusões com sustentação oral por ano.

```python
for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    sub = df_final[(df_final['ambiente'] == ambiente) & (df_final['teve_sustentacao'])]
    tab = sub.groupby('ano').size().reset_index(name='n')
    # Garante todos os anos, mesmo com zero
    tab = tab.set_index('ano').reindex(range(2020, 2026), fill_value=0).reset_index()

    _ = plotar_barras_reajuste(
        tab, col_x='ano',
        titulo=f'Inclusões com sustentação oral por ano — {ambiente} (2020–2025)',
    )
```

---

# Gráficos adicionais possíveis (mesma coluna)

Caso a análise precise ir além dos 4 gráficos base, a coluna `teve_sustentacao`
permite os seguintes cortes, todos no mesmo padrão:

## Por ano e classe (barras agrupadas)

```python
for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    sub = df_final[(df_final['ambiente'] == ambiente) & (df_final['teve_sustentacao'])]
    tab = sub.groupby(['ano', 'classe']).size().reset_index(name='n')

    _ = plotar_barras_reajuste(
        tab, col_x='ano', col_grupo='classe',
        titulo=f'Sustentação oral por ano e classe — {ambiente} (2020–2025)',
        cores=CORES_CLASSE,
    )
```

## Por ano e tipo de questão (barras agrupadas, só PV)

```python
sub = df_final[
    (df_final['ambiente'] == 'Plenário Virtual') & (df_final['teve_sustentacao'])
].copy()
sub['tipo_questao'] = sub['tipo_questao'].replace({'IJ': 'QI'})
tab = sub.groupby(['ano', 'tipo_questao']).size().reset_index(name='n')

_ = plotar_barras_reajuste(
    tab, col_x='ano', col_grupo='tipo_questao',
    titulo='Sustentação oral por ano e tipo de questão — Plenário Virtual (2020–2025)',
    cores=CORES_TIPO,
)
```

## Comparação de taxa entre ambientes (barras lado a lado)

Percentual de inclusões com sustentação em cada ambiente, por ano.

```python
tab = (
    df_final.groupby(['ano', 'ambiente'])['teve_sustentacao']
    .mean().mul(100).reset_index(name='n')  # 'n' aqui é o percentual
)

_ = plotar_barras_reajuste(
    tab, col_x='ano', col_grupo='ambiente',
    titulo='Taxa de sustentação oral por ano e ambiente (%) (2020–2025)',
    label_y='% de inclusões com sustentação',
)
```

---

# Índice dos gráficos

| # | Descrição | Eixo X | Grupo | Ambientes | Formato |
|---|-----------|--------|-------|-----------|---------|
| 1 | Sustentação — período | — | — | PV | pizza |
| 2 | Sustentação — período | — | — | PP | pizza |
| 3 | Sustentação — anual | ano | — | PV | barras |
| 4 | Sustentação — anual | ano | — | PP | barras |
| + | Sustentação — anual por classe | ano | classe | PV, PP | barras agrupadas |
| + | Sustentação — anual por tipo | ano | tipo_questao | PV | barras agrupadas |
| + | Taxa por ambiente | ano | ambiente | ambos | barras agrupadas |

## Notas de implementação

- **Unidade de análise**: inclusão em pauta (contagem de linhas), não processos
  distintos. Para contar processos, aplicar `.drop_duplicates('incidente')`.
- **Fonte**: sempre o `inclusoes_em_pauta_mestre.parquet`, que já traz
  `teve_sustentacao` calculada. Não reprocessar a detecção para plotar.
- **Renomeação IJ → QI**: só na exibição, via `.replace()` numa cópia.
- **Reindex de anos**: usar `.reindex(range(2020, 2026), fill_value=0)` nos
  gráficos anuais para não omitir anos sem ocorrências.
- **Interpretação do físico**: a taxa de 22% no físico só é correta com a detecção
  ampliada (nome + complemento). A sustentação presencial não usa o `and_nome`
  padronizado, então uma detecção que olhasse só o `and_nome` subestimaria o físico.
- **Sustentações indeferidas**: já excluídas na construção de `teve_sustentacao`
  (pedidos negados/rejeitados/não realizados não contam).
- **Supressão de auto-display**: prefixar chamadas finais com `_ =`.