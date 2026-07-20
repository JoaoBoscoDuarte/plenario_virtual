import sys
import streamlit as st

from pathlib import Path

st.set_page_config(layout="wide")

# ── Path setup ───────────────────────────────────────────────────────────────
_root = Path(__file__).resolve().parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

# ── Navegação ────────────────────────────────────────────────────────────────
pg = st.navigation(
    {
        "Acervo": [
            st.Page("pages/acervo/acervo.py", title="Acervo Histórico", icon="📦"),
        ],
        "Inclusões em Pauta": [
            st.Page("pages/inclusoes/inclusoes.py", title="Inclusões em Pauta", icon="📅"),
        ],
        "Reajuste de Voto": [
            st.Page("pages/reajuste/reajuste.py", title="Reajuste de Voto", icon="🔄"),
        ],
        "Tramitação": [
            st.Page("pages/tramitacao/tramitacao.py", title="Tramitação por Ambiente", icon="🔀"),
        ],
        "Sustentação Oral": [
            st.Page("pages/sustentacao/sustentacao.py", title="Sustentação Oral", icon="🎤"),
        ],
        "Visão Geral": [
            st.Page("pages/geral/geral.py", title="Visão Geral", icon="📊"),
        ],
        "Narrativa": [
            st.Page("pages/narrativa/narrativa.py", title="Gráficos Narrativa", icon="📈"),
        ],
    }
)

pg.run()
