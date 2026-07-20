# Plano de Implementação — Gráficos de Sessões Virtuais Iniciadas

## Contexto e bases de dados

Dois DataFrames alimentam todos os gráficos:

**`df_sessoes_final`** — unidade de análise principal. Colunas relevantes:
- `incidente` — identificador do processo
- `ano` — ano da sessão (2020–2025)
- `classe` — ADI, ADPF, ADC, ADO
- `relator` — nome do ministro relator
- `tipo_questao` — PR, RC, QI (IJ já renomeado para QI)
- `desfecho` — desfecho detalhado da sessão
- `macro_desfecho` — "Concluído" ou "Não concluído"
- `data_sessao_dt` — data da sessão (datetime)

**`df_final`** — inclusões em pauta, usado apenas no Bloco 5 (duração). Filtrar para `ambiente == 'Plenário Virtual'` antes de usar.

**Volumes de referência:** 4.335 sessões | 2.624 processos distintos | 2020–2025

**Preparação obrigatória antes de qualquer gráfico:**
```python
df_s = df_sessoes_final.copy()
df_s['tipo_questao'] = df_s['tipo_questao'].replace({'IJ': 'QI'})
df_s['data_sessao_dt'] = pd.to_datetime(df_s['data_sessao_dt'])
df_s['mes'] = df_s['data_sessao_dt'].dt.month
df_s['trimestre'] = df_s['data_sessao_dt'].dt.quarter
```

---

## BLOCO 1 — Sazonalidade (3 gráficos + 1 tabela)

### G1.1 — Sessões por mês
- **Tipo:** barras simples
- **Eixo X:** mês (Jan a Dez, nomes abreviados)
- **Eixo Y:** contagem de sessões
- **Derivação:** `df_s['mes'].value_counts().sort_index()`, reindexar range(1,13)
- **Mapa de meses:** `{1:'Jan', 2:'Fev', ..., 12:'Dez'}`
- **Título:** "Sessões virtuais por mês — 2020–2025"
- **Nota:** Janeiro tem 1 sessão e Julho tem 12 — recessos judiciários visíveis

### G1.2 — Sessões por mês e ano (tabela)
- **Tipo:** tabela impressa (não gráfico)
- **Derivação:** `df_s.groupby(['ano','mes']).size().unstack(fill_value=0)`
- **Finalidade:** referência numérica de sazonalidade por ano

### G1.3 — Sessões por trimestre e ano
- **Tipo:** barras agrupadas
- **Eixo X:** ano (2020–2025)
- **Grupos:** T1, T2, T3, T4
- **Eixo Y:** contagem de sessões
- **Derivação:** `df_s.groupby(['ano','trimestre']).size()`
- **Linha de total:** sim (`df_s.groupby('ano').size()`)
- **Título:** "Sessões virtuais por trimestre e ano — 2020–2025"

---

## BLOCO 2 — Relator (4 gráficos)

**Pré-processamento:** filtrar top 10 relatores por volume.
```python
TOP_N = 10
top_relatores = df_s['relator'].value_counts().head(TOP_N).index.tolist()
df_top = df_s[df_s['relator'].isin(top_relatores)].copy()
```

Top 10 de referência (em ordem): Gilmar Mendes 538, Barroso 450, Cármen Lúcia 437, Fachin 408, Alexandre de Moraes 397, Nunes Marques 385, Rosa Weber 365, Dias Toffoli 334, Marco Aurélio 236, Luiz Fux 201.

### G2.1 — Sessões por relator
- **Tipo:** barras simples
- **Eixo X:** nome do relator (top 10, ordenado por volume decrescente)
- **Eixo Y:** contagem de sessões
- **Derivação:** `df_s['relator'].value_counts().head(10)`
- **Título:** "Sessões virtuais por relator — Top 10 (2020–2025)"

### G2.2 — Taxa de conclusão por relator
- **Tipo:** barras simples
- **Eixo X:** nome do relator (top 10, ordenado por taxa decrescente)
- **Eixo Y:** percentual (%)
- **Derivação:** `df_top.groupby('relator')['macro_desfecho'].apply(lambda x: round(100*(x=='Concluído').mean(), 1))`
- **Título:** "Taxa de conclusão por relator — Top 10 (2020–2025)"

### G2.3 — Macro-desfecho por relator
- **Tipo:** barras empilhadas
- **Eixo X:** nome do relator (top 10)
- **Grupos:** "Concluído" / "Não concluído"
- **Eixo Y:** contagem de sessões
- **Derivação:** `df_top.groupby(['relator','macro_desfecho']).size()`
- **Título:** "Macro-desfecho por relator — Top 10 (2020–2025)"

### G2.4 — Sessões por relator e classe
- **Tipo:** barras empilhadas
- **Eixo X:** nome do relator (top 10)
- **Grupos:** ADI, ADPF, ADC, ADO
- **Eixo Y:** contagem de sessões
- **Derivação:** `df_top.groupby(['relator','classe']).size()`
- **Título:** "Sessões por relator e classe — Top 10 (2020–2025)"

