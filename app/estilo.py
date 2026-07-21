"""Padrão visual único (PADRÃO GERAL) para todos os gráficos Plotly do dashboard.

Fonte: Especificacoes_graficos_Joao.md + COMPLETA GRÁFICOS.docx (cliente).
Regras: fonte preta (#000000), sem grade de fundo, sem eixo secundário, sem
linha de total, sem rodapé de fonte, título afirma o achado, marcadores de
ER (emendas regimentais) e sombreamento ESPIN idênticos em todos os gráficos
que cruzam essas datas.
"""

from __future__ import annotations
import plotly.graph_objects as go

AZUL = "#2563EB"
AZUL_CLARO = "#93C5FD"
CINZA = "#9CA3AF"
VERDE = "#059669"
ROXO = "#7C3AED"
VERMELHO = "#C00000"
PRETO = "#000000"

COR_PV = AZUL
COR_PP = CINZA
COR_AMBOS = AZUL_CLARO

# Emendas Regimentais: (data em fração ano.mes/12, rótulo)
ER_DATAS = {
    51: (2016, 6, 22),
    52: (2019, 6, 14),
    53: (2020, 3, 18),
}
ESPIN_INICIO = (2020, 2, 3)
ESPIN_FIM = (2022, 4, 22)

AXIS_PADRAO = dict(
    showline=True, linewidth=1.5, linecolor=PRETO,
    showgrid=False, zeroline=False,
    title_font=dict(family="Arial, sans-serif", size=16, color=PRETO),
    tickfont=dict(family="Arial, sans-serif", size=15, color=PRETO, weight="bold"),
    ticks="outside", tickcolor=PRETO,
)

LAYOUT_PADRAO = dict(
    template="plotly_white",
    height=560,
    margin=dict(t=110, b=70, l=60, r=40),
    title_font=dict(family="Arial, sans-serif", size=22, color=PRETO),
    font=dict(family="Arial, sans-serif", color=PRETO),
    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=False,
)

LEGENDA_PADRAO = dict(
    orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
    font=dict(family="Arial, sans-serif", size=14, color=PRETO),
)


def br(v: float, d: int = 0) -> str:
    """Formata número no padrão brasileiro (ponto de milhar, vírgula decimal)."""
    if d == 0:
        return f"{int(round(v)):,}".replace(",", ".")
    s = f"{v:,.{d}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def aplicar_padrao(fig: go.Figure, titulo: str, subtitulo: str | None = None, **layout_kwargs) -> go.Figure:
    """Aplica título/subtítulo em negrito preto e o layout base a `fig`, sem rodapé de fonte."""
    title = f"<b>{titulo}</b>"
    if subtitulo:
        title += f"<br><sup>{subtitulo}</sup>"
    layout = {**LAYOUT_PADRAO, **layout_kwargs}
    fig.update_layout(title=title, **layout)
    fig.update_xaxes(**AXIS_PADRAO)
    fig.update_yaxes(**AXIS_PADRAO)
    return fig


def _frac_ano(ano_base: int, ano: int, mes: int, dia: int) -> float:
    """Posição x fracionária de uma data dentro do eixo categórico de anos (0-indexed a partir de ano_base)."""
    import calendar
    dias_no_mes = calendar.monthrange(ano, mes)[1]
    return (ano - ano_base) + (mes - 1) / 12 + (dia / dias_no_mes) / 12


def add_er_marker(fig: go.Figure, ano_base: int, er: int, y0: float, y1: float, y_label: float) -> go.Figure:
    """Linha vertical preta tracejada + rótulo 'ER n' na data exata da emenda regimental."""
    ano, mes, dia = ER_DATAS[er]
    x = _frac_ano(ano_base, ano, mes, dia)
    fig.add_shape(type="line", x0=x, x1=x, y0=y0, y1=y1,
                  line=dict(color=PRETO, width=1.5, dash="dash"), xref="x", yref="y")
    fig.add_annotation(x=x, y=y_label, text=f"<b>ER {er}</b>", showarrow=False,
                        font=dict(color=PRETO, size=12), xref="x", yref="y")
    return fig


def add_espin_shade(fig: go.Figure, ano_base: int, y0: float, y1: float, y_label: float) -> go.Figure:
    """Sombreamento rosa claro + linhas vermelhas tracejadas + rótulo 'ESPIN' no período da ESPIN."""
    x0 = _frac_ano(ano_base, *ESPIN_INICIO)
    x1 = _frac_ano(ano_base, *ESPIN_FIM)
    fig.add_vrect(x0=x0, x1=x1, fillcolor="#FCE7F3", opacity=0.55, line_width=0, layer="below")
    for x in (x0, x1):
        fig.add_shape(type="line", x0=x, x1=x, y0=y0, y1=y1,
                      line=dict(color=VERMELHO, width=1.5, dash="dash"), xref="x", yref="y")
    fig.add_annotation(x=(x0 + x1) / 2, y=y_label, text="<b>↔ ESPIN</b>", showarrow=False,
                        font=dict(color=VERMELHO, size=12), xref="x", yref="y")
    return fig
