"""Script de atualização dos datasets no HuggingFace Hub (seguindo DEPLOY_GUIDE.md).

Uso típico (após ter as credenciais):
    pip install -r requirements.txt
    export HF_TOKEN="hf_..."
    python scripts/upload_hf.py

Ou após login via CLI (recomendado - use o novo comando):
    hf auth login
    python scripts/upload_hf.py

Os arquivos parquet NÃO são versionados no Git — este script é a forma oficial
de publicar/atualizar os dados para consumo pelo dashboard no Streamlit Cloud.
"""

from __future__ import annotations

import os
from pathlib import Path

from huggingface_hub import HfApi

# Ajuste conforme seu usuário / repo no Hugging Face
REPO_ID = os.getenv("HF_REPO", "JoaoBoscoooo/stf-plenario-virtual")
DATASETS = ["andamentos", "decisoes", "deslocamentos", "processos"]  # 4 datasets (inclui a base principal)

# Diretório padrão dos parquets gerados pelo pipeline
DEFAULT_PROCESSED = Path("data/processed")


def main():
    token = os.getenv("HF_TOKEN")
    if token:
        api = HfApi(token=token)
        print("Usando token da variável de ambiente HF_TOKEN.")
    else:
        # Usa o token salvo via `hf auth login` (melhor prática atual)
        api = HfApi()
        print("Usando token salvo via `hf auth login` (recomendado).")

    print(f"Subindo datasets para https://huggingface.co/datasets/{REPO_ID}")
    for nome in DATASETS:
        caminho = DEFAULT_PROCESSED / f"{nome}.parquet"
        if not caminho.exists():
            print(f"  ⚠ {caminho} não encontrado — pulando")
            continue
        api.upload_file(
            path_or_fileobj=str(caminho),
            path_in_repo=f"{nome}.parquet",
            repo_id=REPO_ID,
            repo_type="dataset",
        )
        size_mb = caminho.stat().st_size / (1024 * 1024)
        print(f"  ✓ {nome}.parquet enviado ({size_mb:.2f} MB)")

    print("\nConcluído. Atualize o Streamlit Cloud (ou espere o próximo push) para o cache expirar.")
    print("Dica: em produção o cache do Streamlit expira automaticamente em ~1h (ou force reload limpando o @st.cache_data).")


if __name__ == "__main__":
    main()
