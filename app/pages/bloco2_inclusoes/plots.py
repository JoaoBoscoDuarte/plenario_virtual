"""Figuras Plotly do Bloco 2 — Narrativa Estendida das Inclusões em Pauta (2016–2025).

Gráficos 2.a–2.r e 3.1/3.2 conforme Especificacoes_graficos_Joao.md e COMPLETA GRÁFICOS.docx.
2.d foi descartado pela cliente ("desisti do gráfico"). 2.j2 (companion 2016-2019 de 2.j)
foi adicionado a pedido explícito da cliente no docx, sem ID formal no .md.
Fonte dos dados: inclusoes_em_pauta (2016–2025, já traz tipo_questao/sufixo corrigidos).
"""

from __future__ import annotations
import pandas as pd
import plotly.graph_objects as go

from estilo import aplicar_padrao, br, AZUL, AZUL_CLARO, CINZA, VERDE, ROXO, VERMELHO

COR_PV, COR_PP = AZUL, CINZA
_CLASSES = ["ADI", "ADPF", "ADC", "ADO"]
_CORES_CLASSE = {"ADI": "#2563EB", "ADPF": "#93C5FD", "ADC": "#059669", "ADO": "#7C3AED"}
_CORES_TIPO = {"PR": AZUL, "RC": "#f59e0b", "IJ": VERDE}
_CORES_CATEGORIA = {
    "Unânime": VERDE, "Maioria (relator vencedor)": AZUL,
    "Maioria (relator vencido)": "#f59e0b", "Não concluído": CINZA,
}
_CORES_NC = {
    "Pedido de vista": ROXO, "Destaque": "#ec4899",
    "Retirado de pauta": "#f59e0b", "Motivos diversos": CINZA,
}


def _categoria(d: str) -> str:
    if d == "Concluído - decisão unânime":
        return "Unânime"
    if d == "Concluído - decisão maioria com o relator":
        return "Maioria (relator vencedor)"
    if d == "Concluído - decisão maioria, vencido o relator":
        return "Maioria (relator vencido)"
    return "Não concluído"


def _categoria_nc(d: str) -> str:
    if d == "Não concluído - pedido de vista":
        return "Pedido de vista"
    if d == "Não concluído - destaque":
        return "Destaque"
    if d == "Não concluído - retirado de pauta":
        return "Retirado de pauta"
    return "Motivos diversos"


def _tramitacao_por_processo(df: pd.DataFrame, ano_ini: int, ano_fim: int) -> pd.Series:
    """Classifica cada processo (incidente) por ambiente(s) em que tramitou no período."""
    sub = df[df["ano"].between(ano_ini, ano_fim)]
    amb = sub.groupby("incidente")["ambiente"].apply(set)

    def classif(s):
        pv, pp = "Plenário Virtual" in s, "Plenário Presencial" in s
        if pv and pp:
            return "Ambos"
        return "Somente Virtual" if pv else "Somente Presencial"

    return amb.apply(classif)


