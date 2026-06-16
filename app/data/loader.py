import streamlit as st
import pandas as pd
from huggingface_hub import hf_hub_download

@st.cache_data(ttl=3600)  # Cache por 1h — evita redownload a cada interação
def load_parquet(repo_id: str, filename: str) -> pd.DataFrame:
    path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        repo_type="dataset",
    )
    return pd.read_parquet(path)