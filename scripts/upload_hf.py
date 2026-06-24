"""Script de atualização dos datasets no HuggingFace Hub.

Uso típico:
    export HF_REPO="JoaoBoscoooo/plenario_virtual"
    export HF_TOKEN="hf_..."
    python scripts/upload_hf.py

Ou use o CLI:
    hf auth login
    python scripts/upload_hf.py

Nunca commitar tokens no Git.
Os arquivos parquet NÃO são versionados no Git — use este script para publicar.
"""

from __future__ import annotations

import os
from pathlib import Path

from huggingface_hub import HfApi

# Ajuste conforme seu usuário / repo no Hugging Face (atualizado)
REPO_ID = os.getenv("HF_REPO", "JoaoBoscoooo/plenario_virtual")

# Mapeamento de arquivos reais no disco -> caminho no HF (suporta estrutura
# recomendada em IMPLEMENTACAO_GRAFICA.md para o acervo e arquivos atuais).
# Mantemos os principais datasets flat por compatibilidade atual; acervo usa subpasta.
FILES = [
    ("arquivosConcatenados.parquet", "processed/arquivosConcatenados.parquet"),
    ("dim_andamentos.parquet", "processed/dim_andamentos.parquet"),
    ("dim_decisoes.parquet", "processed/dim_decisoes.parquet"),
    ("dim_deslocamentos.parquet", "processed/dim_deslocamentos.parquet"),
    ("dim_partes.parquet", "processed/dim_partes.parquet"),
    # Acervo histórico (conforme spec do IMPLEMENTACAO_GRAFICA.md)
    ("acervo/evolucao_acervo.parquet", "processed/acervo/evolucao_acervo.parquet"),
]

# Diretório padrão dos parquets — relativo à raiz do projeto (pai de scripts/)
DEFAULT_PROCESSED = Path(__file__).resolve().parent.parent / "data" / "processed"


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
    for local_rel, remote_path in FILES:
        caminho = DEFAULT_PROCESSED / local_rel
        if not caminho.exists():
            print(f"  ⚠ {caminho} não encontrado — pulando")
            continue
        api.upload_file(
            path_or_fileobj=str(caminho),
            path_in_repo=remote_path,
            repo_id=REPO_ID,
            repo_type="dataset",
        )
        size_mb = caminho.stat().st_size / (1024 * 1024)
        print(f"  ✓ {remote_path} enviado ({size_mb:.2f} MB)")

    print("\nConcluído. Atualize o Streamlit Cloud (ou espere o próximo push) para o cache expirar.")
    print("Dica: em produção o cache do Streamlit expira automaticamente em ~1h (ou force reload limpando o @st.cache_data).")
    print("Nota: acervo usa 'processed/acervo/evolucao_acervo.parquet' no HF para alinhar com IMPLEMENTACAO_GRAFICA.md.")


if __name__ == "__main__":
    main()