---

## BLOCO 3 — Múltiplas sessões por processo (4 gráficos)

**Pré-processamento:** calcular número de sessões por processo e posição de cada sessão.
```python
sess_por_proc = df_s.groupby('incidente').size().reset_index(name='n_sessoes')
sess_por_proc = sess_por_proc.merge(
    df_s[['incidente','classe','tipo_questao','macro_desfecho']].drop_duplicates('incidente'),
    on='incidente', how='left'
)

def faixa_sessoes(n):
    if n == 1: return '1 sessão'
    if n <= 3: return '2–3 sessões'
    if n <= 5: return '4–5 sessões'
    return '6+ sessões'

sess_por_proc['faixa'] = sess_por_proc['n_sessoes'].apply(faixa_sessoes)
ORDEM_FAIXA = ['1 sessão', '2–3 sessões', '4–5 sessões', '6+ sessões']

# Posição de cada sessão no histórico do processo
df_s_ord = df_s.sort_values(['incidente','data_sessao_dt']).copy()
df_s_ord['n_sessao'] = df_s_ord.groupby('incidente').cumcount() + 1
```

Volumes de referência: 1 sessão = 1.605 processos | 2–5 sessões = 989 | >5 sessões = 30.

### G3.1 — Distribuição de sessões por processo
- **Tipo:** barras simples
- **Eixo X:** faixa (ordem fixa: 1 sessão / 2–3 / 4–5 / 6+)
- **Eixo Y:** contagem de processos
- **Derivação:** `sess_por_proc['faixa'].value_counts().reindex(ORDEM_FAIXA)`
- **Título:** "Distribuição de sessões por processo — 2020–2025"

### G3.2 — Faixa de sessões por classe
- **Tipo:** barras empilhadas
- **Eixo X:** classe (ADI, ADPF, ADC, ADO)
- **Grupos:** faixas (1 sessão / 2–3 / 4–5 / 6+)
- **Eixo Y:** contagem de processos
- **Derivação:** `sess_por_proc.groupby(['classe','faixa']).size()`
- **Título:** "Número de sessões por processo e classe — 2020–2025"

### G3.3 — Taxa de conclusão: 1ª sessão vs posteriores
- **Tipo:** barras simples (2 barras)
- **Eixo X:** "1ª sessão" / "Sessões posteriores"
- **Eixo Y:** percentual (%)
- **Derivação:**
```python
df_s_ord['posicao'] = df_s_ord['n_sessao'].apply(
    lambda n: '1ª sessão' if n == 1 else 'Sessões posteriores'
)
df_s_ord.groupby('posicao')['macro_desfecho'].apply(
    lambda x: round(100*(x=='Concluído').mean(), 1)
)
```
- **Título:** "Taxa de conclusão: 1ª sessão vs sessões posteriores — 2020–2025"
- **Interpretação esperada:** a 1ª sessão deve ter taxa muito superior às posteriores

### G3.4 — Taxa de conclusão por posição da sessão
- **Tipo:** barras simples (4 barras)
- **Eixo X:** posição (ordem fixa: 1ª / 2ª / 3ª / 4ª+ sessão)
- **Eixo Y:** percentual (%)
- **Derivação:**
```python
def posicao_label(n):
    if n <= 3: return f'{n}ª sessão'
    return '4ª+ sessão'

ORDEM_POS = ['1ª sessão', '2ª sessão', '3ª sessão', '4ª+ sessão']
df_s_ord['posicao_n'] = df_s_ord['n_sessao'].apply(posicao_label)
df_s_ord.groupby('posicao_n')['macro_desfecho'].apply(
    lambda x: round(100*(x=='Concluído').mean(), 1)
).reindex(ORDEM_POS)
```
- **Título:** "Taxa de conclusão por posição da sessão no processo — 2020–2025"

---

## BLOCO 4 — Cruzamentos (5 gráficos + 2 tabelas)

### G4.1 — Classe × tipo de questão (tabela)
- **Tipo:** tabela impressa
- **Derivação:** `df_s.groupby(['classe','tipo_questao']).size().unstack(fill_value=0)`
- **Finalidade:** referência para G4.2

### G4.2 — Sessões por classe e tipo de questão
- **Tipo:** barras agrupadas
- **Eixo X:** classe (ADI, ADPF, ADC, ADO)
- **Grupos:** PR, RC, QI
- **Eixo Y:** contagem de sessões
- **Derivação:** `df_s.groupby(['classe','tipo_questao']).size()`
- **Título:** "Sessões por classe e tipo de questão — 2020–2025"

