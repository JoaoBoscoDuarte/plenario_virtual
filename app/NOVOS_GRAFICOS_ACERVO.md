Esta documentação foi elaborada para orientar a equipe de desenvolvimento (ou você mesmo) na integração deste script de gráficos Plotly em um Dashboard (como Streamlit, Dash, ou um frontend customizado).

Abaixo, detalhamos a arquitetura do código, os requisitos de dados, o catálogo de gráficos gerados e os ajustes necessários para transpor o código do ambiente de cadernos (Jupyter/Colab) para uma aplicação web.

---

## 1. Requisitos e Estrutura de Dados

Para que os gráficos funcionem corretamente no dashboard, o *dataframe* base (`df_final`) deve conter obrigatoriamente as seguintes colunas:

* **`ano`**: Numérico ou categórico (ex: 2020, 2021).
* **`ambiente`**: Texto classificando o local (ex: `'Plenário Virtual'`, `'Plenário Físico'`).
* **`classe`**: Sigla da classe processual (ex: `'ADI'`, `'ADPF'`, `'ADC'`, `'ADO'`).
* **`desfecho`**: Texto detalhado com o resultado do julgamento.

**Transformação Inicial Necessária:**
O script exige a criação de uma coluna derivada chamada `macro_desfecho` logo na carga dos dados. Ela padroniza o detalhamento dos desfechos em três grandes categorias:

```python
def macro_desfecho(d):
    if str(d).startswith('Concluído'): return 'Concluído'
    if str(d).startswith('Não concluído'): return 'Não concluído'
    return 'Sem registro'

df_final['macro_desfecho'] = df_final['desfecho'].apply(macro_desfecho)

```

---

## 2. Identidade Visual (Design System)

O código centraliza a paleta de cores em dicionários globais. Isso garante consistência visual em todo o dashboard. Mantenha estas variáveis no topo do seu arquivo de configuração:

| Categoria | Dicionário/Variável | Cores (Hex) |
| --- | --- | --- |
| **Classes Judiciais** | `CORES_CLASSE` | ADI (Azul: `#2563eb`), ADPF (Laranja: `#f59e0b`), ADC (Verde: `#16a34a`), ADO (Vermelho: `#ef4444`) |
| **Status (Macro)** | `CORES_MACRO` | Concluído (Verde: `#16a34a`), Não concluído (Vermelho: `#ef4444`), Sem registro (Cinza: `#94a3b8`) |
| **Totais** | `COR_TOTAL` | Azul Claro: `#3498db` |
| **Linhas de Tendência** | `COR_LINHA` | Cinza Escuro: `#7f7f7f` |

> **Nota sobre o `LAYOUT_BASE`:** O dicionário `LAYOUT_BASE` está definido no seu código, mas as funções atualmente usam `fig.update_layout(...)` com parâmetros reescritos. Recomenda-se injetar o `LAYOUT_BASE` diretamente nas funções para evitar repetição de código no dashboard.

---

## 3. Funções Geradoras (Helpers)

O sistema utiliza duas funções principais de abstração. Elas devem ser colocadas em um módulo de utilitários (ex: `utils_charts.py`).

### `plotar_barras_stf`

Função versátil para criar gráficos de barras simples ou empilhadas (agrupadas), com suporte opcional a uma linha de total no eixo Y secundário.

* **Uso ideal:** Evolução temporal (anos no eixo X) de métricas quebradas por classe ou desfecho.
* **Atenção na Integração:** O parâmetro `df_dados` já deve chegar filtrado para a função.

### `plotar_pizza_stf`

Gera gráficos de proporção. Aceita o parâmetro `buraco` (hole), permitindo alternar entre formato Pizza tradicional (`buraco=0`) ou Rosca/Donut (`buraco=0.4`).

---

## 4. Catálogo de Gráficos para o Dashboard

Aqui está o mapeamento de todos os gráficos gerados pelo código, prontos para serem distribuídos nas abas ou seções do seu dashboard:

### Visão Geral de Inclusões

| ID | Título/Objetivo | Tipo Plotly | Segmentação |
| --- | --- | --- | --- |
| **5** | Inclusões por Ano e Ambiente | Barras Agrupadas | Plenário Virtual vs. Físico ao longo do tempo. |
| **5b** | Proporção PV vs PP (Total) | Pizza | Proporção histórica entre os dois ambientes. |

