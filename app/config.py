import os

HF_REPO_ID = os.getenv("HF_REPO", "JoaoBoscoooo/plenario_virtual")

HF_FILES = {
    "evolucao_acervo":      "processed/acervo/evolucao_acervo.parquet",
    "inclusoes_em_pauta":  "processed/inclusoes_em_pauta.parquet",
    "inclusoes_com_pauta": "processed/inclusoes_com_pauta.parquet",
}
