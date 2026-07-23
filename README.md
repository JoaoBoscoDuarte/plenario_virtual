# STF Plenário Virtual — Jurimetria

Dashboard e pipeline de análise do Plenário Virtual do STF: ~9.358 processos
de controle concentrado de constitucionalidade (ADI/ADPF/ADC/ADO),
1988–2026, em formato analítico (star schema).

## Estrutura

```
app/         Dashboard Streamlit (não coberto por esta refatoração)
data/        Dados processados (.parquet) e brutos — repo git separado, clone HF
docs/        Documentação de controle e specs de design
notebooks/   Notebooks de EDA e construção do pipeline (em construção)
scripts/     Utilitários (ex: upload_hf.py)
```

Detalhes do dashboard: [app/PROJECT_STRUCTURE.md](app/PROJECT_STRUCTURE.md),
[app/DATA_LAYER.md](app/DATA_LAYER.md), [docs/filters.md](docs/filters.md).
Contrato dos dados processados: [docs/CONTEXTO_DADOS.md](docs/CONTEXTO_DADOS.md).
Plano de refatoração do pipeline: [docs/superpowers/specs/2026-07-23-refatoracao-pipeline-design.md](docs/superpowers/specs/2026-07-23-refatoracao-pipeline-design.md).

## Setup

```bash
pip install -e .
# ou
pip install -r requirements.txt
```

## Rodar o dashboard

```bash
streamlit run app/app.py
```

Lê `data/processed/` localmente; sem token necessário em dev. Em produção
(Streamlit Cloud) usa Hugging Face Datasets (`HF_REPO`/`HF_TOKEN`, ver
[app/DATA_LAYER.md](app/DATA_LAYER.md)).

## Pipeline de dados (em construção)

Hoje `data/processed/*.parquet` é gerado manualmente (notebook/Colab), sem
código versionado no repo. Notebooks e pipeline (`raw/ArquivosConcatenados.csv`
→ star schema) estão sendo adicionados — ver plano de refatoração acima.

## Publicar dados no Hugging Face

```bash
python scripts/upload_hf.py
```
