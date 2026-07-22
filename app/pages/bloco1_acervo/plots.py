"""Figuras Plotly do Bloco 1 — Narrativa do Acervo (1988–2025).

Gráficos 1.a, 1.b, 1.c, 1.d conforme Especificacoes_graficos_Joao.md.
Fonte dos dados: evolucao_acervo (data/processed/acervo/evolucao_acervo.parquet).
"""

from __future__ import annotations
import pandas as pd
import plotly.graph_objects as go

from estilo import (
    aplicar_padrao, add_er_marker, br,
    CINZA, VERMELHO, ER_DATAS,
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
        rotulos.append(f"{a}-{fim}" if a != fim else str(a))
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
    return aplicar_padrao(
        fig,
        "O acervo cresce em praticamente todos os triênios desde 1988",
        "Variação do acervo (distribuições − baixas) por triênio, Controle Concentrado, 1988–2025",
        xaxis=dict(title="Período"), yaxis=dict(title="Variação do acervo"),
    )


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
    fig = aplicar_padrao(
        fig,
        "O acervo ativo é dominado por ADI ao longo de toda a série",
        "Acervo ativo por classe processual e ano, Controle Concentrado, 1988–2025",
        xaxis=dict(title="Processos ativos", range=[0, ymax * 1.12]),
        yaxis=dict(title="", type="category", range=[-0.5, len(anos) - 0.5]),
        height=1500, showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.01, x=0.5, xanchor="center"),
    )
    if show_values:
        for i, total in enumerate(totais):
            fig.add_annotation(x=total, y=i, text=f"<b>{br(total)}</b>", showarrow=False,
                               font=dict(color="black", size=11), xref="x", yref="y", xanchor="left", xshift=6)
    for er in (51, 52, 53):
        ano, mes, _ = ER_DATAS[er]
        idx_from_top = list(piv.index).index(ano) if ano in piv.index else None
        if idx_from_top is not None:
            frac = idx_from_top - (mes - 1) / 12
            fig.add_shape(type="line", x0=0, x1=ymax, y0=frac, y1=frac,
                          line=dict(color="black", width=1.5, dash="dash"), xref="x", yref="y")
            fig.add_annotation(x=ymax * 0.97, y=frac, text=f"<b>ER {er}</b>", showarrow=False,
                               font=dict(color="black", size=11), xref="x", yref="y", yshift=8)
    return fig


def fig_1c_distribuicao_baixa(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    """1.c — Distribuições (positivo) e baixas (negativo, espelhado) por ano."""
    tot = _totais_por_ano(df).sort_values("ano")
    anos = [str(a) for a in tot["ano"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=anos, y=tot["quantidade_distribuidos"], name="Distribuições",
                          marker_color="#2563EB"))
    fig.add_trace(go.Bar(x=anos, y=-tot["quantidade_baixas"], name="Baixas",
                          marker_color=CINZA))
    fig.update_layout(barmode="relative")

    ymin, ymax = -920, 940
    fig = aplicar_padrao(
        fig,
        "Distribuições superam baixas na maior parte da série histórica",
        "Distribuições e baixas anuais (espelhadas), Controle Concentrado, 1988–2025",
        xaxis=dict(title="Ano", dtick=1, tickangle=-90),
        yaxis=dict(title="Processos", range=[ymin, ymax]),
        showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.5, xanchor="center"),
    )
    add_er_marker(fig, 0, 51, ymin, ymax, ymax * 0.92)
    add_er_marker(fig, 0, 52, ymin, ymax, ymax * 0.92)
    add_er_marker(fig, 0, 53, ymin, ymax, ymax * 0.92)
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
        textposition="outside", textfont=dict(color="black", size=11, weight="bold"),
        cliponaxis=False,
    ))
    fig = aplicar_padrao(
        fig,
        "A variação anual do acervo tornou-se negativa na década de 2020",
        "Variação anual do acervo (distribuições − baixas), Controle Concentrado, 1988–2025",
        xaxis=dict(title="Ano", dtick=1, tickangle=-90), yaxis=dict(title="Variação"),
    )
    return fig
