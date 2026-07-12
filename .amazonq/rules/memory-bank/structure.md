# Project Structure

## Directory Tree

```
plenario_virtual/
├── app/                        # Streamlit application
│   ├── app.py                  # Entry point — navigation only
│   ├── config.py               # Global constants (HF repo, file paths)
│   ├── requirements.txt        # App-specific dependencies
│   ├── components/
│   │   └── filters.py          # Sidebar UI widgets (Streamlit only, no data logic)
│   ├── data/
│   │   ├── loader.py           # Data loading + caching (HF or local)
│   │   └── filters.py          # Pure filtering logic (no Streamlit imports)
│   └── pages/
│       ├── acervo/             # Page: Acervo Histórico
│       │   ├── acervo.py       # Orchestrator (load → filter → render)
│       │   ├── plots.py        # Plotly figure builders (no Streamlit)
│       │   └── layout.py       # st.* rendering (no figure building)
│       ├── inclusoes/          # Page: Inclusões em Pauta
│       │   ├── inclusoes.py
│       │   ├── plots.py
│       │   └── layout.py
│       └── geral/              # Page: Visão Geral
│           ├── geral.py
│           └── layout.py
├── data/
│   ├── processed/              # Parquet datasets (star schema)
│   │   ├── arquivosConcatenados.parquet   # Fact table (9,358 processes)
│   │   ├── dim_andamentos.parquet         # ~505k procedural events
│   │   ├── dim_decisoes.parquet           # ~30k decisions
│   │   ├── dim_deslocamentos.parquet      # ~252k file movements
│   │   ├── dim_partes.parquet             # ~71k parties
│   │   ├── inclusoes_em_pauta.parquet
│   │   ├── inclusoes_com_pauta.parquet
│   │   ├── sessoes_virtuais.parquet
│   │   └── acervo/
│   │       └── evolucao_acervo.parquet
│   └── raw/
│       └── ArquivosConcatenados.csv       # Original source data
├── docs/                       # Control documents and graph lists
├── notebooks/                  # EDA and analysis notebooks
├── scripts/
│   └── upload_hf.py            # Upload datasets to Hugging Face
├── pyproject.toml              # Package config (stf-plenario-virtual v0.2.0)
└── requirements.txt            # Full dependency list
```

## Core Components and Relationships

### Data Flow
```
loader.py (cached)
    │
    ▼
<pagina>.py ──► data/filters.py ──► df filtrado
    │
    ▼
layout.py ──► plots.py ──► go.Figure
    │
    ▼
st.plotly_chart(fig)
```

### Layer Responsibilities

| Layer | File | Responsibility |
|-------|------|----------------|
| Entry | `app.py` | Navigation registration only |
| Config | `config.py` | HF repo ID, file paths, constants |
| Loading | `data/loader.py` | `@st.cache_data` parquet loading (local → HF fallback) |
| Filtering | `data/filters.py` | Pure pandas filtering, no Streamlit |
| UI Widgets | `components/filters.py` | Sidebar widgets, returns filter dict |
| Figures | `pages/*/plots.py` | Plotly figure construction, no Streamlit |
| Rendering | `pages/*/layout.py` | `st.*` calls, receives figures |
| Orchestration | `pages/*/<page>.py` | Load → filter → render, nothing else |

## Data Architecture (Star Schema)

```
arquivosConcatenados (FACT, key: incidente)
    ├── dim_partes         (parties per process)
    ├── dim_andamentos     (procedural events)
    ├── dim_decisoes       (decisions with full text)
    └── dim_deslocamentos  (file movements between sectors)
```

## Deployment
- **Production**: Streamlit Cloud + Hugging Face Datasets (`JoaoBoscoooo/plenario_virtual`)
- **Local dev**: reads from `data/processed/` directly, no token needed
- **Cache TTL**: 1 hour via `@st.cache_data(ttl=3600)`