# ── 2.a ──────────────────────────────────────────────────────────────────────
def fig_2a_participacao_ano(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    tab = df.groupby(["ano", "ambiente"]).size().unstack(fill_value=0)
    pct = 100 * tab["Plenário Virtual"] / tab.sum(axis=1)
    anos = [str(a) for a in pct.index]

    fig = go.Figure(go.Bar(
        x=anos, y=pct.values, marker_color=COR_PV,
        text=[f"{v:.1f}%".replace(".", ",") for v in pct.values] if show_values else None,
        textposition="outside", textfont=dict(color="black", size=16, weight="bold"),
        cliponaxis=False,
    ))
    x_espin = list(pct.index).index(2022) + 0.5
    fig.add_shape(type="line", x0=x_espin, x1=x_espin, y0=0, y1=85,
                  line=dict(color=VERMELHO, width=1.5, dash="dash"), xref="x", yref="y")
    fig.add_annotation(x=x_espin, y=80, text="<b>Fim da ESPIN</b>", showarrow=False,
                       font=dict(color=VERMELHO, size=13), bgcolor="white", borderpad=4, xref="x", yref="y")
    fig = aplicar_padrao(
        fig, "De 4% a dois terços da pauta: o degrau da universalização",
        "Participação do Plenário Virtual nas inclusões em pauta, 2016–2025",
        xaxis=dict(title="Ano"),
        yaxis=dict(title="", range=[0, 90]),
    )
    fig.update_yaxes(showline=False, showticklabels=False, ticks="")
    fig.update_xaxes(tickfont=dict(size=22), title_font=dict(size=22))
    return fig


# ── 2.b ──────────────────────────────────────────────────────────────────────
def fig_2b_inclusoes_ano_ambiente(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    tab = df.groupby(["ano", "ambiente"]).size().unstack(fill_value=0)
    anos = [str(a) for a in tab.index]

    fig = go.Figure()
    for amb, cor, nome in [("Plenário Virtual", COR_PV, "PLENÁRIO VIRTUAL"), ("Plenário Presencial", COR_PP, "PLENÁRIO PRESENCIAL")]:
        fig.add_trace(go.Bar(
            x=anos, y=tab[amb], name=nome, marker_color=cor,
            text=[br(v) for v in tab[amb]] if show_values else None,
            textposition="outside", textfont=dict(color="black", size=16, weight="bold"),
            cliponaxis=False,
        ))
    fig = aplicar_padrao(
        fig, "O salto das inclusões no ambiente virtual",
        "Inclusões em pauta por ano e ambiente, 2016–2025",
        xaxis=dict(title="Ano"), yaxis=dict(title="", showticklabels=False, ticks=""),
        barmode="group", showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=0.96, x=0.5, xanchor="center"),
    )
    fig.update_yaxes(showline=False, showticklabels=False, ticks="")
    fig.update_xaxes(tickfont=dict(size=22), title_font=dict(size=22))
    return fig


# ── 2.c ──────────────────────────────────────────────────────────────────────
_NOME_TIPO = {"PR": "PR", "RC": "RC", "IJ": "QI"}  # cliente pede rótulo "QI" (a base usa código "IJ")


def _tabela_2c(df: pd.DataFrame) -> pd.DataFrame:
    """Inclusões do PV por ano e tipo de questão (PR/RC/QI), 2016–2019 — para exportação."""
    sub = df[(df["ambiente"] == "Plenário Virtual") & df["ano"].between(2016, 2019) & df["tipo_questao"].isin(["PR", "RC", "IJ"])]
    tab = sub.groupby(["ano", "tipo_questao"]).size().unstack(fill_value=0).reindex(columns=["PR", "RC", "IJ"], fill_value=0)
    tab = tab.rename(columns=_NOME_TIPO)
    tab["Total"] = tab.sum(axis=1)
    return tab.reset_index().rename(columns={"ano": "Ano"})


def _tabela_2c(df: pd.DataFrame) -> pd.DataFrame:
    sub = df[(df["ambiente"] == "Plenário Virtual") & df["ano"].between(2016, 2019) & df["tipo_questao"].isin(["PR", "RC", "IJ"])]
    tab = sub.groupby(["ano", "tipo_questao"]).size().unstack(fill_value=0).reindex(columns=["RC", "PR", "IJ"], fill_value=0)
    tab["Total"] = tab.sum(axis=1)
    for tp in ["RC", "PR", "IJ"]:
        tab[f"%{tp}"] = (tab[tp] / tab["Total"] * 100).round(1).astype(str) + "%"
    tab = tab.reset_index()
    tab.columns = ["Ano", "RC", "PR", "IJ", "Total", "%RC", "%PR", "%IJ"]
    return tab[["Ano", "RC", "%RC", "PR", "%PR", "IJ", "%IJ", "Total"]]


def fig_2c_composicao_pv_tipo(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    sub = df[(df["ambiente"] == "Plenário Virtual") & df["ano"].between(2016, 2019) & df["tipo_questao"].isin(["PR", "RC", "IJ"])]
    tab = sub.groupby(["ano", "tipo_questao"]).size().unstack(fill_value=0).reindex(columns=["RC", "PR", "IJ"], fill_value=0)
    anos = [str(a) for a in tab.index]
    totais = tab.sum(axis=1)

    fig = go.Figure()
    for tipo in ["RC", "PR", "IJ"]:
        fig.add_trace(go.Bar(
            x=anos, y=tab[tipo], name=_NOME_TIPO[tipo], marker_color=_CORES_TIPO[tipo],
            text=None, cliponaxis=False,
        ))
    fig = aplicar_padrao(
        fig, "Em 2019, o virtual deixa de ser exclusivamente recursal",
        "Inclusões em pauta do Plenário Virtual por tipo de questão, 2016–2019",
        xaxis=dict(title="Ano", type="category", range=[-0.5, len(anos) - 0.5]),
        yaxis=dict(title="", range=[0, totais.max() * 1.2]),
        barmode="stack", showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=0.98, x=0.5, xanchor="center"),
        height=650,
    )
    fig.update_xaxes(tickfont=dict(size=22), title_font=dict(size=22))
    fig.update_yaxes(showline=False, showticklabels=False, ticks="")
    if show_values:
        for i, total in enumerate(totais):
            fig.add_annotation(x=i, y=total, text=f"<b>{br(total)}</b>", showarrow=False,
                               font=dict(color="black", size=20), xref="x", yref="y",
                               yanchor="bottom", yshift=6)
    return fig


# ── 2.e / 2.f ────────────────────────────────────────────────────────────────
def _classe_ano(df: pd.DataFrame, ambiente: str, show_values: bool, titulo: str, subtitulo: str, show_pct: bool = False) -> go.Figure:
    sub = df[(df["ambiente"] == ambiente) & df["ano"].between(2020, 2025)]
    tab = sub.groupby(["ano", "classe"], observed=True).size().unstack(fill_value=0).reindex(columns=_CLASSES, fill_value=0)
    anos = [str(a) for a in tab.index]
    totais_ano = tab.sum(axis=1)

    fig = go.Figure()
    for classe in _CLASSES:
        if show_values and show_pct:
            textos = [f"<span style='font-size:12px'>({v/totais_ano[ano]*100:.0f}%)</span><br><span style='font-size:20px'>{br(v)}</span>" if totais_ano[ano] > 0 else br(v)
                      for v, ano in zip(tab[classe], tab.index)]
        elif show_values:
            textos = [br(v) for v in tab[classe]]
        else:
            textos = None
        fig.add_trace(go.Bar(
            x=anos, y=tab[classe], name=classe, marker_color=_CORES_CLASSE[classe],
            text=textos, textposition="outside", textfont=dict(color="black", size=20, weight="bold"),
            cliponaxis=False,
        ))
    ymax = tab.values.max()
    yrange = [0, ymax * (1.35 if show_pct else 1.15)]
    fig = aplicar_padrao(
        fig, titulo, subtitulo,
        xaxis=dict(title="Ano"), yaxis=dict(title="", range=yrange),
        barmode="group", showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=0.92, x=0.5, xanchor="center"),
    )
    fig.update_yaxes(showline=False, showticklabels=False, ticks="")
    fig.update_xaxes(tickfont=dict(size=22), title_font=dict(size=22))
    return fig


