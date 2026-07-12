"""Layout e visualizações da página Visão Geral."""

from __future__ import annotations
import textwrap
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

_CORES_FASES = {
    1: "#7f8c8d",
    2: "#3498db",
    3: "#9b59b6",
    4: "#e67e22",
}

_DADOS_TIMELINE = [
    {"fase": 1, "data": "2007",      "norma": "ER 21/2007",        "desc": "Criação do formato eletrônico assíncrono para votação sobre repercussão geral em RE; prazo comum de 20 dias corridos."},
    {"fase": 1, "data": "2010",      "norma": "ER 41/2010",        "desc": "Redistribuição dos autos quando o relator é vencido."},
    {"fase": 1, "data": "2010",      "norma": "ER 42/2010",        "desc": "1ª ampliação: julgamento de mérito de RE com repercussão geral reconhecida (reafirmação de jurisprudência)."},
    {"fase": 2, "data": "2016",      "norma": "ER 51/2016",        "desc": "2ª ampliação: julgamento de agravos internos e EDs; possibilidade de julgamentos virtuais pelas Turmas; aproximação do controle concentrado."},
    {"fase": 2, "data": "2016",      "norma": "Res. 587/2016",     "desc": "Criação do 'destaque'; sessões semanais (7 dias corridos para votos)."},
    {"fase": 2, "data": "2018",      "norma": "Res. 611/2018",     "desc": "Prorrogação automática de prazo para 1º dia útil; abstenção computada como adesão ao relator."},
    {"fase": 3, "data": "2019",      "norma": "ER 52/2019",        "desc": "3ª ampliação: cautelares em controle concentrado, referendos; todas as classes em temas com jurisprudência dominante."},
    {"fase": 3, "data": "2019",      "norma": "Res. 642/2019",     "desc": "Prazo de votos reduzido p/ 5 dias úteis; destaque/sustentação oral deslocam ao presencial."},
    {"fase": 4, "data": "3/2/2020",  "norma": "Portaria MS 188",   "desc": "Declaração da ESPIN (início oficial da pandemia de Covid-19)."},
    {"fase": 4, "data": "18/3/2020", "norma": "ER 53/2020",        "desc": "Expansão irrestrita: todas as classes processuais (inclui mérito concentrado); sustentação oral virtual; sessões extraordinárias."},
    {"fase": 4, "data": "2020",      "norma": "Res. 669/2020",     "desc": "Pedidos de vista formulados no presencial podem ser devolvidos ao PV."},
    {"fase": 4, "data": "2020",      "norma": "Res. 672/2020",     "desc": "Sessões síncronas por videoconferência autorizadas."},
    {"fase": 4, "data": "2020",      "norma": "Res. 675/2020",     "desc": "Publicidade em tempo real: votos disponíveis ao público externo durante o julgamento."},
    {"fase": 4, "data": "2020",      "norma": "Res. 684/2020",     "desc": "Prazo de voto elastecido de 5 para 6 dias úteis (sessão começa e termina sexta-feira)."},
    {"fase": 4, "data": "2020",      "norma": "ER 54/2020",        "desc": "Abstenção passa a constar como 'não participação'; expressão 'Plenário Virtual' inserida no RISTF."},
    {"fase": 4, "data": "22/4/2022", "norma": "Portaria MS 913",   "desc": "Fim oficial da ESPIN (encerramento formal do período pandêmico e início do recorte pós-pandêmico)."},
    {"fase": 4, "data": "2022",      "norma": "ER 58/2022",        "desc": "Cautelares monocráticas submetidas automaticamente a referendo na pauta virtual subsequente."},
    {"fase": 4, "data": "2024",      "norma": "Res. 844/2024",     "desc": "Sessões virtuais com horário fixo de início (11h sexta) e encerramento (23h59 sexta seguinte)."},
    {"fase": 4, "data": "2024",      "norma": "Portaria 249/2024", "desc": "Instituição de Grupo de Trabalho para atualização das normas do PV."},
    {"fase": 4, "data": "21/8/2025", "norma": "Portal de Sessões", "desc": "Lançamento de ferramenta unificada de consulta a deliberações síncronas e assíncronas."},
]

_ROTULOS_FASES = {
    1: "ETAPA RESTRITA",
    2: "ETAPA AMPLIATIVA 1",
    3: "ETAPA AMPLIATIVA 2",
    4: "ETAPA AMPLIATIVA 3",
}