### G4.3 — Macro-desfecho por ano, por tipo de questão (3 gráficos separados)
- **Tipo:** barras empilhadas, um gráfico por tipo (PR, RC, QI)
- **Eixo X:** ano (2020–2025)
- **Grupos:** "Concluído" / "Não concluído"
- **Eixo Y:** contagem de sessões
- **Linha de total:** sim
- **Derivação:** filtrar `df_s` por tipo, depois `groupby(['ano','macro_desfecho']).size()`
- **Títulos:** "Macro-desfecho por ano — PR — Sessões virtuais (2020–2025)" (idem RC e QI)

### G4.4 — Macro-desfecho por ano, por classe (2 gráficos — só ADI e ADPF)
- **Tipo:** barras empilhadas, um gráfico por classe
- **Eixo X:** ano (2020–2025)
- **Grupos:** "Concluído" / "Não concluído"
- **Eixo Y:** contagem de sessões
- **Linha de total:** sim
- **Derivação:** filtrar `df_s` por classe, depois `groupby(['ano','macro_desfecho']).size()`
- **Títulos:** "Macro-desfecho por ano — ADI — Sessões virtuais (2020–2025)" (idem ADPF)
- **Nota:** ADC (79 sessões) e ADO (40 sessões) têm base pequena — omitir ou incluir disclaimer

### G4.5 — Taxa de conclusão: classe × tipo de questão (tabela + gráfico)
- **Tabela:** `df_s.groupby(['classe','tipo_questao'])['macro_desfecho'].apply(lambda x: round(100*(x=='Concluído').mean(),1)).unstack()`
- **Gráfico:** barras agrupadas
- **Eixo X:** classe
- **Grupos:** PR, RC, QI
- **Eixo Y:** percentual (%)
- **Título:** "Taxa de conclusão por classe e tipo de questão — Sessões virtuais (2020–2025)"

---

## BLOCO 5 — Duração até conclusão (3 gráficos)

**Pré-processamento:** calcular dias entre primeira inclusão em pauta e sessão de conclusão.
```python
# Primeira inclusão em pauta de cada processo (do df_final virtual)
df_final_virt = df_final[df_final['ambiente'] == 'Plenário Virtual'].copy()
primeira_pauta = (
    df_final_virt.groupby('incidente')['data_inclusao_dt'].min()
    .reset_index(name='primeira_pauta_dt')
)

# Sessão de conclusão (a última com macro_desfecho == 'Concluído')
sess_concluidas = (
    df_s[df_s['macro_desfecho'] == 'Concluído']
    .sort_values('data_sessao_dt')
    .groupby('incidente').last()
    .reset_index()[['incidente','data_sessao_dt','classe','tipo_questao']]
)

duracao = sess_concluidas.merge(primeira_pauta, on='incidente', how='left')
duracao['dias'] = (duracao['data_sessao_dt'] - duracao['primeira_pauta_dt']).dt.days
duracao = duracao[duracao['dias'] >= 0]

def faixa_duracao(d):
    if d <= 30:  return '≤ 30 dias'
    if d <= 90:  return '31–90 dias'
    if d <= 180: return '91–180 dias'
    if d <= 365: return '6–12 meses'
    if d <= 730: return '1–2 anos'
    return '> 2 anos'

ORDEM_DUR = ['≤ 30 dias','31–90 dias','91–180 dias','6–12 meses','1–2 anos','> 2 anos']
duracao['faixa_dur'] = duracao['dias'].apply(faixa_duracao)
```

Estatísticas de referência (calcular no notebook antes de plotar):
```python
print(duracao['dias'].describe())
```

### G5.1 — Distribuição de duração até conclusão
- **Tipo:** barras simples
- **Eixo X:** faixa de duração (ordem fixa: ≤30 / 31–90 / 91–180 / 6–12m / 1–2a / >2a)
- **Eixo Y:** contagem de processos concluídos
- **Derivação:** `duracao['faixa_dur'].value_counts().reindex(ORDEM_DUR)`
- **Título:** "Tempo até conclusão — Processos virtuais (2020–2025)"

### G5.2 — Duração mediana por classe
- **Tipo:** barras simples
- **Eixo X:** classe (ADI, ADPF, ADC, ADO)
- **Eixo Y:** dias (mediana)
- **Derivação:** `duracao.groupby('classe')['dias'].median().round(0).astype(int)`
- **Título:** "Tempo mediano até conclusão por classe (dias) — 2020–2025"

### G5.3 — Duração mediana por tipo de questão
- **Tipo:** barras simples
- **Eixo X:** tipo de questão (PR, RC, QI)
- **Eixo Y:** dias (mediana)
- **Derivação:** `duracao.groupby('tipo_questao')['dias'].median().round(0).astype(int)`
- **Título:** "Tempo mediano até conclusão por tipo de questão (dias) — 2020–2025"

---

## Resumo

| Bloco | Tema | Gráficos | Tabelas |
|---|---|---|---|
| 1 | Sazonalidade | 2 | 1 |
| 2 | Relator | 4 | 0 |
| 3 | Múltiplas sessões | 4 | 0 |
| 4 | Cruzamentos | 7 | 2 |
| 5 | Duração | 3 | 0 |
| **Total** | | **20** | **3** |