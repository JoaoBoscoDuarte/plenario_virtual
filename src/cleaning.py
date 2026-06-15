"""Full ETL pipeline orchestrator for STF Plenário Virtual data.

This module is the single source of truth for transforming the raw CSV
into the four clean parquet datasets (processos + exploded andamentos/decisoes/deslocamentos).

It can be used:
- As a standalone script: `python -m src.cleaning` (or `python src/cleaning.py`)
- Imported by notebooks (for audit/validation) or by the Streamlit app / other tools.
- In future CI or update scripts.

Design goals (per project specs + user request):
- Notebook-independent: dashboard users never need to open/run notebooks.
- Reproducible and operable.
- Reuses the robust JSON explosion logic from json_transforme.py.
- Extracts the scalar list parsing + main table prep that previously lived only in the ETL notebook.
"""

from __future__ import annotations

import argparse
import ast
import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd

# Internal reuse of the high-quality JSON transformers
from .json_transforme import (
    processar_andamentos,
    processar_decisoes,
    processar_deslocamentos,
)

# ──────────────────────────────────────────────────────────────────────────────
# Paths — robust discovery that works in development, editable install,
# and when the script is run from any CWD.
# We search upwards for the distinctive raw data file.
# ──────────────────────────────────────────────────────────────────────────────

def _discover_root() -> Path:
    """Find the project root by looking for data/raw/ArquivosConcatenados_1.csv
    walking up from CWD and from this file's location. This survives
    `pip install -e .` and different working directories.
    """
    candidates = []

    # Start from current working directory (most common case when user cds into the project)
    cwd = Path.cwd().resolve()
    candidates.extend([cwd] + list(cwd.parents))

    # Also consider the location of this module (helps in some installed scenarios)
    here = Path(__file__).resolve()
    candidates.extend([here] + list(here.parents))

    marker = "ArquivosConcatenados_1.csv"
    for p in candidates:
        candidate = p / "data" / "raw" / marker
        if candidate.exists():
            return p

    # Last resort: fall back to two parents of this file (old behavior)
    return Path(__file__).resolve().parents[2]


DEFAULT_ROOT = _discover_root()
DEFAULT_RAW = DEFAULT_ROOT / "data" / "raw" / "ArquivosConcatenados_1.csv"
DEFAULT_PROCESSED = DEFAULT_ROOT / "data" / "processed"


# ──────────────────────────────────────────────────────────────────────────────
# Scalar list parsers (moved/adapted from notebook 01_limpeza_preprocessing.ipynb)
# ──────────────────────────────────────────────────────────────────────────────

def parse_liminar(valor: Any) -> list[str]:
    """Converte string '["MEDIDA LIMINAR"]' (ou '[]') em lista Python limpa."""
    if pd.isna(valor):
        return []
    
    s = str(valor).strip()
    if s in ("", "[]", "nan", "None", "null"):
        return []
    
    try:
        parsed = ast.literal_eval(s)
        if isinstance(parsed, list):
            return [str(x).strip() for x in parsed if str(x).strip()]
        
        return [str(parsed).strip()] if str(parsed).strip() else []
    
    except Exception:
        return []


def parse_assuntos(valor: Any) -> list[str]:
    """Converte string de lista de assuntos (com separador | e &nbsp;) em lista limpa sem duplicatas."""
    if pd.isna(valor):
        return []
    s = str(valor)

    try:
        # Handle cases that are already proper list strings
        if s.strip().startswith("["):
            parsed = ast.literal_eval(s)

            if isinstance(parsed, list):
                itens = parsed

            else:
                itens = [parsed]
        else:
            itens = [s]

        assuntos: list[str] = []
        for item in itens:

            if not isinstance(item, str):
                item = str(item)
            # remove &nbsp; e espaços extras, split no separador |
            partes = [
                p.strip().replace("\xa0", "").replace("&nbsp;", "")
                for p in item.split("|")
            ]
            partes = [p for p in partes if p]
            assuntos.extend(partes)

        # remove duplicatas mantendo ordem
        return list(dict.fromkeys(assuntos))
    
    except Exception:
        return []


# ──────────────────────────────────────────────────────────────────────────────
# Core preparation for the main "processos" table (denormalized scalar view)
# ──────────────────────────────────────────────────────────────────────────────

