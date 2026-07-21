"""Figuras Plotly para a página de Acervo — função única paramétrica."""

from __future__ import annotations
import plotly.graph_objects as go
import pandas as pd

from estilo import aplicar_padrao, add_er_marker, add_espin_shade, br, AZUL, AZUL_CLARO, CINZA, VERDE, ROXO, VERMELHO

CORES_CLASSE = {
    "ADI":  "#3498db",
    "ADC":  "#1abc9c",
    "ADO":  "#9b59b6",
    "ADPF": "#e67e22",
}

# Altura vertical (fração do topo) de cada rótulo ER, para não sobrepor.
_ER_Y_MULT = {51: 1.15, 52: 1.08, 53: 1.00}


def plotar_grafico_stf(
    df: pd.DataFrame,
    classe_nome: str,
    coluna_metrica: str,
    label_metrica: str,
    show_values: bool = False,
) -> go.Figure:
    """
    Função única de plotagem paramétrica.

    - classe_nome="TOTAL": barras do agregado geral.
    - classe_nome=<classe>: barras da classe (sem linha de total sobreposta,
      per PADRÃO GERAL — sem eixo secundário, sem linha de tendência de total).
    """
    is_total = classe_nome.upper() == "TOTAL"

    if is_total:
        d = df.groupby("ano", as_index=False)[coluna_metrica].sum()
        cor = AZUL
        nome = f"TOTAL GERAL ({label_metrica.upper()})"
    else:
        d = df[df["classe"] == classe_nome]
        cor = CORES_CLASSE.get(classe_nome, AZUL)
        nome = f"CLASSE: {classe_nome.upper()}"

    max_y = float(d[coluna_metrica].max() or 1)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=d["ano"],
        y=d[coluna_metrica],
        marker_color=cor,
        text=d[coluna_metrica] if show_values else None,
        textposition="outside",
        cliponaxis=False,
        name=nome,
    ))

    y_top = max_y * 1.25
    add_espin_shade(fig, ano_base=0, y0=0, y1=y_top, y_label=max_y * 1.18)
    for er, mult in _ER_Y_MULT.items():
        add_er_marker(fig, ano_base=0, er=er, y0=0, y1=y_top, y_label=max_y * mult)

    titulo_peca = "Total Geral" if is_total else f"Classe {classe_nome}"
    titulo = f"Evolução anual do acervo do STF — {titulo_peca}"
    subtitulo = f"{label_metrica}, por ano de referência (1988–2025)"

    aplicar_padrao(
        fig, titulo, subtitulo,
        height=600,
        margin=dict(t=140, b=100, l=60, r=60),
        uniformtext_minsize=8,
        uniformtext_mode="hide",
    )
    fig.update_xaxes(
        dtick=1,
        title_text="Ano de Referência",
        tickangle=-45,
        range=[1987.5, 2025.5],
    )
    fig.update_yaxes(title_text=label_metrica)

    return fig
