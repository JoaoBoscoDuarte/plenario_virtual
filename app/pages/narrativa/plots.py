"""Plotly figures for narrative graphics NA–NF.

Values hardcoded per verification against inclusoes_em_pauta_mestre.parquet.
ponytail: hardcoded — compute from parquet if underlying data changes.
"""

from __future__ import annotations
import plotly.graph_objects as go

COR_PV = '#2563eb'
COR_PP = '#94a3b8'
COR_AMBOS = '#93C5FD'
COR_ESPIN = '#dc2626'

_AXIS = dict(
    showline=True, linewidth=2, linecolor="black",
    showgrid=True, gridwidth=1, gridcolor="#d0d0d0",
    title_font=dict(family="Arial, sans-serif", size=18, color="black"),
    tickfont=dict(family="Arial, sans-serif", size=17, color="black"),
)

_LAYOUT_BASE = dict(
    template="plotly_white", height=500,
    margin=dict(t=130, b=80, l=60, r=60),
    title_font=dict(family="Arial, sans-serif", size=26, color="black"),
    hovermode="x unified",
)


def plot_na() -> go.Figure:
    anos = ['2020', '2021', '2022', '2023', '2024', '2025']
    valores = [59.8, 68.0, 64.1, 66.8, 59.0, 66.6]

    fig = go.Figure(data=[
        go.Bar(x=anos, y=valores, marker_color=COR_PV,
               text=[f'{v}%' for v in valores], textposition='outside',
               cliponaxis=False, showlegend=False)
    ])

    fig.add_shape(type="line", x0=2.33, x1=2.33, y0=0, y1=85,
                  line=dict(color=COR_ESPIN, width=2, dash="dash"),
                  xref="x", yref="y")
    fig.add_annotation(x=2.33, y=80, text="fim da ESPIN (abril de 2022)",
                       showarrow=False, font=dict(color=COR_ESPIN, size=14),
                       xref="x", yref="y")

    fig.update_layout(
        title="<b>A participação do Plenário Virtual mantém-se entre 59% e 68% ao ano</b><br><sup>Percentual das inclusões em pauta destinadas ao ambiente virtual, 2020-2025</sup>",
        yaxis=dict(range=[0, 85], title="%"),
        xaxis=dict(title="Ano"),
        **_LAYOUT_BASE,
    )
    fig.update_xaxes(**_AXIS)
    fig.update_yaxes(**_AXIS)
    return fig


def plot_nb() -> go.Figure:
    categorias = ['Participação na pauta', 'Participação nos julgamentos concluídos']
    valores = [63.9, 91.3]

    fig = go.Figure(data=[
        go.Bar(x=categorias, y=valores, marker_color=COR_PV,
               text=[f'{v}%' for v in valores], textposition='outside',
               cliponaxis=False, showlegend=False)
    ])

    fig.update_layout(
        title="<b>O Plenário Virtual concentra os julgamentos concluídos</b><br><sup>Participação do ambiente virtual na pauta e nos 3.187 julgamentos concluídos, 2020-2025</sup>",
        yaxis=dict(range=[0, 110], title="%"),
        xaxis=dict(title=""),
        **_LAYOUT_BASE,
    )
    fig.update_xaxes(**_AXIS)
    fig.update_yaxes(**_AXIS)
    return fig


def plot_nc() -> go.Figure:
    categorias = ['Somente Plenário Presencial', 'Ambos os ambientes', 'Somente Plenário Virtual']
    valores = [5.6, 16.9, 77.5]
    processos = [159, 478, 2197]
    cores = [COR_PP, COR_AMBOS, COR_PV]
    textos = [f'{v}%  ({p} processos)' for v, p in zip(valores, processos)]

    fig = go.Figure(data=[
        go.Bar(y=categorias, x=valores, orientation='h', marker_color=cores,
               text=textos, textposition='outside', cliponaxis=False,
               showlegend=False)
    ])

    fig.update_layout(
        title="<b>Três de cada quatro processos nunca passam pelo Plenário Presencial</b><br><sup>Tramitação em pauta dos 2.834 processos de controle concentrado, 2020-2025</sup>",
        xaxis=dict(range=[0, 110], title="%"),
        yaxis=dict(title=""),
        **_LAYOUT_BASE,
    )
    fig.update_xaxes(**_AXIS)
    fig.update_yaxes(**_AXIS)
    return fig


def plot_nd() -> go.Figure:
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=['Recursos'], x=[94.3], name='Plenário Virtual', orientation='h',
        marker_color=COR_PV,
        text="Plenário Virtual: 94,3% (1.048 recursos)",
        textposition='inside', insidetextanchor='middle',
    ))

    fig.add_trace(go.Bar(
        y=['Recursos'], x=[5.7], name='Plenário Presencial', orientation='h',
        marker_color=COR_PP,
        text="PP: 5,7% (63)", textposition='outside',
    ))

    fig.update_layout(
        title="<b>A atividade recursal migrou quase integralmente para o ambiente virtual</b><br><sup>Destino das 1.111 inclusões em pauta de recursos (AgR, ED e afins), 2020-2025</sup>",
        barmode='stack',
        xaxis=dict(title="%"),
        yaxis=dict(title=""),
        showlegend=False,
        **_LAYOUT_BASE,
    )
    fig.update_xaxes(**_AXIS)
    fig.update_yaxes(**_AXIS)
    return fig


def plot_ne() -> go.Figure:
    categorias = ['Plenário Virtual', 'Plenário Presencial']
    valores = [1.8, 4.3]
    cores = [COR_PV, COR_PP]

    fig = go.Figure(data=[
        go.Bar(x=categorias, y=valores, marker_color=cores,
               text=[str(v).replace('.', ',') for v in valores],
               textposition='outside', cliponaxis=False, showlegend=False)
    ])

    fig.update_layout(
        title="<b>Cada julgamento presencial consome mais que o dobro de inclusões em pauta</b><br><sup>Média de inclusões em pauta por processo em cada ambiente, 2020-2025</sup>",
        yaxis=dict(range=[0, 5.5], title="Inclusões por processo"),
        xaxis=dict(title=""),
        **_LAYOUT_BASE,
    )
    fig.update_xaxes(**_AXIS)
    fig.update_yaxes(**_AXIS)
    return fig


def plot_nf() -> go.Figure:
    categorias = ['Plenário Virtual', 'Plenário Presencial']
    valores = [86.0, 39.2]
    cores = [COR_PV, COR_PP]

    fig = go.Figure(data=[
        go.Bar(x=categorias, y=valores, marker_color=cores,
               text=[f'{str(v).replace(".", ",")}%' for v in valores],
               textposition='outside', cliponaxis=False, showlegend=False)
    ])

    fig.update_layout(
        title="<b>Considerado o processo, o ambiente virtual conclui 86% do que pauta</b><br><sup>Percentual de processos pautados que tiveram julgamento concluído, 2020-2025</sup>",
        yaxis=dict(range=[0, 105], title="%"),
        xaxis=dict(title=""),
        **_LAYOUT_BASE,
    )
    fig.update_xaxes(**_AXIS)
    fig.update_yaxes(**_AXIS)
    return fig
