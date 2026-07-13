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
- `desfecho` — desfecho detalhado da inclusão
- `teve_sustentacao` — booleano: a inclusão teve sustentação oral realizada

## Como a sustentação oral foi detectada (contexto)

A marcação `teve_sustentacao` foi construída assim:

1. Um andamento conta como sustentação oral se `and_nome == 'Sustentação Oral'`
   OU se o `and_complemento` casa o padrão `sustenta[çc]\w*\s+or`
   (captura formatos não padronizados, comuns no Plenário Físico).
2. São **excluídas** as sustentações indeferidas/rejeitadas/não realizadas —
   quando um termo de negação (indeferir/rejeitar/negar/cancelar) aparece a até
   30 caracteres da menção à sustentação. Também exclui o andamento de nome
   "Arquivo de sustentação oral rejeitado".
3. Uma inclusão em pauta recebe `teve_sustentacao = True` se houver ao menos um
   andamento de sustentação entre 15 dias antes e 30 dias após a data da inclusão
   (a sustentação pode ser protocolada antes do início da sessão).

A detecção ampliada foi essencial: usar só `and_nome` subestimava o físico
(3,4%), pois a sustentação presencial é registrada em formato diferente. Com a
detecção ampliada, o físico sobe para um patamar realista.

---

# UNIVERSO DE ANÁLISE (fundamental)

A análise de sustentação oral **NÃO** usa o `df_final` inteiro. O universo é o
total de inclusões em pauta **MENOS** dois grupos que não podem/devem entrar:

1. **Tipo de questão RC** — recursos (AgR, ED) **não têm direito** a sustentação
   oral. Incluí-los infla o denominador com casos onde sustentação é impossível.
2. **Desfecho "retirado de pauta"** — inclusões retiradas **não chegaram a
   julgamento**, então não faz sentido avaliar sustentação nelas.

Restam apenas **PR e IJ (QI)** que **não foram retiradas**.

```python
# Universo de análise da sustentação oral
universo_sust = df_final[
    (df_final['tipo_questao'] != 'RC') &
    (df_final['desfecho'] != 'Não concluído - retirado de pauta')
].copy()

# Renomeia IJ -> QI para exibição
universo_sust['tipo_questao'] = universo_sust['tipo_questao'].replace({'IJ': 'QI'})

print(f"Total de inclusoes:        {len(df_final):,}")
print(f"  (-) tipo RC:             {(df_final['tipo_questao'] == 'RC').sum():,}")
print(f"  (-) retirado de pauta:   {(df_final['desfecho'] == 'Não concluído - retirado de pauta').sum():,}")
print(f"Universo de analise:       {len(universo_sust):,}")
```

**Todos os gráficos abaixo operam sobre `universo_sust`, nunca sobre `df_final`.**

Resultado de referência (universo de análise):

- Plenário Virtual: 31,8% das inclusões válidas têm sustentação oral
- Plenário Físico: 24,2%

## Cores

```python
CORES_SUST = {
    'Com sustentação oral': '#0891b2',   # ciano
    'Sem sustentação oral': '#e5e7eb',   # cinza claro
}
CORES_TIPO = {'PR': '#2563eb', 'QI': '#16a34a'}  # RC nao entra no universo
CORES_DESFECHO = {
    'Concluído - decisão unânime':                    '#16a34a',
    'Concluído - decisão maioria com o relator':      '#2563eb',
    'Concluído - decisão maioria, vencido o relator': '#f59e0b',
    'Não concluído - pedido de vista':                '#8b5cf6',
    'Não concluído - destaque':                       '#ec4899',
    'Não concluído - motivos diversos':               '#9ca3af',
}
```

## Funções de plotagem (pré-existentes)

```python
def plotar_pizza_reajuste(serie, titulo, cores=None):
    """Pizza (donut) para proporção com/sem determinada característica."""

def plotar_barras_reajuste(df_dados, col_x, col_grupo=None, titulo='',
                            label_y='Inclusões', cores=None):
    """Barras (simples ou agrupadas). df_dados deve ter col_x, col_grupo e 'n'."""
```

Nota: prefixar chamadas finais com `_ =` para suprimir o auto-display do Jupyter.

---

# GRÁFICO 1 e 2 — Sustentação oral — Período — PV e PP (pizza)

Proporção de inclusões (do universo) com/sem sustentação oral no período.

```python
for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    sub = universo_sust[universo_sust['ambiente'] == ambiente]
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

```python
for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    sub = universo_sust[
        (universo_sust['ambiente'] == ambiente) & (universo_sust['teve_sustentacao'])
    ]
    tab = sub.groupby('ano').size().reset_index(name='n')
    tab = tab.set_index('ano').reindex(range(2020, 2026), fill_value=0).reset_index()

    _ = plotar_barras_reajuste(
        tab, col_x='ano',
        titulo=f'Inclusões com sustentação oral por ano — {ambiente} (2020–2025)',
    )
