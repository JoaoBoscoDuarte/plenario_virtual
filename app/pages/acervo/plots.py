"""Figuras Plotly para a página de Acervo — função única paramétrica.

Modelo visual idêntico ao 1.b2 (app/pages/bloco1_acervo/plots.py):
mesmas cores de classe, linhas ER/ESPIN, legenda e fontes de eixo.
"""

from __future__ import annotations
import plotly.graph_objects as go
import pandas as pd

from estilo import aplicar_padrao, br, AZUL, VERMELHO, ER_DATAS, _frac_ano

_CORES_CLASSE = {"ADI": "#2563EB", "ADPF": "#93C5FD", "ADC": "#059669", "ADO": "#7C3AED"}
ANO_MIN = 1988

# Título/subtítulo "história" por métrica, para a visão TOTAL (verificado contra os dados).
_HISTORIA_METRICA = {
    "quantidade_ativos": (
        "O acervo ativo encolhe ano a ano desde o pico de 2017",
        "Estoque de processos ativos ao final de cada ano",
    ),
    "quantidade_inativos": (
        "O acervo inativo cresce de forma ininterrupta desde 1988",
        "Estoque acumulado de processos encerrados",
    ),
    "total_geral": (
        "O acervo total nunca parou de crescer, mesmo com a queda dos ativos",
        "Soma de processos ativos e inativos ao final de cada ano",
    ),
    "quantidade_baixas": (
        "As baixas anuais dispararam com a ESPIN e a virtualização do julgamento",
        "Processos baixados por ano",
    ),
    "quantidade_distribuidos": (
        "As distribuições recuam após o pico da pandemia em 2020–2021",
        "Processos distribuídos por ano",
    ),
}


def _titulo_classe(d: pd.DataFrame, coluna_metrica: str, label_metrica: str, classe_nome: str) -> str:
    """Título calculado a partir da tendência real da classe (primeiro vs. último ano)."""
    d = d.sort_values("ano")
    v_ini, v_fim = float(d[coluna_metrica].iloc[0]), float(d[coluna_metrica].iloc[-1])
    ano_ini, ano_fim = int(d["ano"].iloc[0]), int(d["ano"].iloc[-1])
    if v_fim > v_ini:
        tendencia = "cresce"
    elif v_fim < v_ini:
        tendencia = "cai"
    else:
        tendencia = "se mantém estável"
    return (
        f"Classe {classe_nome}: {label_metrica.lower()} {tendencia} "
        f"de {br(v_ini)} ({ano_ini}) para {br(v_fim)} ({ano_fim})"
    )