### Inclusões por Classe Processual

| ID | Título/Objetivo | Tipo Plotly | Segmentação |
| --- | --- | --- | --- |
| **6** | Inclusões por Classe (PV) | Barras + Linha (Total) | Evolução anual de ADI, ADPF, ADC, ADO no Virtual. |
| **6b** | Proporção por Classe (PV) | Pizza | Participação de cada classe no total do Virtual. |
| **7** | Inclusões por Classe (PP) | Barras + Linha (Total) | Evolução anual de classes no Físico. |
| **7b** | Proporção por Classe (PP) | Pizza | Participação de cada classe no total do Físico. |

### Desempenho e Desfechos (Geral e Anual)

| ID | Título/Objetivo | Tipo Plotly | Segmentação |
| --- | --- | --- | --- |
| **8** | Concluídos vs Não Concluídos (PV) | Pizza | Resumo geral de sucesso no Virtual. |
| **8b** | Desfecho Detalhado (PV) | Rosca (`buraco=0.3`) | Quebra específica dos motivos e resultados. |
| **9** | Concluídos vs Não Concluídos (PP) | Pizza | Resumo geral de sucesso no Físico. |
| **10** | Status Macro por Ano (PV) | Barras Agrupadas | Evolução temporal de concluídos/não concluídos. |
| **11** | Status Macro por Ano (PP) | Barras Agrupadas | O mesmo que o 10, aplicado ao Físico. |

### Aprofundamento Analítico (Filtros Específicos)

| ID | Título/Objetivo | Tipo Plotly | Segmentação |
| --- | --- | --- | --- |
| **12** | Apenas Concluídos por Ano (PV) | Barras Simples | Foco exclusivo no volume de entregas anuais (Virtual). |
| **13** | Apenas Concluídos por Ano (PP) | Barras Simples | Foco exclusivo no volume de entregas anuais (Físico). |
| **14** | Não Concluídos por Classe (PV) | Barras + Linha (Total) | Gargalos: o que ficou pendente por classe no Virtual. |
| **15** | Não Concluídos por Classe (PP) | Barras + Linha (Total) | Gargalos: o que ficou pendente por classe no Físico. |
| **16** | Concluídos por Classe (PV) | Barras + Linha (Total) | Entregas detalhadas por classe ao longo dos anos. |
| **17** | Concluídos por Classe (PP) | Barras + Linha (Total) | O mesmo que o 16, aplicado ao Físico. |

---

## 5. Passos para Adaptação no Dashboard

Como o código original foi escrito para um ambiente de cadernos/análise (com comandos `.show()`), você precisará fazer pequenos ajustes na hora de renderizá-los em um dashboard de produção.

**1. Remova os comandos `.show()`:**
Dentro das funções `plotar_barras_stf` e `plotar_pizza_stf`, assim como nos scripts soltos, remova ou comente a linha `fig.show()`. Em um dashboard, você deve retornar o objeto `fig` para que a interface o desenhe.

**2. Renderização por Framework:**

* **Se usar Streamlit:** Substitua `fig.show()` por `st.plotly_chart(fig, use_container_width=True)`.
* **Se usar Dash (Plotly):** Passe a figura para a propriedade `figure` de um componente Graph: `dcc.Graph(figure=fig)`.
* **Se usar Frontend customizado (React/Vue/Angular):** Converta a figura para JSON ao final da função retornando `fig.to_json()` e passe isso para a biblioteca `plotly.js` no client-side.

**3. Correção de Sintaxe (Aviso de Bug):**
No código do **Gráfico 14**, há um erro de digitação na criação do gráfico de linha que impedirá a execução em produção.

* **Linha atual:** `x=total14['ano'], y=total14['n'],a`
* **Correção:** Remova a letra `,a` perdida no final do eixo Y. Ficará: `x=total14['ano'], y=total14['n'],`

**4. Otimização de Performance:**
Atualmente, para os gráficos 14 a 17, você está criando um subset dos dados e calculando o *groupby* várias vezes (para o `tab` e para o `total`). Em um dashboard onde a velocidade importa, recomenda-se realizar o cálculo do DataFrame uma única vez, armazená-lo em cache (ex: `@st.cache_data` no Streamlit), e repassá-lo para a função de plotagem.