def _tabela_2e(df: pd.DataFrame) -> pd.DataFrame:
    sub = df[(df["ambiente"] == "Plenário Virtual") & df["ano"].between(2020, 2025)]
    tab = sub.groupby(["ano", "classe"], observed=True).size().unstack(fill_value=0).reindex(columns=_CLASSES, fill_value=0)
    tab["Total"] = tab.sum(axis=1)
    for c in _CLASSES:
        tab[f"%{c}"] = (tab[c] / tab["Total"] * 100).round(1).astype(str) + "%"
    tab = tab.reset_index()
    cols = ["ano"] + [c for pair in zip(_CLASSES, [f"%{c}" for c in _CLASSES]) for c in pair] + ["Total"]
    out = tab[cols].copy()
    out.columns = ["Ano"] + [c for pair in zip(_CLASSES, [f"%{c}" for c in _CLASSES]) for c in pair] + ["Total"]
    return out


def fig_2e_classe_ano_pv(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    return _classe_ano(df, "Plenário Virtual", show_values,
                        "O Plenário Virtual concentra o crescimento das inclusões por classe",
                        "Inclusões em pauta por classe e ano — Plenário Virtual, 2020–2025",
                        show_pct=True)


def fig_2f_classe_ano_pp(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    return _classe_ano(df, "Plenário Presencial", show_values,
                        "O Plenário Presencial mantém volume estável e menor por classe",
                        "Inclusões em pauta por classe e ano — Plenário Presencial, 2020–2025",
                        show_pct=True)


# ── 2.h / 2.i ────────────────────────────────────────────────────────────────
def _tramitacao_anual(df: pd.DataFrame, ano_ini: int, ano_fim: int, show_values: bool, titulo: str, subtitulo: str) -> go.Figure:
    sub = df[df["ano"].between(ano_ini, ano_fim)].copy()
    tram = _tramitacao_por_processo(df, ano_ini, ano_fim)
    sub["tramitacao"] = sub["incidente"].map(tram)
    tab = sub.drop_duplicates("incidente").groupby(["ano", "tramitacao"], observed=True).size().unstack(fill_value=0)
    tab = tab.reindex(columns=["Somente Virtual", "Ambos", "Somente Presencial"], fill_value=0)
    anos = [str(a) for a in tab.index]
    cores = {"Somente Virtual": COR_PV, "Ambos": AZUL_CLARO, "Somente Presencial": COR_PP}

    fig = go.Figure()
    for cat in tab.columns:
        fig.add_trace(go.Bar(
            x=anos, y=tab[cat], name=cat, marker_color=cores[cat],
            text=[br(v) for v in tab[cat]] if show_values else None,
            textposition="outside", textfont=dict(color="black", size=10, weight="bold"),
            cliponaxis=False,
        ))
    fig = aplicar_padrao(
        fig, titulo, subtitulo,
        xaxis=dict(title="Ano do primeiro processo pautado"), yaxis=dict(title="Processos"),
        barmode="group", showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.5, xanchor="center"),
    )
    fig.update_xaxes(tickfont=dict(size=22), title_font=dict(size=22))
    return fig


def fig_2h_tramitacao_anual_2020(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    return _tramitacao_anual(df, 2020, 2025, show_values,
                              "A tramitação exclusivamente virtual domina desde 2020",
                              "Tramitação por ambiente e ano, 2020–2025")


def fig_2i_tramitacao_anual_2016(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    return _tramitacao_anual(df, 2016, 2025, show_values,
                              "A tramitação só-presencial recua ano a ano desde 2016",
                              "Tramitação por ambiente e ano, 2016–2025")


# ── 2.j / 2.j2 ───────────────────────────────────────────────────────────────
def _recursos(df: pd.DataFrame, ano_ini: int, ano_fim: int, show_values: bool, titulo: str, subtitulo: str) -> go.Figure:
    sub = df[(df["tipo_questao"] == "RC") & df["ano"].between(ano_ini, ano_fim)]
    vc = sub["ambiente"].value_counts()
    total = vc.sum()
    pv_n, pp_n = int(vc.get("Plenário Virtual", 0)), int(vc.get("Plenário Presencial", 0))
    pv_pct, pp_pct = 100 * pv_n / total, 100 * pp_n / total

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=["Recursos"], x=[pv_pct], name="Plenário Virtual", orientation="h", marker_color=COR_PV,
        text=f"PV: {pv_pct:.1f}% ({br(pv_n)})".replace(".", ",", 1) if show_values else None,
        textposition="inside", insidetextanchor="middle", textfont=dict(color="white", size=13, weight="bold"),
    ))
    fig.add_trace(go.Bar(
        y=["Recursos"], x=[pp_pct], name="Plenário Presencial", orientation="h", marker_color=COR_PP,
        text=f"PP: {pp_pct:.1f}% ({br(pp_n)})".replace(".", ",", 1) if show_values else None,
        textposition="outside", textfont=dict(color="black", size=13, weight="bold"),
    ))
    return aplicar_padrao(
        fig, titulo, subtitulo,
        xaxis=dict(title="%"), yaxis=dict(title=""),
        barmode="stack", showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.3, x=0.5, xanchor="center"),
        height=320,
    )


