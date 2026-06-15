"""
Central loader for the dashboard datasets.

Supports two modes (per DEPLOY_GUIDE + practical dev needs):
- LOCAL (default for development and "just run the dashboard"): reads directly from data/processed/*.parquet
- HF (production on Streamlit Cloud): uses datasets.load_dataset from Hugging Face Hub

Caching via @st.cache_data to keep interactions snappy.
The HF path is ready; simply set HF_REPO and provide token via st.secrets or env.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Callable

import pandas as pd
import streamlit as st

# Optional heavy dependency — only required when using the Hugging Face Hub path.
# We import at top level (per quality standards) but guard its usage.
try:
    from datasets import load_dataset  # type: ignore
except ImportError:  # pragma: no cover
    load_dataset = None  # type: ignore

# Local fallback (dev / "quero só ver o dashboard")
DEFAULT_LOCAL_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"

# HF (produção / deploy). Altere para seu repo quando publicar os dados.
HF_REPO = os.getenv("HF_REPO", "seu-usuario/stf-plenario-virtual")


def _get_hf_token() -> str | None:
    """Lê token do Hugging Face de st.secrets ou variável de ambiente."""
    try:
        return st.secrets["huggingface"]["token"]
    except Exception:
        return os.getenv("HF_TOKEN")


@st.cache_data(ttl=3600, show_spinner=False)
def _load_local(name: str) -> pd.DataFrame:
    path = DEFAULT_LOCAL_DIR / f"{name}.parquet"
    if not path.exists():
        # Fallback útil se alguém rodar de outro cwd
        alt = Path("data/processed") / f"{name}.parquet"
        if alt.exists():
            path = alt
        else:
            # Em vez de raise imediato, deixamos o caller decidir o fallback
            # (o _choose_loader agora captura FileNotFoundError e usa HF)
            raise FileNotFoundError(
                f"Parquet local não encontrado para '{name}'. "
                "Na nuvem, certifique-se de que USE_LOCAL_DATA=0 e os arquivos estão no HF."
            )
    return pd.read_parquet(path)


@st.cache_data(ttl=3600, show_spinner="Carregando dados do Hugging Face...")
def _load_from_hf(name: str, token: str | None = None) -> pd.DataFrame:
    if load_dataset is None:
        raise RuntimeError(
            "Pacote 'datasets' não está instalado. "
            "Instale com `pip install datasets huggingface-hub` ou use o modo local."
        )
    ds = load_dataset(HF_REPO, data_files=f"{name}.parquet", token=token or _get_hf_token())
    return ds["train"].to_pandas()


def _choose_loader() -> Callable[[str], pd.DataFrame]:
    # Produção no Streamlit Cloud deve usar HF.
    # Defina USE_LOCAL_DATA=0 nas Environment variables do app na Cloud.
    # Para dev local com dados locais: USE_LOCAL_DATA=1 (padrão).
    # Se quiser forçar HF mesmo localmente: FORCE_HF=1.
    use_local = os.getenv("USE_LOCAL_DATA", "1") == "1"
    force_hf = os.getenv("FORCE_HF", "0") == "1"

    if use_local and not force_hf:
        def loader(name: str) -> pd.DataFrame:
            try:
                return _load_local(name)
            except FileNotFoundError:
                # Fallback automático para HF se os arquivos locais não existirem
                # (útil em deploys onde a pasta data/ não foi copiada)
                return _load_from_hf(name)
            except Exception:
                raise
        return loader

    # HF como fonte principal (recomendado para Cloud / produção)
    return _load_from_hf


_loader = _choose_loader()


def load_processos() -> pd.DataFrame:
    """Tabela principal (incidente + metadados + relator + flags derivadas)."""
    return _loader("processos")


def load_andamentos() -> pd.DataFrame:
    return _loader("andamentos")


def load_decisoes() -> pd.DataFrame:
    return _loader("decisoes")


def load_deslocamentos() -> pd.DataFrame:
    return _loader("deslocamentos")


# Helper para páginas que querem todas de uma vez (com cache já aplicado)
def load_all() -> dict[str, pd.DataFrame]:
    return {
        "processos": load_processos(),
        "andamentos": load_andamentos(),
        "decisoes": load_decisoes(),
        "deslocamentos": load_deslocamentos(),
    }
