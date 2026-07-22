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


def _corrigir_tipo_questao_2016_2019(df: pd.DataFrame) -> pd.DataFrame:
    """Reclassifica PR->RC para 72 inclusões do PV (2016-2019) cujo sufixo recursal
    (ex: "ADI-ED", "ADPF-AgR") está no texto do andamento mas não foi extraído pelo
    pipeline upstream (bug na extração de sufixo, não erro na coleta do dado).
    Lista derivada de app/dados/correcao_tipo_questao_2016_2019.csv via regex sobre
    and_complemento (ver histórico do repo); validada contra os números de referência
    da cliente (PR 422->350, RC 189->261 no PV, 2016-2019).
    """
    path = Path(__file__).resolve().parent / "correcao_tipo_questao_2016_2019.csv"
    correcao = pd.read_csv(path)[["incidente", "data_inclusao", "andamento_origem", "tipo_questao_corrigido"]]
    correcao = correcao.drop_duplicates(subset=["incidente", "data_inclusao", "andamento_origem"])
    df = df.merge(correcao, on=["incidente", "data_inclusao", "andamento_origem"], how="left")
    df["tipo_questao"] = df["tipo_questao_corrigido"].fillna(df["tipo_questao"])
    return df.drop(columns=["tipo_questao_corrigido"])


def load_inclusoes_em_pauta() -> pd.DataFrame:
    """Carrega o dataset de inclusões em pauta (2016–2025)."""
    df = load_parquet(HF_REPO_ID, HF_FILES["inclusoes_em_pauta"])
    df["ambiente"] = df["ambiente"].replace("Plenário Físico", "Plenário Presencial")
    df["macro_desfecho"] = df["desfecho"].str.split(" - ").str[0]
    df = _corrigir_tipo_questao_2016_2019(df)
    return df


def load_sustentacao_oral() -> pd.DataFrame:
    """Carrega o dataset de inclusões com marcação de sustentação oral."""
    df = load_parquet(HF_REPO_ID, HF_FILES["sustentacao_oral"])
    df["ambiente"] = df["ambiente"].replace("Plenário Físico", "Plenário Presencial")
    return df


def load_tramitacoes() -> pd.DataFrame:
    """Carrega o dataset de inclusões com tramitação por ambiente (PV/PP/ambos)."""
    df = load_parquet(HF_REPO_ID, HF_FILES["tramitacoes"])
    df["ambiente"] = df["ambiente"].replace("Plenário Físico", "Plenário Presencial")
    df["tramitacao"] = df["tramitacao"].replace({"Só Virtual": "Virtual", "Só Físico": "Físico"})
    return df


def load_reajustes_de_voto() -> pd.DataFrame:
    """Carrega os andamentos de reajuste de voto (nível evento)."""
    return load_parquet(HF_REPO_ID, HF_FILES["reajustes_de_voto"])


def load_sessoes_virtuais() -> pd.DataFrame:
    """Carrega o dataset de sessões virtuais."""
    return load_parquet(HF_REPO_ID, HF_FILES["sessoes_virtuais"])
