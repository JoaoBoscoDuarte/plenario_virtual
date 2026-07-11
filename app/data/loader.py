from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st
from huggingface_hub import hf_hub_download

from config import HF_REPO_ID, HF_FILES


def _try_local_parquet(filename: str) -> pd.DataFrame | None:
    """Tenta carregar o arquivo localmente (conveniência em desenvolvimento)."""
    fname = Path(filename).name
    search_roots = [
        Path("data/processed"),
        Path("../data/processed"),
        Path("data/processed/acervo"),
        Path("../data/processed/acervo"),
    ]
    for root in search_roots:
        p = root / fname
        if p.exists():
            return pd.read_parquet(p)
    return None


def _get_hf_token() -> str | None:
    """Obtém o HF token de variável de ambiente ou Streamlit secrets."""
    token = os.getenv("HF_TOKEN")
    if token:
        return token

    try:
        if hasattr(st, "secrets"):
            if "HF_TOKEN" in st.secrets:
                return st.secrets["HF_TOKEN"]
            if "hf" in st.secrets and "HF_TOKEN" in st.secrets["hf"]:
                return st.secrets["hf"]["HF_TOKEN"]
    except Exception:
        pass

    return None


@st.cache_data(ttl=3600)
def load_parquet(repo_id: str, filename: str) -> pd.DataFrame:
    """Baixa (ou usa local) um arquivo parquet do repositório HF.

    Tenta o caminho exato e, como fallback, apenas o basename dentro de processed/.
    O cache é aplicado aqui — funções loader específicas não precisam de decorator.
    """
    if not filename:
        raise ValueError("filename é obrigatório.")

    local = _try_local_parquet(filename)
    if local is not None:
        return local

    token = _get_hf_token()

    name = Path(filename).name
    candidates = dict.fromkeys([filename, name, f"processed/{name}"])

    last_error: Exception | None = None
    for cand in candidates:
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

    raise RuntimeError(
        f"Não foi possível baixar '{filename}' do repositório '{repo_id}'. "
        f"Tentativas: {list(candidates)}. Último erro: {last_error}"
    ) from last_error


# ── Loaders específicos ───────────────────────────────────────────────────────
# Cada função é um wrapper simples — o cache já está em load_parquet.
# Para adicionar um novo dataset: registrar o path em config.HF_FILES
# e criar uma função load_<nome>() seguindo o mesmo padrão.


def load_evolucao_acervo() -> pd.DataFrame:
    """Carrega o dataset de evolução anual do acervo histórico."""
    return load_parquet(HF_REPO_ID, HF_FILES["evolucao_acervo"])


def load_inclusoes_em_pauta() -> pd.DataFrame:
    """Carrega o dataset de inclusões em pauta (2020–2025)."""
    return load_parquet(HF_REPO_ID, HF_FILES["inclusoes_em_pauta"])