```

# GRÁFICO 5 e 6 — Sustentação por tipo de questão (PR e QI) — PV e PP

RC não aparece porque foi excluído do universo.

```python
for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    sub = universo_sust[
        (universo_sust['ambiente'] == ambiente) & (universo_sust['teve_sustentacao'])
    ]
    tab = sub.groupby(['ano', 'tipo_questao']).size().reset_index(name='n')

    _ = plotar_barras_reajuste(
        tab, col_x='ano', col_grupo='tipo_questao',
        titulo=f'Sustentação oral por ano e tipo de questão — {ambiente} (2020–2025)',
        label_y='Inclusões com sustentação',
        cores=CORES_TIPO,
    )
```

# GRÁFICO 7 e 8 — Sustentação por tipo de desfecho — PV e PP

"Retirado de pauta" não aparece porque foi excluído do universo.

```python
for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    sub = universo_sust[
        (universo_sust['ambiente'] == ambiente) & (universo_sust['teve_sustentacao'])
    ]
    tab = sub.groupby('desfecho').size().reset_index(name='n')
    tab = tab.sort_values('n', ascending=False)

    _ = plotar_barras_reajuste(
        tab, col_x='desfecho', col_grupo=None,
        titulo=f'Sustentação oral por tipo de desfecho — {ambiente} (2020–2025)',
        label_y='Inclusões com sustentação',
    )
```

---

# Taxas de referência (universo de análise)

## Por tipo de questão

| Ambiente         | PR               | QI              |
| ---------------- | ---------------- | --------------- |
| Plenário Virtual | 31,1% (904/2907) | 38,0% (120/316) |
| Plenário Físico  | 27,5% (42/153)   | 33,8% (24/71)   |

QI tem taxa de sustentação maior que PR em ambos os ambientes.

## Por tipo de desfecho (Plenário Virtual)

| Desfecho                   | Taxa de sustentação |
| -------------------------- | ------------------- |
| Pedido de vista            | 41,4% (a maior)     |
| Maioria com o relator      | 31,4%               |
| Decisão unânime            | 29,0%               |
| Motivos diversos           | 25,7%               |
| Destaque                   | 25,2%               |
| Maioria, vencido o relator | 19,0% (a menor)     |

Achado: a maior taxa de sustentação está nos casos com pedido de vista, sugerindo
que sustentação oral e vista sinalizam casos mais complexos ou controversos.

---

# Índice dos gráficos

| #   | Descrição             | Eixo X   | Grupo                | Ambientes | Formato          |
| --- | --------------------- | -------- | -------------------- | --------- | ---------------- |
| 1   | Sustentação — período | —        | —                    | PV        | pizza            |
| 2   | Sustentação — período | —        | —                    | PP        | pizza            |
| 3   | Sustentação — anual   | ano      | —                    | PV        | barras           |
| 4   | Sustentação — anual   | ano      | —                    | PP        | barras           |
| 5   | Por tipo de questão   | ano      | tipo_questao (PR/QI) | PV        | barras agrupadas |
| 6   | Por tipo de questão   | ano      | tipo_questao (PR/QI) | PP        | barras agrupadas |
| 7   | Por tipo de desfecho  | desfecho | —                    | PV        | barras           |
| 8   | Por tipo de desfecho  | desfecho | —                    | PP        | barras           |

## Notas de implementação

- **UNIVERSO**: sempre `universo_sust` (df_final sem RC e sem retirados de pauta),
  nunca `df_final` inteiro. Este é o ponto mais importante do guia.
- **Unidade de análise**: inclusão em pauta (contagem de linhas). Para processos
  distintos, aplicar `.drop_duplicates('incidente')`.
- **Fonte**: `inclusoes_em_pauta_mestre.parquet`, que já traz `teve_sustentacao`.
- **Renomeação IJ -> QI**: aplicada na criação do `universo_sust`.
- **RC excluído**: recursos não têm direito a sustentação oral. Controle de
  qualidade: apenas 2,7% dos RCs tinham sustentação detectada (ruído esperado).
- **Retirado de pauta excluído**: inclusões retiradas não chegaram a julgamento.
- **Reindex de anos**: usar `.reindex(range(2020, 2026), fill_value=0)` nos
  gráficos anuais.
- **Interpretação do físico**: a taxa realista do físico só aparece com a detecção
  ampliada (nome + complemento).
- **Supressão de auto-display**: prefixar chamadas finais com `_ =`.
