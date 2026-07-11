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
        "Visão Geral": [
            st.Page("pages/geral/geral.py", title="Visão Geral", icon="📊"),
        ],
    }
)

pg.run()
