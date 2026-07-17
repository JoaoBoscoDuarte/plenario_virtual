import os

HF_REPO_ID = os.getenv("HF_REPO", "JoaoBoscoooo/plenario_virtual")

HF_FILES = {
    "evolucao_acervo":    "processed/acervo/evolucao_acervo.parquet",
    "inclusoes_em_pauta": "processed/inclusoes_em_pauta.parquet",
    "sustentacao_oral":   "processed/sustentacao_oral.parquet",
    "tramitacoes":        "processed/tramitacoes.parquet",
    "reajustes_de_voto":  "processed/reajustes_de_voto.parquet",
    "sessoes_virtuais":   "processed/sessoes_virtuais.parquet",
}
