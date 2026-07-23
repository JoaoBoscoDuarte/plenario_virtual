# Refatoração: pipeline, notebooks e documentação

Data: 2026-07-23
Escopo: tudo exceto `app/` (Dashboard). Refatoração do app fica para um ciclo futuro.

## Contexto

`app/` (Streamlit) já é bem estruturado: camadas loader/filters/plots/layout
separadas, convenções documentadas em `app/DATA_LAYER.md`,
`app/PROJECT_STRUCTURE.md`, `filters.md` e `.amazonq/rules/memory-bank/guidelines.md`.
O lado de dados/pipeline é o oposto: sem código versionado.

Achados:
- `README.md` raiz vazio.
- `pyproject.toml` declara `stf-etl = "src.cleaning:_cli"`, mas `src/` não
  existe no repo — entry point quebrado.
- O script que gera `data/processed/*.parquet` a partir de
  `data/raw/ArquivosConcatenados.csv` (citado como `01_limpeza_preprocessing.py`
  em `CONTEXTO_DADOS.md`) nunca foi commitado — rodou só em notebook/Colab.
- `notebooks/` vazio, `scripts/` só tem `upload_hf.py`.
- `build/` órfão na raiz (não rastreado pelo git).
- Docs redundantes: `CONTEXTO_DADOS.md` existe idêntico na raiz e em
  `data/processed/CONTEXTO_DADOS.md`; dois `.docx` (`COMPLETA GRÁFICOS.docx`,
  `LISTA DE GRÁFICOS.docx`) provavelmente duplicam conteúdo já em `.md`.
- Três fontes de dependências: `requirements.txt`, `app/requirements.txt`,
  `pyproject.toml`.

## Plano

### Fase 0 — Higiene trivial (feito nesta sessão)
- Remover entry point `stf-etl` quebrado do `pyproject.toml` até `src/`
  existir de fato.
- Remover `build/` órfão.
- Remover `LISTA DE GRÁFICOS.docx` e `app/COMPLETA GRÁFICOS .docx` — conteúdo
  confirmado (via diff de texto extraído) já incorporado em
  `docs/LISTA_DE_GRAFICOS_controle.md` e `app/Especificacoes_graficos_Joao.md`
  respectivamente.
- Mover docs de contexto soltos na raiz para `docs/`: `CONTEXTO_DADOS.md`,
  `filters.md`, `plano_organizacao_pagina.md`. `data/processed/CONTEXTO_DADOS.md`
  é mantido como mirror intencional (acompanha o dataset publicado no HF).
- Atualizar as 2 referências aos `.docx` removidos em docstrings de
  `app/estilo.py` e `app/pages/bloco2_inclusoes/plots.py` (comentário only,
  sem mudança de lógica).

### Fase 1 — Documentação (feito nesta sessão)
- Preencher `README.md`: visão geral, setup, como rodar app, como rodar
  pipeline (placeholder), estrutura de pastas, links para docs existentes.
- Este documento.

### Fase 2 — Notebooks (usuário adiciona depois)
- Convenção: `notebooks/NN_descricao.ipynb`, numerado por ordem de execução
  (`01_limpeza_preprocessing.ipynb`, `02_...`).
- Cada notebook deve ser reproduzível a partir de `data/raw/` puro.
- Checklist "notebook → pipeline": lógica pura (sem estado de célula) vai
  para função em `src/`, notebook fica só orquestração + EDA.

### Fase 3 — Pipeline completo (depois dos notebooks)
- Criar `src/` real: pacote Python que implementa o ETL descrito em
  `CONTEXTO_DADOS.md` seção 5 (limpeza, explosão de JSON, star schema,
  validação, export parquet).
- Reconectar `stf-etl` no `pyproject.toml` a `src.cleaning:_cli`.
- Consolidar as 3 fontes de dependências em uma (`pyproject.toml` com
  extras `hf`/`dev` já existentes).
- Cada função do pipeline ganha um teste mínimo (assert-based), não
  suíte completa.

## Fora de escopo
- Qualquer mudança em `app/`.
- Qualquer mudança em `data/` (repo HF separado).
