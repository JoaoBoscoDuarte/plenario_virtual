# CONTEXTO_DADOS.md — Conjunto de Dados Processados do Plenário Virtual (STF)

> **Objetivo deste documento**: servir como contexto compartilhado para LLMs (Grok, Claude, GPT, etc.) entenderem o significado, propósito, estrutura e particularidades dos arquivos `.parquet` presentes em `data/processed/`.
>
> **Importante**: ignore completamente a pasta `processed/acervo/` (evolução de acervo histórico). Este documento foca exclusivamente nos 5 arquivos principais de processos.

---

## 1. Visão Geral e Propósito

Este dataset contém **informações processuais de ações de controle concentrado de constitucionalidade** julgadas (ou em tramitação) no **Plenário Virtual do Supremo Tribunal Federal (STF)**.

### Classes Processuais Abrangidas (exclusivamente)
- **ADI** — Ação Direta de Inconstitucionalidade (maioria esmagadora)
- **ADPF** — Arguição de Descumprimento de Preceito Fundamental
- **ADC** — Ação Declaratória de Constitucionalidade
- **ADO** — Ação Direta de Inconstitucionalidade por Omissão

### Finalidade Típica de Uso
- Jurimetria e análise quantitativa/qualitativa do STF
- Estudos sobre tempo de tramitação, perfil de autores, relatores, padrões de decisão
- Análise de texto (NLP) sobre decisões (`dec_link_conteúdo`)
- Estatísticas de movimentação processual (andamentos, deslocamentos)
- Identificação de padrões por origem geográfica, esfera institucional, etc.

**Cobertura temporal**: de 1988-10-06 até 2026-03-06 (data de protocolo).

**Volume principal** (valores aproximados observados):
- Processos (linhas na tabela fato): **9.358**
- Andamentos: ~505 mil
- Decisões: ~30 mil
- Deslocamentos: ~252 mil
- Partes: ~71 mil

---

## 2. Arquitetura dos Dados (Modelo Estrela)

O processamento seguiu o padrão **Star Schema**:

```
                    ┌─────────────────────┐
                    │ arquivosConcatenados│  ← TABELA FATO
                    │ (metadados gerais)  │
                    └──────────┬──────────┘
                               │ incidente (1:N)
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
   dim_partes          dim_andamentos       dim_decisoes
          │                    │                    │
          └────────────────────┴────────────────────┘
                               │
                               ▼
                      dim_deslocamentos
```

- **Chave primária da Fato**: `incidente` (único por processo)
- **Chave estrangeira nas dimensões**: `incidente`
- As 4 dimensões foram geradas pela **explosão** (normalização) de campos JSON aninhados do CSV original.
- Colunas pesadas de lista (`partes_total`, `andamentos_lista`, `decisões`, `deslocamentos_lista`) foram **removidas** da tabela fato após a explosão.

**Benefícios**:
- Evita redundância
- Permite contagens e agregações precisas
- Facilita joins e análises granulares

---

## 3. Tabela Fato: `arquivosConcatenados.parquet`

**Linhas**: 9.358 (um registro = um processo/incidente)

### Colunas e Descrições (baseado no dicionário original + transformações)

| Coluna                    | Tipo (atual)      | Descrição |
|---------------------------|-------------------|-----------|
| `incidente`               | int64             | Identificador único do processo (PK). |
| `classe`                  | category          | Sigla da classe (ADI, ADPF, ADC, ADO). |
| `nome_processo`           | str               | Ex: "ADI 1234". |
| `classe_extenso`          | category          | Nome completo da classe processual. |
| `tipo_processo`           | category          | "Físico" ou "Eletrônico". |
| `liminar`                 | object (list)     | Lista de pedidos de tutela de urgência (ex: `['MEDIDA LIMINAR']`). `None` quando não há. |
| `origem`                  | category          | UF de origem (DF lidera). |
| `relator`                 | category          | Ministro relator (pode incluir aposentados). |
| `autor1`                  | str               | Primeiro autor (PGR, Governadores, partidos, etc.). |
| `len(partes_total)`       | int64             | Contagem de partes (conveniência). |
| `data_protocolo`          | datetime64[ns]    | Data de entrada no tribunal. |
| `origem_orgao`            | str               | Órgão de origem original (detalhado). |
| `lista_assuntos`          | str               | Lista (stringificada) de assuntos/categorias temáticas. |
| `resumo`                  | str               | Texto longo (provavelmente resumo ou HTML da página do processo). Média ~2.8k caracteres. |
| `len(andamentos_lista)`   | int64             | Contagem de andamentos (conveniência). |
| `len(decisões)`           | int64             | Contagem de decisões (conveniência). |
| `len(deslocamentos)`      | int64             | Contagem de deslocamentos (conveniência). |
| `status_processo`         | category          | "Finalizado" ou "Em andamento". |
| `numero_processo`         | int64             | Número sequencial extraído de `nome_processo` (ex: 1234 de "ADI 1234"). |
| `esfera_origem`           | str               | **Coluna derivada** — macrocategoria do órgão de origem (Justiça Federal, Estadual, Eleitoral, Tribunais Superiores, Ministério Público, etc.). `Não Identificado` para nulos. |

