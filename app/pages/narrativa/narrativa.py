"""Página: Gráficos de Narrativa."""

from __future__ import annotations
import streamlit as st
from pages.narrativa.layout import render_graficos

st.title("Gráficos de Narrativa")
st.markdown("""
Seis gráficos que sintetizam os principais achados sobre a relação entre o **Plenário Virtual**
e o **Plenário Presencial** no STF (2020–2025). Dados do portal de transparência do STF,
elaboração própria.
""")

st.markdown("---")
render_graficos()
