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
import sys
from pathlib import Path

from huggingface_hub import HfApi

# Ajuste conforme seu usuário / repo no Hugging Face (atualizado)
REPO_ID = os.getenv("HF_REPO", "JoaoBoscoooo/plenario_virtual")

# Mapeamento de arquivos reais no disco -> caminho no HF.
# Só datasets efetivamente lidos pelo dashboard (ver app/dados/loader.py).
FILES = [
    ("arquivosConcatenados.parquet", "processed/arquivosConcatenados.parquet"),
    ("dim_decisoes.parquet", "processed/dim_decisoes.parquet"),
    ("acervo/evolucao_acervo.parquet", "processed/acervo/evolucao_acervo.parquet"),
    ("inclusoes_em_pauta.parquet",  "processed/inclusoes_em_pauta.parquet"),
    ("sessoes_virtuais.parquet",    "processed/sessoes_virtuais.parquet"),
    ("sustentacao_oral.parquet",    "processed/sustentacao_oral.parquet"),
    ("tramitacoes.parquet",         "processed/tramitacoes.parquet"),
]

# Datasets em data/interim/ — subprodutos do star-schema não lidos pelo
# dashboard hoje. Não sobem por padrão (dim_andamentos sozinho é 560MB).
# Passe --interim para publicá-los também (ex: reprocessamento futuro).
INTERIM_FILES = [
    ("dim_andamentos.parquet", "interim/dim_andamentos.parquet"),
    ("dim_deslocamentos.parquet", "interim/dim_deslocamentos.parquet"),
    ("dim_partes.parquet", "interim/dim_partes.parquet"),
    ("reajustes_de_voto.parquet", "interim/reajustes_de_voto.parquet"),
    ("inclusoes_em_pauta_2016_2025.csv", "interim/inclusoes_em_pauta_2016_2025.csv"),
]

# Diretório padrão dos parquets — relativo à raiz do projeto (pai de scripts/)
DEFAULT_PROCESSED = Path(__file__).resolve().parent.parent / "data" / "processed"
DEFAULT_INTERIM = Path(__file__).resolve().parent.parent / "data" / "interim"


def main():
    subir_interim = "--interim" in sys.argv

    token = os.getenv("HF_TOKEN")
    if token:
        api = HfApi(token=token)
        print("Usando token da variável de ambiente HF_TOKEN.")
    else:
        # Usa o token salvo via `hf auth login` (melhor prática atual)
        api = HfApi()
        print("Usando token salvo via `hf auth login` (recomendado).")

    print(f"Subindo datasets para https://huggingface.co/datasets/{REPO_ID}")
    grupos = [(DEFAULT_PROCESSED, FILES)]
    if subir_interim:
        grupos.append((DEFAULT_INTERIM, INTERIM_FILES))

    for base, files in grupos:
        for local_rel, remote_path in files:
            caminho = base / local_rel
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

    if not subir_interim:
        print("\n(datasets de data/interim/ não enviados — use --interim para incluí-los)")
    print("\nConcluído. Atualize o Streamlit Cloud (ou espere o próximo push) para o cache expirar.")
    print("Dica: em produção o cache do Streamlit expira automaticamente em ~1h (ou force reload limpando o @st.cache_data).")


if __name__ == "__main__":
    main()
