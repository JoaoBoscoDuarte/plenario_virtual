"""Figuras Plotly do Bloco 1 — Narrativa do Acervo (1988–2025).

Gráficos 1.a, 1.b, 1.c, 1.d conforme Especificacoes_graficos_Joao.md.
Fonte dos dados: evolucao_acervo (data/processed/acervo/evolucao_acervo.parquet).
"""

from __future__ import annotations
import pandas as pd
import plotly.graph_objects as go

from estilo import (
    aplicar_padrao, add_er_marker, _frac_ano, br,
    CINZA, VERMELHO, VERDE, ER_DATAS,
)

_CLASSES = ["ADI", "ADPF", "ADC", "ADO"]
_CORES_CLASSE = {"ADI": "#2563EB", "ADPF": "#93C5FD", "ADC": "#059669", "ADO": "#7C3AED"}
ANO_MIN = 1988


def _totais_por_ano(df: pd.DataFrame) -> pd.DataFrame:
    """Soma distribuídos/baixas/ativos por ano, agregando as 4 classes."""
    return df.groupby("ano", as_index=False)[
        ["quantidade_distribuidos", "quantidade_baixas", "quantidade_ativos"]
    ].sum()


def fig_1a_variacao_trienal(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    """1.a — Variação do acervo (distribuição - baixa) agrupada em triênios (último grupo: biênio)."""
    tot = _totais_por_ano(df).sort_values("ano")
    tot["variacao"] = tot["quantidade_distribuidos"] - tot["quantidade_baixas"]

    anos = tot["ano"].tolist()
    ano_max = max(anos)
    grupos, rotulos = [], []
    a = ANO_MIN
    while a <= ano_max:
        fim = min(a + 2, ano_max)
        grupos.append((a, fim))
        rotulos.append(f"{a}<br>{fim}" if a != fim else str(a))
        a = fim + 1

    valores = []
    for ini, fim in grupos:
        mask = (tot["ano"] >= ini) & (tot["ano"] <= fim)
        valores.append(tot.loc[mask, "variacao"].sum())

    cores = [CINZA if v >= 0 else VERMELHO for v in valores]
    textos = [f"{'+' if v >= 0 else ''}{br(v)}" for v in valores]

    fig = go.Figure(go.Bar(
        x=rotulos, y=valores, marker_color=cores,
        text=textos if show_values else None, textposition="outside",
        textfont=dict(color="black", size=13, weight="bold"), cliponaxis=False,
    ))
    fig = aplicar_padrao(
        fig,
        "Após três décadas de acumulação, o acervo passa a encolher em 2018",
        "Variação do acervo ativo de controle concentrado por triênio (distribuição menos baixa), 1988 - 2025",
        xaxis=dict(title=""), yaxis=dict(title=""),
    )
    fig.update_yaxes(showline=False, showticklabels=False, ticks="")
    return fig


def fig_1b_acervo_por_classe(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    """1.b — Acervo ativo por classe, barras horizontais empilhadas, 1988 no topo a 2025 na base."""
    piv = df.pivot_table(index="ano", columns="classe", values="quantidade_ativos", aggfunc="sum").fillna(0)
    piv = piv.reindex(columns=_CLASSES, fill_value=0).sort_index(ascending=False)
    anos = [str(a) for a in piv.index]
    totais = piv.sum(axis=1)

    fig = go.Figure()
    for classe in _CLASSES:
        fig.add_trace(go.Bar(
            y=anos, x=piv[classe], name=classe, orientation="h",
            marker_color=_CORES_CLASSE[classe],
        ))
    fig.update_layout(barmode="stack")

    ymax = int(totais.max())
    anos_int = list(piv.index)
    leg_y = 0.98
    fig = aplicar_padrao(
        fig,
        "O acervo ativo é dominado por ADI ao longo de toda a série",
        "Acervo ativo por classe processual e ano, Controle Concentrado, 1988–2025",
        xaxis=dict(title="Processos ativos", range=[0, ymax * 1.48]),
        yaxis=dict(title="", type="category", range=[-0.5, len(anos) - 0.5]),
        height=1500, showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=leg_y, x=0.5, xanchor="center"),
    )
    if show_values:
        for i, total in enumerate(totais):
            fig.add_annotation(x=total, y=i, text=f"<b>{br(total)}</b>", showarrow=False,
                               font=dict(color="black", size=13), xref="x", yref="y", xanchor="left", xshift=6)

    x_linha = ymax * 1.16  # linhas de marcação se estendem além das barras
    x_label = ymax * 1.19  # rótulos ficam no espaço em branco à direita

    # Faixa ESPIN: do início de 2020 ao final de 2022 (limites entre linhas de ano).
    if 2020 in anos_int and 2022 in anos_int:
        y0_espin = anos_int.index(2022) - 0.5
        y1_espin = anos_int.index(2020) + 0.5
        x_seta = ymax * 1.25       # seta-medida fica no gradiente, entre os rótulos ER e o texto ESPIN
        x_espin_label = ymax * 1.34  # texto ESPIN mais recuado que os rótulos ER

        fig.add_hrect(y0=y0_espin, y1=y1_espin, fillcolor="#FCE7F3", opacity=0.7,
                      line_width=0, layer="below")
        for y in (y0_espin, y1_espin):
            fig.add_shape(type="line", x0=0, x1=x_linha, y0=y, y1=y,
                          line=dict(color="black", width=2.5, dash="dash"), xref="x", yref="y")

        # Seta dupla (medida) demarcando o intervalo de tempo do ESPIN.
        fig.add_annotation(x=x_seta, y=y1_espin, ax=x_seta, ay=y0_espin, axref="x", ayref="y",
                           xref="x", yref="y", showarrow=True, arrowhead=2, arrowsize=1.2,
                           arrowwidth=2, arrowcolor=VERMELHO, text="")
        fig.add_annotation(x=x_seta, y=y0_espin, ax=x_seta, ay=y1_espin, axref="x", ayref="y",
                           xref="x", yref="y", showarrow=True, arrowhead=2, arrowsize=1.2,
                           arrowwidth=2, arrowcolor=VERMELHO, text="")

        fig.add_annotation(x=x_espin_label, y=(y0_espin + y1_espin) / 2, text="<b>ESPIN</b>",
                           showarrow=False, font=dict(color=VERMELHO, size=13, weight="bold"),
                           xref="x", yref="y", xanchor="left")

    # Marcadores ER: linha na fronteira entre o ano da emenda e o ano anterior.
    for er in (51, 52, 53):
        ano, _, _ = ER_DATAS[er]
        if ano in anos_int:
            frac = anos_int.index(ano) + 0.5
            fig.add_shape(type="line", x0=0, x1=x_linha, y0=frac, y1=frac,
                          line=dict(color="black", width=2.5, dash="dash"), xref="x", yref="y")
            fig.add_annotation(x=x_label, y=frac, text=f"<b>ER {er}</b>", showarrow=False,
                               font=dict(color="black", size=13), xref="x", yref="y", xanchor="left")
    return fig


def fig_1c_distribuicao_baixa(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    """1.c — Distribuições (positivo) e baixas (negativo, espelhado) por ano."""
    tot = _totais_por_ano(df).sort_values("ano")
    anos = [str(a) for a in tot["ano"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=anos, y=tot["quantidade_distribuidos"], name="DISTRIBUIÇÕES",
                          marker_color="#2563EB",
                          text=[br(v) for v in tot["quantidade_distribuidos"]] if show_values else None,
                          textposition="outside", textfont=dict(color="black", size=13, weight="bold"),
                          cliponaxis=False))
    fig.add_trace(go.Bar(x=anos, y=-tot["quantidade_baixas"], name="BAIXAS",
                          marker_color=CINZA,
                          text=[br(v) for v in tot["quantidade_baixas"]] if show_values else None,
                          textposition="outside", textfont=dict(color="black", size=13, weight="bold"),
                          cliponaxis=False))
    fig.update_layout(barmode="relative")

    d_max = tot["quantidade_distribuidos"].max()
    b_max = tot["quantidade_baixas"].max()
    ymin = -int(b_max * 1.15)
    ymax = int(d_max * 1.30)
    fig = aplicar_padrao(
        fig,
        "Distribuições superam baixas na maior parte da série histórica",
        "Distribuições e baixas anuais (espelhadas), Controle Concentrado, 1988–2025",
        xaxis=dict(title="", tickangle=-90, type="category", range=[-0.5, len(anos) - 0.5]),
        yaxis=dict(title="", range=[ymin, ymax]),
        showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.5, xanchor="center"),
        height=650,
    )
    er_y = ymax * 0.90  # todas as linhas ER terminam na mesma altura ("final da linha")
    er_yshift = {51: 0, 52: 16, 53: -16}  # deslocamento em pixels p/ 52/53 não se chocarem (anos adjacentes)
    for er in (51, 52, 53):
        if er in (52, 53):
            ano_er, _, _ = ER_DATAS[er]
            x = anos.index(str(ano_er)) - 0.5
        else:
            ano, mes, dia = ER_DATAS[er]
            x = _frac_ano(ANO_MIN, ano, mes, dia)
        fig.add_shape(type="line", x0=x, x1=x, y0=ymin, y1=ymax,
                      line=dict(color="black", width=1.5, dash="dash"), xref="x", yref="y")
        fig.add_annotation(x=x, y=er_y, yshift=er_yshift[er], text=f"<b>ER {er}</b>", showarrow=False,
                           font=dict(color="black", size=12), bgcolor="white", borderpad=1,
                           xref="x", yref="y")
    idx_2020 = anos.index("2020")
    idx_2022 = anos.index("2022")
    x0 = idx_2020 - 0.5
    x1 = idx_2022 + 0.5
    fig.add_vrect(x0=x0, x1=x1, fillcolor="#FCE7F3", opacity=0.7, line_width=0, layer="below")
    fig.add_annotation(x=(x0 + x1) / 2, y=ymax * 0.99, yanchor="top", text="<b>ESPIN</b>", showarrow=False,
                       font=dict(color=VERMELHO, size=13, weight="bold"), bgcolor="white", borderpad=2,
                       xref="x", yref="y")
    fig.update_yaxes(showline=False, showticklabels=False, ticks="")
    return fig


def fig_1d_variacao_anual(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    """1.d — Variação anual do acervo (distribuições − baixas), positivo cinza / negativo vermelho."""
    tot = _totais_por_ano(df).sort_values("ano")
    tot["variacao"] = tot["quantidade_distribuidos"] - tot["quantidade_baixas"]
    anos = [str(a) for a in tot["ano"]]
    cores = [CINZA if v >= 0 else VERMELHO for v in tot["variacao"]]

    fig = go.Figure(go.Bar(
        x=anos, y=tot["variacao"], marker_color=cores,
        text=[f"{'+' if v >= 0 else ''}{br(v)}" for v in tot["variacao"]] if show_values else None,
        textposition="outside", textfont=dict(color="black", size=13, weight="bold"),
        cliponaxis=False,
    ))
    v_abs = max(abs(tot["variacao"].max()), abs(tot["variacao"].min()))
    ymax = int(v_abs * 1.4)
    ymin = -int(v_abs * 1.15)
    fig = aplicar_padrao(
        fig,
        "A variação anual do acervo tornou-se negativa na década de 2020",
        "Variação anual do acervo (distribuições − baixas), Controle Concentrado, 1988–2025",
        xaxis=dict(title="", dtick=1, tickangle=-90), yaxis=dict(title="", range=[ymin, ymax]),
    )
    er_y = ymax * 0.90  # todas as linhas ER terminam na mesma altura ("final da linha")
    er_yshift = {51: 0, 52: 16, 53: -16}  # deslocamento em pixels p/ 52/53 não se chocarem (anos adjacentes)
    for er in (51, 52, 53):
        if er in (52, 53):
            ano_er, _, _ = ER_DATAS[er]
            x = anos.index(str(ano_er)) - 0.5
        else:
            ano, mes, dia = ER_DATAS[er]
            x = _frac_ano(ANO_MIN, ano, mes, dia)
        fig.add_shape(type="line", x0=x, x1=x, y0=ymin, y1=ymax,
                      line=dict(color="black", width=1.5, dash="dash"), xref="x", yref="y")
        fig.add_annotation(x=x, y=er_y, yshift=er_yshift[er], text=f"<b>ER {er}</b>", showarrow=False,
                           font=dict(color="black", size=12), bgcolor="white", borderpad=1,
                           xref="x", yref="y")
    idx_2020 = anos.index("2020")
    idx_2022 = anos.index("2022")
    x0 = idx_2020 - 0.5
    x1 = idx_2022 + 0.5
    fig.add_vrect(x0=x0, x1=x1, fillcolor="#FCE7F3", opacity=0.7, line_width=0, layer="below")
    fig.add_annotation(x=(x0 + x1) / 2, y=ymax * 0.99, yanchor="top", text="<b>ESPIN</b>", showarrow=False,
                       font=dict(color=VERMELHO, size=13, weight="bold"), bgcolor="white", borderpad=2,
                       xref="x", yref="y")
    fig.update_yaxes(showline=False, showticklabels=False, ticks="")
    return fig