def plotar_grafico_stf(
    df: pd.DataFrame,
    classe_nome: str,
    coluna_metrica: str,
    label_metrica: str,
    show_values: bool = False,
) -> go.Figure:
    """
    Função única de plotagem paramétrica — modelo visual do 1.b2.

    - classe_nome="TOTAL": barra do agregado geral, cor AZUL, título "história" fixo por métrica.
    - classe_nome=<classe>: barra da classe, cor de `_CORES_CLASSE`, título calculado pela tendência real.
    """
    is_total = classe_nome.upper() == "TOTAL"

    if is_total:
        d = df.groupby("ano", as_index=False)[coluna_metrica].sum()
        cor = AZUL
        nome = f"TOTAL GERAL ({label_metrica.upper()})"
    else:
        d = df[df["classe"] == classe_nome].sort_values("ano")
        cor = _CORES_CLASSE.get(classe_nome, AZUL)
        nome = f"CLASSE: {classe_nome.upper()}"

    anos_int = sorted(d["ano"].unique().tolist())
    anos = [str(a) for a in anos_int]
    ymax = float(d[coluna_metrica].max() or 1)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[str(a) for a in d["ano"]],
        y=d[coluna_metrica],
        marker_color=cor,
        text=[br(v) for v in d[coluna_metrica]] if show_values else None,
        textposition="outside",
        textfont=dict(color="black", size=13, weight="bold"),
        cliponaxis=False,
        name=nome,
    ))

    y_er = ymax * 1.1
    y_espin = ymax * 1.1

    # ESPIN — réplica exata de fig_1b2_acervo_por_classe_vertical
    if 2020 in anos_int and 2022 in anos_int:
        idx_2020 = anos.index("2020")
        idx_2022 = anos.index("2022")
        x0_espin = idx_2020 - 0.5
        x1_espin = idx_2022 + 0.5
        x0_linha_espin = x0_espin + 0.06

        fig.add_vrect(x0=x0_espin, x1=x1_espin, fillcolor="#FCE7F3", opacity=0.7, line_width=0, layer="below")
        fig.add_shape(type="line", x0=x0_linha_espin, x1=x0_linha_espin, y0=0, y1=y_espin,
                      line=dict(color=VERMELHO, width=1.5, dash="dash"), xref="x", yref="y")
        fig.add_shape(type="line", x0=x1_espin, x1=x1_espin, y0=0, y1=y_espin,
                      line=dict(color=VERMELHO, width=1.5, dash="dash"), xref="x", yref="y")
        fig.add_annotation(x=x0_linha_espin, y=y_espin, ax=x1_espin, ay=y_espin, axref="x", ayref="y",
                           xref="x", yref="y", showarrow=True, arrowhead=2, arrowsize=1.6,
                           arrowwidth=1.2, arrowcolor=VERMELHO, text="")
        fig.add_annotation(x=x1_espin, y=y_espin, ax=x0_linha_espin, ay=y_espin, axref="x", ayref="y",
                           xref="x", yref="y", showarrow=True, arrowhead=2, arrowsize=1.6,
                           arrowwidth=1.2, arrowcolor=VERMELHO, text="")
        fig.add_annotation(x=(x0_linha_espin + x1_espin) / 2, y=y_espin, yanchor="bottom", yshift=6,
                           text="<b>ESPIN</b>", showarrow=False,
                           font=dict(color=VERMELHO, size=13, weight="bold"),
                           xref="x", yref="y")

    # ER — réplica exata de fig_1b2_acervo_por_classe_vertical
    for er in (51, 52, 53):
        if er in (52, 53):
            ano_er, _, _ = ER_DATAS[er]
            if str(ano_er) not in anos:
                continue
            x = anos.index(str(ano_er)) - 0.5
        else:
            ano_er, mes, dia = ER_DATAS[er]
            x = _frac_ano(ANO_MIN, ano_er, mes, dia)
        fig.add_shape(type="line", x0=x, x1=x, y0=0, y1=y_er,
                      line=dict(color="#000000", width=1.5, dash="dash"), xref="x", yref="y")
        fig.add_annotation(x=x, y=y_er, yanchor="bottom", text=f"<b>ER<br>{er}</b>", showarrow=False,
                           font=dict(color="#000000", size=11), bgcolor="white", borderpad=1,
                           xref="x", yref="y")

    if is_total:
        titulo, subtitulo_base = _HISTORIA_METRICA[coluna_metrica]
    else:
        titulo = _titulo_classe(d, coluna_metrica, label_metrica, classe_nome)
        subtitulo_base = label_metrica

    titulo_peca = "Total Geral" if is_total else f"Classe {classe_nome}"
    ano_min, ano_max = anos_int[0], anos_int[-1]
    subtitulo = f"{subtitulo_base} — {titulo_peca} ({ano_min}–{ano_max})"

    fig = aplicar_padrao(
        fig, titulo, subtitulo,
        xaxis=dict(title=""), yaxis=dict(title="", range=[0, ymax * 1.2]),
        showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=0.95, x=0.5, xanchor="center"),
        height=650, margin=dict(t=150, b=70, l=60, r=40),
    )
    fig.update_yaxes(showline=True)
    fig.update_xaxes(tickfont=dict(size=22), title_font=dict(size=22))
    return fig
