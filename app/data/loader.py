from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st
from huggingface_hub import hf_hub_download

# Repositório Hugging Face Datasets atual
# Configure via variável de ambiente:
#   HF_REPO=JoaoBoscoooo/plenario_virtual
#   HF_TOKEN=hf_...
HF_REPO_ID = os.getenv("HF_REPO", "JoaoBoscoooo/plenario_virtual")


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


def _get_hf_token():
    """Obtém HF token de várias fontes (ideal para Streamlit Cloud)."""
    # 1. Variável de ambiente (inclui secrets configurados no Streamlit Cloud)
    token = os.getenv("HF_TOKEN")
    if token:
        return token

    # 2. Streamlit secrets (st.secrets) - funciona quando rodando no Cloud
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            if "HF_TOKEN" in st.secrets:
                return st.secrets["HF_TOKEN"]
            # Também aceita dentro de uma seção [hf]
            if "hf" in st.secrets and "HF_TOKEN" in st.secrets["hf"]:
                return st.secrets["hf"]["HF_TOKEN"]
    except Exception:
        pass

    return None


@st.cache_data(ttl=3600)
def load_parquet(repo_id: str | None = None, filename: str = "") -> pd.DataFrame:
    """Download (or use local) a parquet dataset from the HF repo (or local mirror).

    Aceita tanto nome simples quanto caminho com prefixo (ex: "arquivosConcatenados.parquet"
    ou "processed/arquivosConcatenados.parquet").
    Tenta automaticamente localizações comuns no repositório.
    """
    if not filename:
        raise ValueError("filename is required")
    repo_id = repo_id or HF_REPO_ID

    local = _try_local_parquet(filename)
    if local is not None:
        return local

    token = _get_hf_token()

    # Tenta o filename exato + variações comuns (processed/ + basename)
    candidates = [filename]

    name = Path(filename).name
    if name != filename:
        candidates.append(name)
    else:
        # Se passou só o nome, também tenta processed/
        candidates.append(f"processed/{name}")

    # Remove duplicados mantendo ordem
    seen = set()
    unique_candidates = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            unique_candidates.append(c)

    last_error = None
    for cand in unique_candidates:
        try:
            path = hf_hub_download(
                repo_id=repo_id,
                filename=cand,
                repo_type="dataset",
                token=token,
            )
            return pd.read_parquet(path)
        except Exception as e:
            last_error = e
            continue

    # Se chegou aqui, falhou em todos
    raise RuntimeError(
        f"Não foi possível baixar '{filename}' do repositório {repo_id}. "
        f"Tentativas: {unique_candidates}. Último erro: {last_error}"
    ) from last_error


@st.cache_data(ttl=3600)
def load_evolucao_acervo() -> pd.DataFrame:
    """Carrega o dataset processado da evolução do acervo histórico.

    Usa fallback local ou baixa do Hugging Face (caminho processado/acervo/...).
    Segue a estrutura recomendada no IMPLEMENTACAO_GRAFICA.md.
    """
    # Reaproveita a lógica geral de load_parquet (local + HF + candidatos)
    # Usamos o repo explicitamente para evitar depender do default em versões antigas
    return load_parquet("JoaoBoscoooo/plenario_virtual", "processed/acervo/evolucao_acervo.parquet")