### Particularidades Importantes
- `incidente` é único e identifica o processo de forma estável.
- `esfera_origem` foi criada por categorização textual para facilitar agregações (ver função `categorizar_esfera` no script).
- `lista_assuntos` e `liminar` permanecem como estruturas de lista/string (não foram explodidas).
- `resumo` pode conter ruído HTML de raspagem — tratar antes de NLP.
- Colunas `len(...)` são pré-computadas para evitar ter que contar nas dimensões em análises rápidas.

---

## 4. Tabelas de Dimensão

Todas as dimensões compartilham as colunas de contexto:
- `incidente`
- `classe`
- `tipo_processo`

### 4.1 `dim_partes.parquet`

Armazena todos os sujeitos processuais (autores, réus, interessados, amicus curiae, advogados etc.).

| Variável     | Tipo     | Descrição |
|--------------|----------|-----------|
| `incidente`  | int      | Chave para fato |
| `classe`     | str      | Classe processual |
| `tipo_processo` | str   | Físico / Eletrônico |
| `par__index` | int      | Posição sequencial da parte na lista original do processo |
| `par_tipo`   | str      | Papel jurídico (`REQTE.(S)`, `ADV.`, `INTDO`, `AM. CURIAE`, etc.) |
| `par_nome`   | str      | Nome completo (pessoa, órgão, entidade + OAB quando aplicável) |

**Observação**: Prefixo `par_` + `_index` resulta em `par__index`.

### 4.2 `dim_andamentos.parquet` (maior tabela)

Histórico completo de eventos e certidões do processo.

| Variável           | Tipo     | Descrição |
|--------------------|----------|-----------|
| `incidente`        | int      | Chave |
| `classe` / `tipo_processo` | ... | Contexto |
| `and_index`        | int      | Número do andamento (geralmente ordem cronológica inversa) |
| `and_data`         | str      | Data do evento (formato dd/mm/aaaa ou similar) |
| `and_nome`         | str      | Título do ato (ex: "Petição", "Conclusos", "Expedido", "BAIXA AO ARQUIVO DO STF") |
| `and_complemento`  | str      | Detalhes (número de petição, destinatário, guia etc.) |
| `and_julgador`     | str      | Geralmente 'NA' para atos de secretaria |
| `and_validade`     | str      | Validação interna |
| `and_link`         | str      | URL para PDF (quando disponível) |
| `and_link_tipo`    | object   | Tipo/extensão do link |
| `and_link_conteúdo`| str      | Texto extraído (OCR ou digital) da peça vinculada |

### 4.3 `dim_decisoes.parquet`

Decisões com carga decisória (monocráticas, colegiadas, liminares, julgamentos etc.).

| Variável            | Tipo     | Descrição |
|---------------------|----------|-----------|
| `incidente`         | int      | Chave |
| `dec_index`         | int      | Relaciona com `and_index` do andamento correspondente |
| `dec_data`          | str      | Data da decisão |
| `dec_nome`          | str      | Tipo (ex: "Procedente", "Medida Cautelar", "Julgamento Virtual", "Despacho") |
| `dec_complemento`   | str      | Resumo ou dispositivo curto |
| `dec_julgador`      | str      | Ministro ou "Tribunal" / "Plenário" |
| `dec_validade`      | str      | Validação |
| `dec_link`          | str      | Link para íntegra |
| `dec_link_tipo`     | object   | |
| `dec_link_conteúdo` | str      | **Teor completo da decisão** — excelente para análise textual / embeddings |

### 4.4 `dim_deslocamentos.parquet`

Movimentação física/eletrônica dos autos entre setores do STF.

