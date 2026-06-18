from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st
from huggingface_hub import hf_hub_download

HF_REPO_ID = os.getenv("HF_REPO", "JoaoBoscoDuarte/stf-plenario-virtual")


def _try_local_parquet(filename: str) -> pd.DataFrame | None:
    """Try to load from local data/ tree (dev convenience).
    Searches by basename under processed/ and processed/acervo/ to support
    both flat files and the acervo subdir used for evolucao_acervo.parquet.
    """
    fname = Path(filename).name
    search_roots = [
        Path("data/processed"),
        Path("../data/processed"),
        Path("data/processed/acervo"),
        Path("../data/processed/acervo"),
    ]
    for root in search_roots:
        for p in root.glob(f"**/{fname}"):
            if p.exists():
                return pd.read_parquet(p)
    return None


@st.cache_data(ttl=3600)
def load_parquet(repo_id: str | None = None, filename: str = "") -> pd.DataFrame:
    """Download (or use local) a parquet dataset from the HF repo (or local mirror).
    Keeps backward compatibility with calls that pass explicit repo_id.
    """
    if not filename:
        raise ValueError("filename is required")
    repo_id = repo_id or HF_REPO_ID

    local = _try_local_parquet(filename)
    if local is not None:
        return local

    path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        repo_type="dataset",
    )
    return pd.read_parquet(path)


@st.cache_data(ttl=3600)
def load_evolucao_acervo() -> pd.DataFrame:
    """Carrega o dataset processado da evolução do acervo histórico.

    Usa fallback local (data/processed/acervo/evolucao_acervo.parquet) quando
    disponível (desenvolvimento). Em produção/Streamlit Cloud baixa via
    Hugging Face usando hf_hub_download.
    Segue a estrutura recomendada no IMPLEMENTACAO_GRAFICA.md.
    """
    local = _try_local_parquet("evolucao_acervo.parquet")
    if local is not None:
        return local

    # Structured path per the specification in IMPLEMENTACAO_GRAFICA.md
    filename = "processed/acervo/evolucao_acervo.parquet"
    path = hf_hub_download(
        repo_id=HF_REPO_ID,
        filename=filename,
        repo_type="dataset",
    )
    return pd.read_parquet(path)
