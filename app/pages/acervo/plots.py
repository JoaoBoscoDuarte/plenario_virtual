"""Figuras Plotly para a página de Acervo — função única paramétrica."""

from __future__ import annotations
import plotly.graph_objects as go
import pandas as pd

CORES_CLASSE = {
    "ADI":  "#3498db",
    "ADC":  "#1abc9c",
    "ADO":  "#9b59b6",
    "ADPF": "#e67e22",
}

_LEGEND = dict(
    orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
    font=dict(size=10, color="#333333"),
    bgcolor="#fcfcfc", bordercolor="#cccccc", borderwidth=1,
)

_MARCOS = [
    ("ER 51/2016", 2016, "purple",  1.15),
    ("ER 52/2019", 2019, "#d9822b", 1.08),
    ("ER 53/2020", 2020, "red",     1.00),
]


def _add_marcos(fig: go.Figure, max_y: float) -> None:
    """Adiciona ESPIN e linhas ER ao gráfico."""
    fig.add_vrect(x0=2020, x1=2022, fillcolor="green", opacity=0.08, layer="below", line_width=0)
    # ESPIN: centralizado no topo da zona sombreada, usando yref="paper"
    fig.add_annotation(
        x=2021, y=0.98, yref="paper", text="<b>ESPIN</b>", showarrow=False,
        xanchor="center", yanchor="top", font=dict(color="green", size=9),
    )
    for label, x, color, mult in _MARCOS:
        h = max_y * mult
        fig.add_shape(type="line", x0=x, x1=x, y0=0, y1=h,
                      line=dict(color=color, width=1.2, dash="dash"))
        fig.add_annotation(x=x, y=h, text=label.split("/")[0], showarrow=False,
                           xanchor="center", yanchor="bottom",
                           font=dict(color=color, size=9))

    # Traces fake para legenda
    for label, _, color, _ in _MARCOS:
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines",
                                 line=dict(color=color, width=1.5, dash="dash"),
                                 name=label))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
                             marker=dict(color="green", symbol="square", size=12, opacity=0.2),
                             name="Período da ESPIN (Portaria GM/MS nº 186/2020 e nº 913/2020)"))


def plotar_grafico_stf(
    df: pd.DataFrame,
    classe_nome: str,
    coluna_metrica: str,
    label_metrica: str,
    show_values: bool = False,
) -> go.Figure:
    """
    Função única de plotagem paramétrica.

    - classe_nome="TOTAL": barras do agregado geral, eixo único.
    - classe_nome=<classe>: barras da classe (eixo esquerdo) +
      linha do total geral (eixo direito).
    """
    df_total = df.groupby("ano", as_index=False)[coluna_metrica].sum()
    is_total = classe_nome.upper() == "TOTAL"

    fig = go.Figure()

    if is_total:
        fig.set_subplots(specs=[[{"secondary_y": False}]])
        max_y = float(df_total[coluna_metrica].max() or 1)

        fig.add_trace(go.Bar(
            x=df_total["ano"],
            y=df_total[coluna_metrica],
            marker_color="#3498db",
            text=df_total[coluna_metrica] if show_values else None,
            textposition="outside",
            cliponaxis=False,
            name=f"Total Geral ({label_metrica})",
        ))
    else:
        fig.set_subplots(specs=[[{"secondary_y": True}]])
        df_classe = df[df["classe"] == classe_nome]
        max_y = float(df_classe[coluna_metrica].max() or 1)

        # Linha do total geral no eixo secundário
        fig.add_trace(go.Scatter(
            x=df_total["ano"],
            y=df_total[coluna_metrica],
            mode="lines+markers",
            line=dict(color="#7f7f7f", width=2),
            marker=dict(size=4),
            name=f"Total Geral ({label_metrica})",
        ), secondary_y=True)

        # Barras da classe no eixo primário
        fig.add_trace(go.Bar(
            x=df_classe["ano"],
            y=df_classe[coluna_metrica],
            marker_color=CORES_CLASSE.get(classe_nome, "#3498db"),
            text=df_classe[coluna_metrica] if show_values else None,
            textposition="outside",
            cliponaxis=False,
            name=f"Classe: {classe_nome}",
        ), secondary_y=False)

    _add_marcos(fig, max_y)

    titulo_peca = "Total Geral" if is_total else f"Classe {classe_nome}"
    fig.update_layout(
        title_text=f"Evolução Anual — {titulo_peca} ({label_metrica})",
        template="plotly_white",
        height=600,
        margin=dict(t=140, b=100, l=60, r=60),
        legend=_LEGEND,
        uniformtext_minsize=8,
        uniformtext_mode="hide",
    )
    fig.update_xaxes(
        dtick=1,
        title_text="Ano de Referência",
        tickangle=-45,
        range=[1987.5, 2025.5],
    )

    if is_total:
        fig.update_yaxes(title_text=f"Quantidade — {label_metrica}")
    else:
        fig.update_yaxes(title_text=f"{label_metrica} da Classe (Barras)", secondary_y=False)
        fig.update_yaxes(title_text=f"Total Geral do Tribunal (Linha)", secondary_y=True)

    return fig
