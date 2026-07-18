"""Tema claro/escuro. Funções retornam dicts de estilo conforme st.session_state.tema."""

from __future__ import annotations
import streamlit as st


def is_dark() -> bool:
    return st.session_state.get("tema", "claro") == "escuro"


def _cor_base():
    return "white" if is_dark() else "black"


def _cor_grid():
    return "#444" if is_dark() else "#d0d0d0"


def _templ():
    return "plotly_dark" if is_dark() else "plotly_white"


def _font(family="Arial, sans-serif", size=17) -> dict:
    return dict(family=family, size=size, color=_cor_base())


def _cores_cinza() -> str:
    return "#555" if is_dark() else "#e5e7eb"


# ── Styling dicts ─────────────────────────────────────────────────────────────

def get_legend() -> dict:
    return dict(
        orientation="h", yanchor="top", y=-0.2,
        xanchor="center", x=0.5,
        font=_font(17),
    )


def get_layout() -> dict:
    return dict(
        template=_templ(), height=700,
        margin=dict(t=130, b=140, l=120, r=60),
        legend=get_legend(),
        title_font=_font(26),
    )


def get_axis() -> dict:
    return dict(
        showline=True, linewidth=2, linecolor=_cor_base(),
        showgrid=True, gridwidth=1, gridcolor=_cor_grid(),
        title_font=_font(18),
        tickfont=_font(17),
    )


def get_bar_textfont() -> dict:
    return _font(17)


def get_pizza_textfont() -> dict:
    return _font(14)


def get_pizza_layout() -> dict:
    return dict(
        template=_templ(), height=500,
        margin=dict(t=120, b=100, l=60, r=60),
        showlegend=True,
        title_font=_font(26),
        legend=dict(
            orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5,
            font=_font(17),
        ),
    )


def get_layout_bar() -> dict:
    return dict(
        template=_templ(), height=500,
        margin=dict(t=120, b=80, l=60, r=60),
        legend=get_legend(),
        title_font=_font(26),
        xaxis=dict(dtick=1, title="Ano", tickangle=-45,
                   title_font=_font(18),
                   tickfont=_font(17),
                   showline=True, linewidth=2, linecolor=_cor_base(),
                   showgrid=True, gridwidth=1, gridcolor=_cor_grid()),
        yaxis=dict(title="Inclusões com reajuste de voto",
                   title_font=_font(18),
                   tickfont=_font(17),
                   showline=True, linewidth=2, linecolor=_cor_base(),
                   showgrid=True, gridwidth=1, gridcolor=_cor_grid()),
    )


def get_pizza_title_font() -> dict:
    return _font(18)


# ── Cores temáticas ──────────────────────────────────────────────────────────

def get_cores_reajuste() -> dict:
    return {
        "Com reajuste de voto": "#dc2626",
        "Sem reajuste de voto": _cores_cinza(),
    }


def get_cores_sust() -> dict:
    return {
        "Com sustentação oral": "#0891b2",
        "Sem sustentação oral": _cores_cinza(),
    }


def get_cores_tram() -> dict:
    return {
        "Ambos os ambientes": "#8b5cf6",
        "Só Virtual":         "#2563eb",
        "Só Físico":          "#f59e0b",
    }


# ── UI helper ────────────────────────────────────────────────────────────────

def render_toggle() -> None:
    """Renderiza toggle de tema no sidebar. Retorna None; lê de session_state."""
    atual = st.session_state.get("tema", "claro")
    opcoes = ["claro", "escuro"]
    idx = opcoes.index(atual) if atual in opcoes else 0
    st.selectbox("🌓 Tema", opcoes, index=idx, key="tema",
                 format_func=lambda v: "☀️ Claro" if v == "claro" else "🌙 Escuro")
    # ── CSS para Streamlit ──────────────────────────────────
    if is_dark():
        st.markdown("""
        <style>
        .stApp { background-color: #0e1117; color: #fafafa; }
        .stSelectbox label, .stCheckbox label, .stMarkdown, h1, h2, h3, h4, h5, h6 { color: #fafafa !important; }
        .st-bw { background-color: #1e1e1e; }
        </style>
        """, unsafe_allow_html=True)