def fig_2j_recursos_2020(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    return _recursos(df, 2020, 2025, show_values,
                      "A atividade recursal migrou quase integralmente para o ambiente virtual",
                      "Destino das inclusões em pauta de recursos, 2020–2025")


def fig_2j2_recursos_2016(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    return _recursos(df, 2016, 2019, show_values,
                      "Já em 2016-2019, os recursos concentravam-se no ambiente virtual",
                      "Destino das inclusões em pauta de recursos, 2016–2019")


# ── 2.k1 / 2.k2 ──────────────────────────────────────────────────────────────
def _tipo_ambiente(df: pd.DataFrame, ano_ini: int, ano_fim: int, show_values: bool, titulo: str, subtitulo: str) -> go.Figure:
    sub = df[df["ano"].between(ano_ini, ano_fim) & df["tipo_questao"].isin(["PR", "RC", "IJ"])]
    tab = sub.groupby(["tipo_questao", "ambiente"]).size().unstack(fill_value=0).reindex(index=["PR", "RC", "IJ"])
    tipos = tab.index.tolist()

    fig = go.Figure()
    for amb, cor in [("Plenário Virtual", COR_PV), ("Plenário Presencial", COR_PP)]:
        fig.add_trace(go.Bar(
            x=tipos, y=tab[amb], name=amb, marker_color=cor,
            text=[br(v) for v in tab[amb]] if show_values else None,
            textposition="outside", textfont=dict(color="black", size=12, weight="bold"),
            cliponaxis=False,
        ))
    return aplicar_padrao(
        fig, titulo, subtitulo,
        xaxis=dict(title="Tipo de questão"), yaxis=dict(title="Inclusões"),
        barmode="group", showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.5, xanchor="center"),
    )


def fig_2k1_tipo_ambiente_2016(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    return _tipo_ambiente(df, 2016, 2019, show_values,
                           "O virtual dedica-se apenas à atividade recursal",
                           "Tipo de questão por ambiente, 2016–2019")


def fig_2k2_tipo_ambiente_2020(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    return _tipo_ambiente(df, 2020, 2025, show_values,
                           "O presencial dedica-se aos processos principais; o recurso migrou para o virtual",
                           "Tipo de questão por ambiente, 2020–2025")


# ── 2.l ──────────────────────────────────────────────────────────────────────
def fig_2l_pauta_vs_concluidos(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    sub = df[df["ano"].between(2020, 2025)]
    pct_pauta = 100 * (sub["ambiente"] == "Plenário Virtual").mean()
    concl = sub[sub["desfecho"].str.startswith("Concluído")]
    pct_concl = 100 * (concl["ambiente"] == "Plenário Virtual").mean()

    categorias = ["Participação<br>na pauta", "Participação nos<br>julgamentos concluídos"]
    valores = [pct_pauta, pct_concl]
    fig = go.Figure(go.Bar(
        x=categorias, y=valores, marker_color=COR_PV,
        text=[f"{v:.1f}%".replace(".", ",") for v in valores] if show_values else None,
        textposition="outside", textfont=dict(color="black", size=14, weight="bold"), cliponaxis=False,
    ))
    return aplicar_padrao(
        fig, "O Plenário Virtual concentra os julgamentos concluídos",
        "Participação do PV na pauta e nos julgamentos concluídos, 2020–2025",
        xaxis=dict(title=""), yaxis=dict(title="%", range=[0, 110]),
    )


# ── 2.m / 2.n ────────────────────────────────────────────────────────────────
def _categoria_ano(df: pd.DataFrame, ambiente: str, show_values: bool, titulo: str, subtitulo: str) -> go.Figure:
    sub = df[(df["ambiente"] == ambiente) & df["ano"].between(2020, 2025)].copy()
    sub["categoria"] = sub["desfecho"].apply(_categoria)
    cats = ["Unânime", "Maioria (relator vencedor)", "Maioria (relator vencido)", "Não concluído"]
    tab = sub.groupby(["ano", "categoria"]).size().unstack(fill_value=0).reindex(columns=cats, fill_value=0)
    anos = [str(a) for a in tab.index]

    fig = go.Figure()
    for cat in cats:
        fig.add_trace(go.Bar(
            x=anos, y=tab[cat], name=cat, marker_color=_CORES_CATEGORIA[cat],
            text=[br(v) for v in tab[cat]] if show_values else None,
            textposition="outside", textfont=dict(color="black", size=9, weight="bold"),
            cliponaxis=False,
        ))
    fig = aplicar_padrao(
        fig, titulo, subtitulo,
        xaxis=dict(title="Ano"), yaxis=dict(title="Inclusões", range=[0, 600]),
        barmode="group", showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.05, x=0.5, xanchor="center"),
    )
    fig.update_xaxes(tickfont=dict(size=22), title_font=dict(size=22))
    return fig


def fig_2m_categoria_ano_pv(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    return _categoria_ano(df, "Plenário Virtual", show_values,
                           "No virtual, a unanimidade domina o desfecho ano após ano",
                           "Desfecho por categoria e ano — Plenário Virtual, 2020–2025")


def fig_2n_categoria_ano_pp(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    return _categoria_ano(df, "Plenário Presencial", show_values,
                           "No presencial, o não concluído domina em todos os anos",
                           "Desfecho por categoria e ano — Plenário Presencial, 2020–2025")


# ── 2.o / 2.p ────────────────────────────────────────────────────────────────
def _nc_categoria_ano(df: pd.DataFrame, ambiente: str, show_values: bool, titulo: str, subtitulo: str) -> go.Figure:
    sub = df[(df["ambiente"] == ambiente) & df["ano"].between(2020, 2025) & df["desfecho"].str.startswith("Não concluído")].copy()
    sub["categoria_nc"] = sub["desfecho"].apply(_categoria_nc)
    cats = ["Pedido de vista", "Destaque", "Retirado de pauta", "Motivos diversos"]
    tab = sub.groupby(["ano", "categoria_nc"]).size().unstack(fill_value=0).reindex(columns=cats, fill_value=0)
    anos = [str(a) for a in tab.index]

    fig = go.Figure()
    for cat in cats:
        fig.add_trace(go.Bar(
            x=anos, y=tab[cat], name=cat, marker_color=_CORES_NC[cat],
            text=[br(v) for v in tab[cat]] if show_values else None,
            textposition="outside", textfont=dict(color="black", size=9, weight="bold"),
            cliponaxis=False,
        ))
    fig = aplicar_padrao(
        fig, titulo, subtitulo,
        xaxis=dict(title="Ano"), yaxis=dict(title="Inclusões", range=[0, 450]),
        barmode="group", showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.5, xanchor="center"),
    )
    fig.update_xaxes(tickfont=dict(size=22), title_font=dict(size=22))
    return fig


def fig_2o_nc_categoria_ano_pv(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    return _nc_categoria_ano(df, "Plenário Virtual", show_values,
                              "Pedido de vista é o principal motivo de não conclusão no virtual",
                              "Não concluídos por categoria e ano — Plenário Virtual, 2020–2025")


def fig_2p_nc_categoria_ano_pp(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    return _nc_categoria_ano(df, "Plenário Presencial", show_values,
                              "Motivos diversos dominam a não conclusão no presencial",
                              "Não concluídos por categoria e ano — Plenário Presencial, 2020–2025")


# ── 2.q / 2.r ────────────────────────────────────────────────────────────────
def fig_2q_media_por_processo(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    sub = df[df["ano"].between(2020, 2025)]
    medias = sub.groupby("ambiente").apply(lambda d: len(d) / d["incidente"].nunique())
    categorias = ["Plenário Virtual", "Plenário Presencial"]
    valores = [medias["Plenário Virtual"], medias["Plenário Presencial"]]

    fig = go.Figure(go.Bar(
        x=categorias, y=valores, marker_color=[COR_PV, COR_PP],
        text=[br(v, 1) for v in valores] if show_values else None,
        textposition="outside", textfont=dict(color="black", size=14, weight="bold"), cliponaxis=False,
    ))
    return aplicar_padrao(
        fig, "Cada julgamento presencial consome mais que o dobro de inclusões",
        "Média de inclusões em pauta por processo, 2020–2025",
        xaxis=dict(title=""), yaxis=dict(title="Inclusões por processo", range=[0, 5.5]),
    )


def fig_2r_pct_concluidos(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    sub = df[df["ano"].between(2020, 2025)]

    def pct_concl(d):
        return 100 * d.groupby("incidente")["desfecho"].apply(lambda s: s.str.startswith("Concluído").any()).mean()

    valores = [pct_concl(sub[sub["ambiente"] == "Plenário Virtual"]), pct_concl(sub[sub["ambiente"] == "Plenário Presencial"])]
    categorias = ["Plenário Virtual", "Plenário Presencial"]

    fig = go.Figure(go.Bar(
        x=categorias, y=valores, marker_color=[COR_PV, COR_PP],
        text=[f"{v:.1f}%".replace(".", ",") for v in valores] if show_values else None,
        textposition="outside", textfont=dict(color="black", size=14, weight="bold"), cliponaxis=False,
    ))
    return aplicar_padrao(
        fig, "Considerado o processo, o ambiente virtual conclui 86% do que pauta",
        "Percentual de processos pautados com julgamento concluído, 2020–2025",
        xaxis=dict(title=""), yaxis=dict(title="%", range=[0, 105]),
    )


# ── 3.1 / 3.2 ────────────────────────────────────────────────────────────────
def _tramitacao_periodo(df: pd.DataFrame, ano_ini: int, ano_fim: int, show_values: bool, titulo: str, subtitulo: str) -> go.Figure:
    tram = _tramitacao_por_processo(df, ano_ini, ano_fim)
    vc = tram.value_counts().reindex(["Somente Virtual", "Ambos", "Somente Presencial"], fill_value=0)
    total = vc.sum()
    pct = 100 * vc / total
    cores = [COR_PV if "Virtual" in s else COR_PP if "Presencial" in s else AZUL_CLARO for s in vc.index]
    fig = go.Figure(go.Bar(
        y=vc.index, x=vc.values, orientation="h", marker_color=cores,
        text=[f"{br(n)} ({p:.1f}%)".replace(".", ",", 1) for n, p in zip(vc.values, pct.values)] if show_values else None,
        textposition="outside", textfont=dict(color="black", size=20, weight="bold"), cliponaxis=False,
    ))
    fig = aplicar_padrao(
        fig, titulo, subtitulo,
        xaxis=dict(title="", range=[0, vc.max() * 1.25]), yaxis=dict(title=""),
        height=340,
    )
    fig.update_xaxes(tickfont=dict(size=20))
    fig.update_yaxes(tickfont=dict(size=20), categoryorder="total descending")
    return fig


def fig_31_tramitacao_2016(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    return _tramitacao_periodo(df, 2016, 2019, show_values,
                                "Antes da universalização, a maioria dos processos era só presencial",
                                "Tramitação por ambiente, por período (2016–2019)")


def fig_32_tramitacao_2020(df: pd.DataFrame, show_values: bool = True) -> go.Figure:
    return _tramitacao_periodo(df, 2020, 2025, show_values,
                                "Três de cada quatro processos nunca passam pelo Plenário Presencial",
                                "Tramitação por ambiente, por período (2020–2025)")


fig_2g_tramitacao_periodo_2020 = fig_32_tramitacao_2020  # alias