| Variável            | Tipo  | Descrição |
|---------------------|-------|-----------|
| `incidente`         | int   | Chave |
| `des_index`         | int   | Sequencial da remessa |
| `des_data_recebido` | str   | "Recebido em DD/MM/AAAA" ou similar |
| `des_enviado por`   | str   | Secretaria/coordenação de origem |
| `des_recebido por`  | str   | Secretaria/coordenação de destino (pode repetir informação) |
| `des_guia`          | str   | Número da Guia de Remessa |

---

## 5. Processo de Geração (Resumo do Pré-processamento)

O arquivo `01_limpeza_preprocessing.py` (conversão direta do notebook original) documenta todo o pipeline. Principais etapas:

1. **Leitura** do CSV bruto (`ArquivosConcatenados.csv`).
2. **Exploração e documentação** (tabelas de descrição de colunas originais + estrutura interna dos JSONs).
3. **Limpeza e padronização**:
   - Normalização de nulos (`NA`, `[]`, strings vazias → `None`)
   - Extração de `numero_processo`
   - Parse de `liminar` (string → lista)
   - Engenharia de `esfera_origem` (categorização por palavras-chave)
   - Conversão de `data_protocolo` para datetime
   - Conversão de colunas de baixa cardinalidade para `category`
4. **Explosão dos campos JSON** (`explodir_json_veloz`):
   - Função otimizada que usa `ast.literal_eval` + `explode` + `json_normalize`
   - Aplica prefixos (`par_`, `and_`, `dec_`, `des_`)
   - Limpa nulos internos
5. **Remoção** das 4 colunas de listas pesadas da tabela fato.
6. **Validação**:
   - Unicidade de `incidente`
   - Range de datas (1988–2026)
   - Classes restritas ao escopo
   - Integridade referencial (dimensões só referenciam incidentes existentes)
7. **Exportação** para Apache Parquet (compressão + preservação de tipos).

**Nunca rode o script completo em ambiente com pouca memória** — ele foi projetado para rodar em Colab com o CSV completo + explosões.

---

## 6. Dicas de Uso para LLMs e Análises

### Joins Recomendados
```python
# Exemplo básico
fato = pd.read_parquet("arquivosConcatenados.parquet")
andamentos = pd.read_parquet("dim_andamentos.parquet")

df = fato.merge(andamentos, on="incidente", how="left", suffixes=("", "_and"))
```

### Contagens Rápidas
Use as colunas `len(...)` da tabela fato antes de contar nas dimensões.

### Datas
- `data_protocolo` → já é `datetime`
- Colunas de data nas dimensões (`and_data`, `dec_data`, ...) → geralmente strings → converter com `pd.to_datetime(..., dayfirst=True, errors="coerce")`

### Filtros Comuns
- Classes: `df["classe"].isin(["ADI", "ADPF"])`
- Período: derivar ano de `data_protocolo` ou usar `filter_by_year_range` (ver camada `app/data/filters.py`)
- Status: separar "Finalizado" vs "Em andamento"

### Cuidados
- `resumo` pode ter HTML — limpe com BeautifulSoup ou regex antes de usar.
- `lista_assuntos` está como string JSON-like — use `ast.literal_eval` quando precisar.
- Algumas decisões podem ter `dec_link_conteúdo` vazio.
- `and_index` / `dec_index` podem estar em ordem inversa (mais recente primeiro).
- Relatores incluem ministros aposentados (histórico completo).

### Performance
Parquet é colunar — ao ler, prefira:
```python
pd.read_parquet(f, columns=["incidente", "classe", "data_protocolo"])
```

---
## 8. Resumo para LLMs

**O que é?**  
Dados estruturados de ~9.358 processos constitucionais do STF (1988–2026) em formato analítico (fato + 4 dimensões).

**Para que serve?**  
Análises quantitativas, temporais, textuais e de rede sobre o controle concentrado de constitucionalidade no Brasil.

**Como está estruturado?**  
Tabela central (`arquivosConcatenados`) + tabelas detalhadas de andamentos/decisões/deslocamentos/partes ligadas por `incidente`.

**Como foi construído?**  
Limpeza + engenharia de features + explosão de JSONs (ver seção 5 e o script `.py`).

**Não se esqueça**: 
- `incidente` é a chave universal.
- Ignore `acervo/`.
- Converta datas nas dimensões.
- Aproveite as colunas de contagem `len(...)`.

---

*Documento gerado para uso por múltiplas LLMs. Mantenha sincronizado com mudanças no pipeline ou adições de colunas.*
