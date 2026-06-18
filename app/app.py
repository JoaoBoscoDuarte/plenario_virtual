import sys
import streamlit as st
import bootstrap

from data import load_parquet
from pathlib import Path

_root = Path(__file__).resolve().parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

st.set_page_config(
    page_title="Dashboard - Análise plenário virtual",
    layout="wide",
    page_icon="⚖️",
    initial_sidebar_state="expanded"
)

st.title("Dashboard - Análise plenário virtual")
st.markdown("Selecione uma área de análise no menu lateral.")