"""Página: Tramitação por Ambiente."""

import sys
from pathlib import Path

import streamlit as st

_here = Path(__file__).resolve()
_root = _here.parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from dados.loader import load_tramitacoes
from pages.tramitacao.layout import render_graficos

try:
    df = load_tramitacoes()
except Exception as e:
    st.error(f"Erro ao carregar dataset: {e}")
    st.stop()

if df.empty:
    st.warning("O dataframe retornou vazio.")
    st.stop()

st.title("Tramitação por Ambiente")
st.markdown("""
Esta seção analisa em quais **ambientes de julgamento** os processos de Controle Concentrado
(ADI, ADC, ADO e ADPF) tramitaram entre **2020 e 2025**.

Os processos podem ter sido julgados exclusivamente no **Plenário Virtual** (PV), exclusivamente
no **Plenário Físico** (PP), ou em **ambos os ambientes** em inclusões distintas. A análise
cruza essa dimensão com classe processual, tipo de questão, desfecho e taxa de conclusão.

O objetivo é revelar como o ambiente de julgamento se relaciona com o perfil dos processos
e com os resultados das sessões.
""")

st.markdown("""
**Nesta seção:**
- **Tabulador Interativo** — configure livremente os eixos e a métrica para explorar qualquer combinação de dimensões.
- **T1 — Distribuição Geral** — pizza com a proporção de processos por ambiente (só PV / só PP / ambos).
- **T2 — Tramitação × Classe** — volume de processos por ambiente e classe processual.
- **T3 — Tramitação × Tipo de Questão** — volume de processos por ambiente e tipo (PR / RC / QI).
- **T4 — Ambos os Ambientes × Tipo** — recorte dos processos que passaram pelos dois ambientes.
- **T5 — Macro-Desfecho × Ambiente** — inclusões concluídas e não concluídas por ambiente.
- **T6 — Desfecho Detalhado × Ambiente** — os 7 desfechos possíveis por ambiente.
- **T7 — Classe dentro de cada Ambiente** — composição por classe em cada grupo de tramitação.
- **T8 — Tipo de Questão dentro de cada Ambiente** — composição por tipo em cada grupo.
- **T9 — Taxa de Conclusão (%)** — percentual de inclusões concluídas por ambiente e classe.
- **Tabela Consolidada** — dados brutos por processo com contagem de inclusões por ambiente.
""")

render_graficos(df)