def prepare_processos_base(raw: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara a tabela principal de processos (processos.parquet).

    - Aplica parsers para liminar, assuntos, partes (se presentes).
    - Converte data_protocolo para datetime (dayfirst).
    - Remove colunas de listas JSON brutas (já exportadas nos arquivos explodidos).
    - Serializa colunas de lista restantes para JSON string (parquet não suporta listas nativas).
    - Mantém o schema estável e limpo para uso no dashboard e análises.
    """
    proc = raw.copy()

    # Parse de campos de lista (liminar e assuntos)
    if "liminar" in proc.columns:
        proc["liminar_lista"] = proc["liminar"].apply(parse_liminar)
        proc["tem_liminar"] = proc["liminar_lista"].apply(lambda x: len(x) > 0)

    if "lista_assuntos" in proc.columns:
        proc["assuntos_lista"] = proc["lista_assuntos"].apply(parse_assuntos)
        # assunto_principal para filtros rápidos (primeiro da lista quando existir)
        proc["assunto_principal"] = proc["assuntos_lista"].apply(
            lambda x: x[0] if isinstance(x, list) and x else None
        )

    # Partes já vêm como JSON string; garantir lista onde possível (para consistência)
    if "partes_total" in proc.columns:
        def _safe_parse_partes(v):
            if pd.isna(v) or str(v).strip() in ("", "[]"):
                return []
            try:
                p = ast.literal_eval(str(v))
                return p if isinstance(p, list) else []
            except Exception:
                return []
        proc["partes_total"] = proc["partes_total"].apply(_safe_parse_partes)

    # Conversão de data (o notebook usava dayfirst + low_memory no read)
    if "data_protocolo" in proc.columns:
        proc["data_protocolo"] = pd.to_datetime(
            proc["data_protocolo"], dayfirst=True, errors="coerce"
        )

    # Colunas a remover: as listas JSON originais + originais substituídas por versões limpas
    COLUNAS_REMOVER = [
        "andamentos_lista",
        "decisões",            # note: original column name has accent
        "deslocamentos_lista",
        "liminar",             # substituída por liminar_lista + tem_liminar
        "lista_assuntos",      # substituída por assuntos_lista + assunto_principal
    ]

    proc = proc.drop(columns=[c for c in COLUNAS_REMOVER if c in proc.columns], errors="ignore")

    # Garantir que qualquer coluna de lista remanescente seja serializada como JSON string
    # (parquet compatibility — exactly as done in the notebook export cell)
    list_cols = [c for c in proc.columns if proc[c].apply(lambda x: isinstance(x, (list, dict))).any()]
    for col in list_cols:
        proc[col] = proc[col].apply(
            lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, (list, dict)) else x
        )

    # Ordenação estável por incidente (útil para joins posteriores)
    if "incidente" in proc.columns:
        proc = proc.sort_values("incidente").reset_index(drop=True)

    return proc


# ──────────────────────────────────────────────────────────────────────────────
# Validation (moved from notebook validation cell for single source of truth)
# ──────────────────────────────────────────────────────────────────────────────

def _run_validations(
    processos: pd.DataFrame,
    andamentos: pd.DataFrame,
    decisoes: pd.DataFrame,
    deslocamentos: pd.DataFrame,
) -> None:
    print("=== VALIDAÇÕES ===")

    dupl = processos["incidente"].duplicated().sum() if "incidente" in processos.columns else 0
    print(f"Incidentes duplicados: {dupl}  {'✓' if dupl == 0 else '⚠️ VERIFICAR'}")

    if "data_protocolo" in processos.columns:
        fora = processos[
            (processos["data_protocolo"].dt.year < 1988) |
            (processos["data_protocolo"].dt.year > 2026)
        ]
        print(f"Datas fora do range 1988–2026: {len(fora)}  {'✓' if len(fora) == 0 else '⚠️ VERIFICAR'}")

    classes_ok = set(processos.get("classe", pd.Series()).dropna().unique()) <= {"ADI", "ADC", "ADO", "ADPF"}
    print(f"Apenas classes ADI/ADC/ADO/ADPF: {'✓' if classes_ok else '⚠️ VERIFICAR'}")
    print(f"Classes encontradas: {sorted(processos.get('classe', pd.Series()).dropna().unique().tolist())}")

    tipos_ok = set(processos.get("tipo_processo", pd.Series()).dropna().unique()) <= {"Físico", "Eletrônico"}
    print(f"Apenas Físico/Eletrônico: {'✓' if tipos_ok else '⚠️ VERIFICAR'}")

    print(f"\nTotal andamentos extraídos: {len(andamentos)}")
    print(f"Total decisões extraídas:   {len(decisoes)}")
    print(f"Total deslocamentos:        {len(deslocamentos)}")


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def load_raw_csv(raw_path: Path | str | None = None) -> pd.DataFrame:
    """Carrega o CSV bruto com configurações consistentes (dayfirst, low_memory)."""
    path = Path(raw_path) if raw_path else DEFAULT_RAW
    if not path.exists():
        raise FileNotFoundError(f"Raw file not found: {path}")
    return pd.read_csv(path, dayfirst=True, low_memory=True)


def run_pipeline(
    raw_path: Path | str | None = None,
    processed_dir: Path | str | None = None,
    validate: bool = True,
) -> dict[str, pd.DataFrame]:
    """
    Executa o pipeline completo: raw → 4 datasets processados em parquet.

    Retorna dict com os DataFrames gerados (para uso em notebooks/tests).
    Os arquivos são sempre escritos em disco (parquet).
    """
    raw_p = Path(raw_path) if raw_path else DEFAULT_RAW
    out_dir = Path(processed_dir) if processed_dir else DEFAULT_PROCESSED
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Carregando raw: {raw_p}")
    proc = load_raw_csv(raw_p)

    print("Preparando tabela base de processos (processos.parquet)...")
    df_processos = prepare_processos_base(proc)

    print("Processando andamentos (explosão + flags de virtual)...")
    df_and = processar_andamentos(proc)
    print(f"  → {len(df_and)} andamentos | virtuais: {df_and.get('and_is_virtual', pd.Series()).sum()}")

    print("Processando decisões (explosão + virtual/unanime/orgao)...")
    df_dec = processar_decisoes(proc)
    print(
        f"  → {len(df_dec)} decisões | "
        f"virtuais: {df_dec.get('dec_virtual', pd.Series()).sum()} | "
        f"unânimes: {df_dec.get('dec_unanime', pd.Series()).sum()}"
    )

    print("Processando deslocamentos (explosão + datas)...")
    df_desl = processar_deslocamentos(proc)
    print(f"  → {len(df_desl)} deslocamentos")

    if validate:
        _run_validations(df_processos, df_and, df_dec, df_desl)

    # Export seguro (evita o ArrowKeyError de period extension visto no notebook)
    # Converter qualquer coluna Period para string antes de salvar
    for df in (df_processos, df_and, df_dec, df_desl):
        for col in df.columns:
            if pd.api.types.is_period_dtype(df[col]):
                df[col] = df[col].astype(str)

    print("\nExportando parquets...")
    df_processos.to_parquet(out_dir / "processos.parquet", index=False, engine="pyarrow")
    df_and.to_parquet(out_dir / "andamentos.parquet", index=False, engine="pyarrow")
    df_dec.to_parquet(out_dir / "decisoes.parquet", index=False, engine="pyarrow")
    df_desl.to_parquet(out_dir / "deslocamentos.parquet", index=False, engine="pyarrow")

    for f in sorted(out_dir.glob("*.parquet")):
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"  {f.name}: {size_mb:.2f} MB")

    print("\nConcluído. Pipeline executado com sucesso.")
    return {
        "processos": df_processos,
        "andamentos": df_and,
        "decisoes": df_dec,
        "deslocamentos": df_desl,
    }


# ──────────────────────────────────────────────────────────────────────────────
# CLI entrypoint
# ──────────────────────────────────────────────────────────────────────────────

def _cli():
    parser = argparse.ArgumentParser(description="Run STF Plenário Virtual ETL pipeline.")
    parser.add_argument("--raw", type=str, default=None, help="Path to raw CSV (default: data/raw/ArquivosConcatenados_1.csv)")
    parser.add_argument("--out", type=str, default=None, help="Output directory for parquets (default: data/processed)")
    parser.add_argument("--no-validate", action="store_true", help="Skip post-processing validations")
    args = parser.parse_args()

    run_pipeline(
        raw_path=args.raw,
        processed_dir=args.out,
        validate=not args.no_validate,
    )


if __name__ == "__main__":
    # When users do `python -m src.cleaning` after `pip install -e .` they may see
    # a RuntimeWarning about src.cleaning. Prefer the console script `stf-etl`
    # (installed via pyproject.toml) for the cleanest experience.
    _cli()
