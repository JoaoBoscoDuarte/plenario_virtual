"""Página: Sessões Virtuais Iniciadas."""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

_here = Path(__file__).resolve()
_root = _here.parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from dados.loader import load_sessoes_virtuais, load_inclusoes_em_pauta
from pages.sessoes_virtuais.layout import render_graficos

try:
    df_s = load_sessoes_virtuais()
except Exception as e:
    st.error(f"Erro ao carregar dataset de sessões virtuais: {e}")
    st.stop()

if df_s.empty:
    st.warning("O dataframe de sessões virtuais retornou vazio.")
    st.stop()

try:
    df_final = load_inclusoes_em_pauta()
except Exception as e:
    st.warning(f"Não foi possível carregar inclusões em pauta (necessário para Bloco 5): {e}")
    df_final = pd.DataFrame()

# ── Preparação básica (comum a todos os blocos) ──────────────────────────────
df_s = df_s.copy()
df_s["tipo_questao"] = df_s["tipo_questao"].replace({"IJ": "QI"})
df_s["data_sessao_dt"] = pd.to_datetime(df_s["data_sessao_dt"])
df_s["mes"] = df_s["data_sessao_dt"].dt.month
df_s["trimestre"] = df_s["data_sessao_dt"].dt.quarter

if not df_final.empty:
    df_final["ambiente"] = df_final["ambiente"].replace("Plenário Físico", "Plenário Presencial")

# ── Cabeçalho ─────────────────────────────────────────────────────────────────
st.title("Sessões Virtuais")
st.markdown("""
Esta seção analisa as **sessões virtuais iniciadas** no Controle Concentrado
(ADI, ADC, ADO e ADPF) do STF entre **2020 e 2025**.

A unidade de análise é a **sessão virtual** — cada vez que um processo é incluído
em ambiente virtual para julgamento. Um mesmo processo pode ter múltiplas sessões
se foi incluído em momentos distintos.

Os gráficos cobrem cinco dimensões de análise:

- **Sazonalidade** — distribuição mensal e trimestral das sessões.
- **Relator** — volume, taxa de conclusão e perfil dos ministros com maior atividade.
- **Múltiplas sessões** — quantas sessões um mesmo processo tem e como a taxa de
  conclusão varia ao longo delas.
- **Cruzamentos** — interação entre classe processual, tipo de questão e desfecho.
- **Duração** — tempo entre a primeira inclusão em pauta e a conclusão do processo.
""")

st.markdown("---")

render_graficos(df_s, df_final)
