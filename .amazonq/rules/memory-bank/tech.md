# Technology Stack

## Languages and Runtime
- **Python** >= 3.10 (devcontainer uses Python 3.11)
- No JavaScript/TypeScript — pure Python stack

## Core Dependencies

| Package | Version | Role |
|---------|---------|------|
| `streamlit` | >=1.35.0 | Web dashboard framework |
| `plotly` | >=5.20.0 | Interactive chart library |
| `pandas` | >=2.0.0 | Data manipulation |
| `pyarrow` | >=14.0.0 | Parquet file I/O |
| `numpy` | >=1.26.0 | Numerical operations |
| `huggingface-hub` | >=0.20.0 | Dataset hosting/download |
| `datasets` | >=2.18.0 | HF dataset access |
| `python-dotenv` | >=1.0.0 | Environment variable loading |

## Optional / Dev Dependencies
- `jupyter`, `ipykernel` — notebook-based EDA
- `matplotlib`, `seaborn` — notebook visualizations
- `altair` >=5.0.0 — alternative charting (listed in requirements)
- `openpyxl` — Excel export support

## Build System
- **setuptools** >= 61.0 via `pyproject.toml`
- Package name: `stf-plenario-virtual` v0.2.0
- Editable install: `pip install -e .`

## Data Storage
- **Format**: Apache Parquet (columnar, compressed)
- **Production hosting**: Hugging Face Datasets (`JoaoBoscoooo/plenario_virtual`)
- **Local path**: `data/processed/`
- **Raw source**: CSV (`data/raw/ArquivosConcatenados.csv`)

## Streamlit Theme (`.streamlit/config.toml`)
```toml
primaryColor = "#1f4e79"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

## Development Commands

```bash
# Install in editable mode (enables clean imports)
pip install -e .

# Run dashboard locally
streamlit run app/app.py

# Run in devcontainer (auto-started on attach)
streamlit run app/app.py --server.enableCORS false --server.enableXsrfProtection false

# Upload datasets to Hugging Face
python scripts/upload_hf.py
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HF_REPO` | Hugging Face repo ID | `JoaoBoscoooo/plenario_virtual` |
| `HF_TOKEN` | Auth token for private repos | — |

On Streamlit Cloud, set these under **Settings → Secrets** as TOML:
```toml
HF_TOKEN = "hf_..."
HF_REPO  = "JoaoBoscoooo/plenario_virtual"
```

## Devcontainer
- Base image: `mcr.microsoft.com/devcontainers/python:1-3.11-bookworm`
- Port 8501 auto-forwarded and opened as preview
- Extensions: `ms-python.python`, `ms-python.vscode-pylance`
