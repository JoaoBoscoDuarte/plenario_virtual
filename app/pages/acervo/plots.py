"""Figuras Plotly para a página de Acervo."""

from __future__ import annotations
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

_CORES = {"ADI": "#1f77b4", "ADPF": "#ff7f0e", "ADC": "#2ca02c", "ADO": "#d62728"}

_LEGEND = dict(
    orientation="h", yanchor="top", y=-0.40, xanchor="center", x=0.5,
    font=dict(size=10, color="#333333"), bgcolor="#fcfcfc",
    bordercolor="#cccccc", borderwidth=1,
)

_MARCOS = [
    ("ER 51/2016", 2016, "purple", 1.16),
    ("ER 52/2019", 2019, "#d9822b", 1.08),
    ("ER 53/2020", 2020, "red", 1.00),
]


def _add_marcos(fig: go.Figure, use_paper_ref: bool = True, max_y: float = 1.0) -> None:
    """Adiciona ESPIN e linhas ER ao gráfico."""
    fig.add_vrect(x0=2020, x1=2022, fillcolor="green", opacity=0.1, layer="below", line_width=0)

    if use_paper_ref:
        fig.add_annotation(x=2021, y=0.95, yref="paper", text="<b>ESPIN</b>",
                           showarrow=False, xanchor="center", yanchor="top",
                           font=dict(color="green", size=10))
        for label, x, color, y1 in _MARCOS:
            fig.add_shape(type="line", x0=x, x1=x, y0=0, y1=y1,
                          xref="x", yref="paper",
                          line=dict(color=color, width=1.5, dash="dash"))
            fig.add_annotation(x=x, y=y1, yref="paper", text=label,
                               showarrow=False, xanchor="center", yanchor="bottom",
                               font=dict(color=color, size=10))
    else:
        fig.add_annotation(x=2021, y=max_y * 0.95, text="<b>ESPIN</b>",
                           showarrow=False, xanchor="center", yanchor="top",
                           font=dict(color="green", size=9))
        heights = {"ER 51/2016": 1.15, "ER 52/2019": 1.08, "ER 53/2020": 1.00}
        for label, x, color, _ in _MARCOS:
            h = max_y * heights[label]
            fig.add_shape(type="line", x0=x, x1=x, y0=0, y1=h,
                          line=dict(color=color, width=1.2, dash="dash"))
            fig.add_annotation(x=x, y=h, text=label.split("/")[0],
                               showarrow=False, xanchor="center", yanchor="bottom",
                               font=dict(color=color, size=9))

    # Traces fake para a legenda
    for label, _, color, _ in _MARCOS:
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines",
                                 line=dict(color=color, width=1.5, dash="dash"), name=label))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
                             marker=dict(color="green", symbol="square", size=12, opacity=0.2),
                             name="Período da ESPIN (Portaria GM/MS nº 186/2020 e nº 913/2020)"))


def fig_total_ativo_anual(df: pd.DataFrame, show_values: bool = False) -> go.Figure:
    """Barras do acervo ativo total anual com marcos históricos."""
    df_t = df.groupby("ano", as_index=False)["quantidade_ativos"].sum()

    fig = px.bar(df_t, x="ano", y="quantidade_ativos",
                 labels={"ano": "Ano de Referência", "quantidade_ativos": "Processos Ativos"})
    fig.update_traces(
        marker_color="#3498db",
        text=df_t["quantidade_ativos"] if show_values else None,
        textposition="outside",
        cliponaxis=False,
        name="Processos Ativos",
        showlegend=True,
    )

    _add_marcos(fig, use_paper_ref=True)

    fig.update_layout(
        template="plotly_white",
        xaxis=dict(dtick=1, title="Ano de Referência"),
        yaxis=dict(title="Quantidade de Processos Ativos"),
        uniformtext_minsize=8, uniformtext_mode="hide",
        margin=dict(t=140, b=160),
        legend=_LEGEND,
    )
    return fig


def fig_ativo_por_classe(df: pd.DataFrame, classe: str, show_values: bool = False) -> go.Figure:
    """Barras da classe + linha do total geral (eixo secundário) com marcos."""
    df_classe = df[df["classe"] == classe]
    df_geral = df.groupby("ano", as_index=False)["quantidade_ativos"].sum()

    max_y = int(df_classe["quantidade_ativos"].max()) if not df_classe.empty else 1
    if max_y == 0:
        max_y = 1

    fig = go.Figure()
    fig.set_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(
        x=df_geral["ano"], y=df_geral["quantidade_ativos"],
        mode="lines+markers", line=dict(color="#7f7f7f", width=2),
        marker=dict(size=4), name="Acervo Total Geral (STF)",
    ), secondary_y=True)

    fig.add_trace(go.Bar(
        x=df_classe["ano"], y=df_classe["quantidade_ativos"],
        marker_color=_CORES.get(classe, "#4C72B0"),
        text=df_classe["quantidade_ativos"] if show_values else None,
        textposition="outside", cliponaxis=False,
        name=f"Classe: {classe}",
    ), secondary_y=False)

    _add_marcos(fig, use_paper_ref=False, max_y=max_y)

    fig.update_layout(
        template="plotly_white",
        margin=dict(t=120, b=160),
        legend=_LEGEND,
    )
    fig.update_xaxes(dtick=1, title_text="Ano de Referência")
    fig.update_yaxes(title_text="Processos da Classe (Barras)", secondary_y=False)
    fig.update_yaxes(title_text="Acervo Total Geral (Linha)", secondary_y=True)
    return fig
