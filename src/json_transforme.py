"""
Pure library module for exploding JSON list columns from the STF raw dataset
and deriving useful flags (virtual/presencial, unanimidade, tipo de órgão, etc.).

This file must contain **only** pure, side-effect free functions and constants.
No execution code, no CLI, no prints, no path logic.

Orchestration and the user-facing CLI entrypoint live in `src/cleaning.py`.
"""

import ast
import re
import json
import pandas as pd

# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────

STR_NULOS = {'NA', 'N/A', 'na', 'n/a', 'null', 'NULL', 'None', 'none', ''}

TERMOS_VIRTUAL = (
    'plenário virtual|pauta virtual|julgamento virtual|'
    'incluído em pauta virtual|retirado de pauta virtual'
)

TERMOS_UNANIME = 'por votação unânime|unanimidade'

TERMOS_MAIORIA = 'por maioria de votos|por maioria'

TERMOS_PLENO   = 'pleno|plenário'
TERMOS_TURMA   = 'primeira turma|segunda turma'
TERMOS_MONO    = 'monocrática|monocratico|decisão individual'


# ─────────────────────────────────────────────
# FUNÇÃO BASE — parser robusto
# ─────────────────────────────────────────────

def explodir_json(
    df: pd.DataFrame,
    coluna: str,
    prefixo: str,
    colunas_contexto: list = None
) -> pd.DataFrame:
    """
    Transforma uma coluna de JSON aninhado em DataFrame normalizado.

    Parâmetros
    ----------
    df               : DataFrame principal
    coluna           : nome da coluna com JSON string
    prefixo          : prefixo aplicado às colunas do JSON (ex: 'and_')
    colunas_contexto : colunas do df principal a incluir em cada linha
    """
    if colunas_contexto is None:
        colunas_contexto = ['incidente', 'classe', 'tipo_processo']

    registros = []
    erros = []

    for _, row in df.iterrows():
        raw = row[coluna]

        # parser robusto: ignora nulos e strings vazias antes de tentar parsear
        if not isinstance(raw, str) or raw.strip() in ('', '[]', 'nan', 'None'):
            continue

        try:
            itens = ast.literal_eval(raw)

            if not isinstance(itens, list):
                continue

            for item in itens:
                entrada = {col: row[col] for col in colunas_contexto}

                for k, v in item.items():
                    # 'NA' string e variantes → None real
                    v_clean = None if (isinstance(v, str) and v.strip() in STR_NULOS) else v
                    # string vazia → None
                    v_clean = None if v_clean == '' else v_clean
                    entrada[f'{prefixo}{k}'] = v_clean

                registros.append(entrada)

        except Exception as e:
            erros.append({
                'incidente': row.get('incidente'),
                'coluna': coluna,
                'erro': str(e),
                'valor': str(raw)[:100]   # primeiros 100 chars para debug
            })

    if erros:
        print(f'[{coluna}] {len(erros)} erros de parsing:')
        for e in erros[:5]:
            print(f"  incidente {e['incidente']}: {e['erro']}")
            print(f"  valor: {e['valor']}")

    return pd.DataFrame(registros)


# ─────────────────────────────────────────────
# ANDAMENTOS
# ─────────────────────────────────────────────

def processar_andamentos(proc: pd.DataFrame) -> pd.DataFrame:
    df_andamentos = explodir_json(proc, 'andamentos_lista', 'and_')

    # tipos
    df_andamentos['and_data'] = pd.to_datetime(
        df_andamentos['and_data'], format='%d/%m/%Y', errors='coerce'
    )
    df_andamentos['and_index'] = pd.to_numeric(
        df_andamentos['and_index'], errors='coerce'
    ).astype('Int64')

    # flag virtual — str.contains vetorizado no lugar de apply(is_virtual)
    nome_virtual = df_andamentos['and_nome'].str.contains(
        TERMOS_VIRTUAL, case=False, na=False
    )
    comp_virtual = df_andamentos['and_complemento'].str.contains(
        TERMOS_VIRTUAL, case=False, na=False
    )
    df_andamentos['and_is_virtual'] = nome_virtual | comp_virtual

    # ordenação cronológica para reconstrução da linha do tempo
    df_andamentos = df_andamentos.sort_values(
        ['incidente', 'and_data', 'and_index']
    ).reset_index(drop=True)

    return df_andamentos


# ─────────────────────────────────────────────
# DECISÕES
# ─────────────────────────────────────────────

def processar_decisoes(proc: pd.DataFrame) -> pd.DataFrame:
    df_decisoes = explodir_json(proc, 'decisões', 'dec_')

    # tipos
    df_decisoes['dec_data'] = pd.to_datetime(
        df_decisoes['dec_data'], format='%d/%m/%Y', errors='coerce'
    )
    df_decisoes['dec_index'] = pd.to_numeric(
        df_decisoes['dec_index'], errors='coerce'
    ).astype('Int64')

    # texto unificado para buscas (nome + complemento)
    texto = (
        df_decisoes['dec_nome'].fillna('') + ' ' +
        df_decisoes['dec_complemento'].fillna('')
    ).str.lower()

    # flag: decisão virtual
    df_decisoes['dec_virtual'] = texto.str.contains(
        TERMOS_VIRTUAL, case=False, na=False
    )

    # flag: unanimidade
    df_decisoes['dec_unanime'] = texto.str.contains(
        TERMOS_UNANIME, case=False, na=False
    )

    # flag: maioria
    df_decisoes['dec_maioria'] = texto.str.contains(
        TERMOS_MAIORIA, case=False, na=False
    )

    # tipo de órgão julgador
    def classificar_orgao(t):
        if pd.isna(t) or t.strip() == '':
            return None
        t = t.lower()
        if re.search(TERMOS_MONO, t):
            return 'monocratica'
        if re.search(TERMOS_TURMA, t):
            return 'turma'
        if re.search(TERMOS_PLENO, t):
            return 'pleno'
        return None

    df_decisoes['dec_tipo_orgao'] = (
        df_decisoes['dec_nome'].fillna('') + ' ' +
        df_decisoes['dec_complemento'].fillna('')
    ).apply(classificar_orgao)

    # ordenação cronológica
    df_decisoes = df_decisoes.sort_values(
        ['incidente', 'dec_data', 'dec_index']
    ).reset_index(drop=True)

    return df_decisoes


# ─────────────────────────────────────────────
# DESLOCAMENTOS
# ─────────────────────────────────────────────

def extrair_data_desl(texto):
    """Extrai data no formato DD/MM/AAAA de strings de deslocamento."""
    if pd.isna(texto):
        return None
    match = re.search(r'(\d{2}/\d{2}/\d{4})', str(texto))
    return match.group(1) if match else None


def processar_deslocamentos(proc: pd.DataFrame) -> pd.DataFrame:
    df_deslocamentos = explodir_json(proc, 'deslocamentos_lista', 'desl_')

    for col_data in ['desl_data_recebido', 'desl_enviado']:
        if col_data in df_deslocamentos.columns:
            df_deslocamentos[col_data + '_dt'] = pd.to_datetime(
                df_deslocamentos[col_data].apply(extrair_data_desl),
                format='%d/%m/%Y', errors='coerce'
            )

    return df_deslocamentos


# This module is now a pure library.
# All orchestration / CLI entrypoint logic lives in src/cleaning.py (run_pipeline + its __main__).
# See the approved refactoring plan for rationale.