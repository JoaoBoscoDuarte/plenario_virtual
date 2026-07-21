"""Plotly figures for narrative graphics NA–NF.

Values hardcoded per verification against inclusoes_em_pauta_mestre.parquet.
ponytail: hardcoded — compute from parquet if underlying data changes.
"""

from __future__ import annotations
import plotly.graph_objects as go

from estilo import aplicar_padrao, COR_PV, COR_PP, COR_AMBOS, VERMELHO as COR_ESPIN

_LAYOUT_EXTRA = dict(height=650, margin=dict(t=130, b=80, l=60, r=60), hovermode="x unified")


def plot_na(show_values: bool = True) -> go.Figure:
    anos = ['2020', '2021', '2022', '2023', '2024', '2025']
    valores = [59.8, 68.0, 64.1, 66.8, 59.0, 66.6]

    fig = go.Figure(data=[
        go.Bar(x=anos, y=valores, marker_color=COR_PV,
               text=[f'{v}%' for v in valores] if show_values else None,
               textposition='outside',
               cliponaxis=False, showlegend=False)
    ])

    fig.add_shape(type="line", x0=2.5, x1=2.5, y0=0, y1=85,
                  line=dict(color=COR_ESPIN, width=2, dash="dash"),
                  xref="x", yref="y")
    fig.add_annotation(x=2.5, y=80, text="ESPIN",
                       showarrow=False, font=dict(color=COR_ESPIN, size=17),
                       xref="x", yref="y")

    aplicar_padrao(
        fig,
        "A participação do Plenário Virtual mantém-se entre 59% e 68% ao ano",
        "Percentual das inclusões em pauta destinadas ao ambiente virtual, 2020-2025",
        yaxis=dict(range=[0, 85]),
        xaxis=dict(title="Ano"),
        **_LAYOUT_EXTRA,
    )
    return fig


def plot_nb(show_values: bool = True) -> go.Figure:
    categorias = ['Participação na pauta', 'Participação nos julgamentos concluídos']
    valores = [63.9, 91.3]

    fig = go.Figure(data=[
        go.Bar(x=categorias, y=valores, marker_color=COR_PV,
               text=[f'{v}%' for v in valores] if show_values else None,
               textposition='outside',
               cliponaxis=False, showlegend=False)
    ])

    aplicar_padrao(
        fig,
        "O Plenário Virtual concentra os julgamentos concluídos",
        "Participação do ambiente virtual na pauta e nos 3.187 julgamentos concluídos, 2020-2025",
        yaxis=dict(range=[0, 110]),
        xaxis=dict(title=""),
        **_LAYOUT_EXTRA,
    )
    return fig


def plot_nc(show_values: bool = True) -> go.Figure:
    categorias = ['Somente Plenário Presencial', 'Ambos os ambientes', 'Somente Plenário Virtual']
    valores = [5.6, 16.9, 77.5]
    processos = [159, 478, 2197]
    cores = [COR_PP, COR_AMBOS, COR_PV]
    textos = [f'{v}%  ({p} processos)' for v, p in zip(valores, processos)]

    fig = go.Figure(data=[
        go.Bar(y=categorias, x=valores, orientation='h', marker_color=cores,
               text=textos if show_values else None,
               textposition='outside', cliponaxis=False,
               showlegend=False)
    ])

    aplicar_padrao(
        fig,
        "Três de cada quatro processos nunca passam pelo Plenário Presencial",
        "Tramitação em pauta dos 2.834 processos de controle concentrado, 2020-2025",
        xaxis=dict(range=[0, 110], title="%"),
        yaxis=dict(title=""),
        **_LAYOUT_EXTRA,
    )
    return fig


def plot_nd(show_values: bool = True) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=['Recursos'], x=[94.3], name='Plenário Virtual', orientation='h',
        marker_color=COR_PV,
        text="Plenário Virtual: 94,3% (1.048 recursos)" if show_values else None,
        textposition='inside', insidetextanchor='middle',
    ))

    fig.add_trace(go.Bar(
        y=['Recursos'], x=[5.7], name='Plenário Presencial', orientation='h',
        marker_color=COR_PP,
        text="PP: 5,7% (63)" if show_values else None,
        textposition='outside',
    ))

    aplicar_padrao(
        fig,
        "A atividade recursal migrou quase integralmente para o ambiente virtual",
        "Destino das 1.111 inclusões em pauta de recursos (AgR, ED e afins), 2020-2025",
        barmode='stack',
        xaxis=dict(title="%"),
        yaxis=dict(title=""),
        showlegend=False,
        **_LAYOUT_EXTRA,
    )
    return fig


def plot_ne(show_values: bool = True) -> go.Figure:
    categorias = ['Plenário Virtual', 'Plenário Presencial']
    valores = [1.8, 4.3]
    cores = [COR_PV, COR_PP]

    fig = go.Figure(data=[
        go.Bar(x=categorias, y=valores, marker_color=cores,
               text=[str(v).replace('.', ',') for v in valores] if show_values else None,
               textposition='outside', cliponaxis=False, showlegend=False)
    ])

    aplicar_padrao(
        fig,
        "Cada julgamento presencial consome mais que o dobro de inclusões em pauta",
        "Média de inclusões em pauta por processo em cada ambiente, 2020-2025",
        yaxis=dict(range=[0, 5.5], title="Inclusões por processo"),
        xaxis=dict(title=""),
        **_LAYOUT_EXTRA,
    )
    return fig


def plot_nf(show_values: bool = True) -> go.Figure:
    categorias = ['Plenário Virtual', 'Plenário Presencial']
    valores = [86.0, 39.2]
    cores = [COR_PV, COR_PP]

    fig = go.Figure(data=[
        go.Bar(x=categorias, y=valores, marker_color=cores,
               text=[f'{str(v).replace(".", ",")}%' for v in valores] if show_values else None,
               textposition='outside', cliponaxis=False, showlegend=False)
    ])

    aplicar_padrao(
        fig,
        "Considerado o processo, o ambiente virtual conclui 86% do que pauta",
        "Percentual de processos pautados que tiveram julgamento concluído, 2020-2025",
        yaxis=dict(range=[0, 105]),
        xaxis=dict(title=""),
        **_LAYOUT_EXTRA,
    )
    return fig