# Faixas Y de cada fase (de cima para baixo = índice crescente)
_FAIXAS_FASE = {
    1: (17.5, 20.5),
    2: (14.5, 17.5),
    3: (12.5, 14.5),
    4: (0.5,  12.5),
}
_CENTRO_FASE = {f: (y0 + y1) / 2 for f, (y0, y1) in _FAIXAS_FASE.items()}


def render_timeline() -> None:
    st.subheader("Linha do Tempo — Evolução do Plenário Virtual")
    st.caption(
        "Marcos normativos que moldaram o Plenário Virtual do STF desde sua criação em 2007 "
        "até 2025, organizados em quatro etapas de expansão."
    )
    with st.expander("Critério / Fonte"):
        st.markdown(
            "- **Fonte:** Emendas Regimentais (ER), Resoluções e Portarias do STF/MS  \n"
            "- **Etapas:** Restrita (2007–2015) → Ampliativa 1 (2016–2018) → "
            "Ampliativa 2 (2019) → Ampliativa 3 (2020–2025)  \n"
            "- **Zona verde:** período da ESPIN (Portaria MS 188/2020 a Portaria MS 913/2022)"
        )

    total = len(_DADOS_TIMELINE)
    y_max = total + 1
    fig = go.Figure()

    # Faixas coloridas de fase (linha vertical à esquerda)
    for fase, (y0, y1) in _FAIXAS_FASE.items():
        fig.add_shape(
            type="line", x0=0, x1=0, y0=y0, y1=y1,
            line=dict(color=_CORES_FASES[fase], width=6),
        )

    # Rótulos laterais das fases
    for fase, y_centro in _CENTRO_FASE.items():
        fig.add_annotation(
            x=-0.08, y=y_centro,
            text=f"<b>{_ROTULOS_FASES[fase]}</b>",
            textangle=-90,
            font=dict(color=_CORES_FASES[fase], size=11),
            showarrow=False,
        )

    # Zona ESPIN (eventos 9 a 15 = índices 8..14 → y = total-8 .. total-14)
    # Portaria MS 188 (idx 8) → y=12, Portaria MS 913 (idx 15) → y=5
    fig.add_hrect(y0=4.5, y1=12.5, fillcolor="green", opacity=0.08,
                  line_width=0, layer="below")
    fig.add_annotation(
        x=0.97, y=8.5,
        text="<b>ESPIN</b>",
        showarrow=False, xanchor="right", yanchor="middle",
        font=dict(color="green", size=10),
    )

    # Eventos
    for i, evt in enumerate(_DADOS_TIMELINE):
        y = total - i
        desc_wrap = "<br>".join(textwrap.wrap(evt["desc"], width=85))
        texto = (
            f"<span style='font-size:12px;font-weight:bold;color:#2c3e50'>"
            f"{evt['norma']} ({evt['data']})</span><br>"
            f"<span style='font-size:11px;color:#555555'>{desc_wrap}</span>"
        )
        fig.add_trace(go.Scatter(
            x=[0], y=[y], mode="markers",
            marker=dict(size=12, color="white",
                        line=dict(color=_CORES_FASES[evt["fase"]], width=3)),
            hoverinfo="skip",
        ))
        fig.add_annotation(
            x=0.03, y=y, text=texto,
            showarrow=False, xanchor="left", yanchor="middle", align="left",
        )

    fig.update_layout(
        title_text="<b>Evolução do Plenário Virtual e Controle Concentrado (STF)</b>",
        title_x=0.5,
        paper_bgcolor="white", plot_bgcolor="white",
        showlegend=False,
        height=1400,
        margin=dict(t=60, b=20, l=80, r=20),
    )
    fig.update_xaxes(range=[-0.15, 1.0], visible=False, fixedrange=True)
    fig.update_yaxes(range=[0, y_max], visible=False, fixedrange=True)

    st.plotly_chart(fig, width="stretch")


def render_metricas(df: pd.DataFrame) -> None:
    c1, c2, c3 = st.columns(3)
    c1.metric("Total (filtrado)", len(df))
    c2.metric("Classes únicas",
              df["classe"].nunique() if "classe" in df.columns else 0)
    c3.metric("Tipos de processo",
              df["tipo_processo"].nunique() if "tipo_processo" in df.columns else 0)
