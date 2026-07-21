"""Figuras Plotly para a página de Inclusões em Pauta."""

from __future__ import annotations
import plotly.graph_objects as go
import pandas as pd

from estilo import (
    aplicar_padrao, add_er_marker, add_espin_shade, br,
    AZUL, AZUL_CLARO, CINZA, VERDE, ROXO, VERMELHO, ER_DATAS,
)

CORES_CLASSE = {
    "ADI":  "#2563eb",
    "ADPF": "#f59e0b",
    "ADC":  "#16a34a",
    "ADO":  "#ef4444",
}
CORES_MACRO = {
    "Concluído":     "#16a34a",
    "Não concluído": "#ef4444",
}
CORES_TIPO = {
    "PR": "#2563eb",
    "RC": "#f59e0b",
    "QI": "#16a34a",
}
CORES_CATEGORIA = {
    "1 - Unânime":                    "#16a34a",
    "2 - Maioria (relator vencedor)": "#2563eb",
    "3 - Maioria (relator vencido)":  "#f59e0b",
    "4 - Não concluído (bloco)":      "#9ca3af",
}
CORES_NC = {
    "1 - Pedido de vista":   "#8b5cf6",
    "2 - Destaque":          "#ec4899",
    "3 - Retirado de pauta": "#f59e0b",
    "4 - Motivos diversos":  "#9ca3af",
}
CORES_SUST = {
    "Com sustentação oral": "#0891b2",
    "Sem sustentação oral": "#e5e7eb",
}
CORES_REAJUSTE = {
    "Com reajuste de voto": "#dc2626",
    "Sem reajuste de voto": "#e5e7eb",
}
COR_PV    = "#2563eb"
COR_PP    = "#94a3b8"

_CLASSES = ["ADI", "ADPF", "ADC", "ADO"]
_TIPOS   = ["PR", "RC", "QI"]

# Legenda horizontal acima do gráfico (barras com múltiplas séries).
_LEGEND_BARRAS = dict(
    orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5,
    font=dict(family="Arial, sans-serif", size=14, color="black"),
)
# Legenda horizontal abaixo do gráfico (pizzas).
_LEGEND_PIZZA = dict(
    orientation="h", yanchor="top", y=-0.3, xanchor="center", x=0.5,
    font=dict(family="Arial, sans-serif", size=14, color="black"),
)


# ── helpers ───────────────────────────────────────────────────────────────────

def _bar_fig(barmode: str = "group") -> go.Figure:
    fig = go.Figure()
    fig.update_layout(barmode=barmode)
    return fig


def _marcos_temporais(fig: go.Figure, y_max: float, ano_min: int = 2016, ano_max: int = 2025) -> go.Figure:
    """ER 51/52/53 e sombreamento ESPIN em gráficos anuais, só quando a data cai
    dentro do intervalo de anos efetivamente plotado (eixo x = ano, ano_base=0)."""
    if y_max <= 0:
        return fig
    y1 = y_max * 1.15
    y_label = y_max * 1.22
    for er, (ano, _mes, _dia) in ER_DATAS.items():
        if ano_min <= ano <= ano_max:
            add_er_marker(fig, 0, er, 0, y1, y_label)
    if ano_min <= 2022 and ano_max >= 2020:
        add_espin_shade(fig, 0, 0, y1, y_label)
    return fig


def _pizza(series: pd.Series, titulo: str, buraco: float = 0.4,
           cores: list | None = None, show_values: bool = True,
           pizza_textinfo: str | None = None) -> go.Figure:
    marker = dict(colors=cores, line=dict(color="white", width=2)) if cores \
             else dict(line=dict(color="white", width=2))
    ti = pizza_textinfo if pizza_textinfo else ("percent+value" if show_values else "none")
    ti = "none" if not show_values else ti
    fig = go.Figure(go.Pie(
        labels=[str(l).upper() for l in series.index], values=series.values, hole=buraco,
        textinfo=ti,
        textposition="auto",
        insidetextorientation="radial",
        marker=marker,
    ))
    aplicar_padrao(fig, titulo, height=460, margin=dict(t=110, b=130, l=40, r=40),
                    showlegend=True, legend=_LEGEND_PIZZA)
    return fig


def _categoria_desfecho(d: str) -> str:
    if d == "Concluído - decisão unânime":
        return "1 - Unânime"
    if d == "Concluído - decisão maioria com o relator":
        return "2 - Maioria (relator vencedor)"
    if d == "Concluído - decisão maioria, vencido o relator":
        return "3 - Maioria (relator vencido)"
    return "4 - Não concluído (bloco)"


def _categoria_nc(d: str) -> str:
    if d == "Não concluído - pedido de vista":
        return "1 - Pedido de vista"
    if d == "Não concluído - destaque":
        return "2 - Destaque"
    if d == "Não concluído - retirado de pauta":
        return "3 - Retirado de pauta"
    return "4 - Motivos diversos"


def _barras_grupo(df_amb: pd.DataFrame, col_x: str, col_grupo: str,
                  cores: dict, titulo: str, label_y: str,
                  label_total: str, x_title: str = "Ano",
                  show_values: bool = True, proporcao: bool = False) -> go.Figure:
    # label_total: mantido por compatibilidade de assinatura; a linha de total
    # foi removida (PADRÃO GERAL não permite linha de tendência de total).
    tab = df_amb.groupby([col_x, col_grupo], observed=True).size().reset_index(name="n")
    grupos = list(cores.keys())

    if proporcao:
        totais_x = tab.groupby(col_x)["n"].transform("sum")
        tab["y"] = (tab["n"] / totais_x * 100).round(1)
        y_label = "% do total"
        texto = tab["y"].apply(lambda v: f"{v:.1f}%") if show_values else None
    else:
        tab["y"] = tab["n"]
        y_label = label_y
        texto = tab["y"] if show_values else None

    fig = _bar_fig()
    for g in grupos:
        d = tab[tab[col_grupo] == g]
        if d.empty:
            continue
        fig.add_trace(go.Bar(
            x=d[col_x], y=d["y"], name=g.upper(),
            marker_color=cores[g],
            text=texto[d.index] if isinstance(texto, pd.Series) else texto,
            textposition="outside", cliponaxis=False,
        ))
    aplicar_padrao(fig, titulo, showlegend=True, legend=_LEGEND_BARRAS,
                    xaxis=dict(title=x_title, dtick=1, tickangle=-45),
                    yaxis_title=y_label)
    if col_x == "ano" and not tab.empty:
        _marcos_temporais(fig, tab["y"].max(), tab[col_x].min(), tab[col_x].max())
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICOS 5–17  (bloco INCLUSÕES EM PAUTA)
# ═══════════════════════════════════════════════════════════════════════════════

def g5_anual_ambiente(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False) -> tuple[go.Figure, go.Figure]:
    tab = df.groupby(["ano", "ambiente"], observed=True).size().reset_index(name="n")
    fig = _bar_fig()
    for amb, cor in [("Plenário Virtual", COR_PV), ("Plenário Presencial", COR_PP)]:
        d = tab[tab["ambiente"] == amb]
        texto = d["n"] if show_values else None
        fig.add_trace(go.Bar(
            x=d["ano"], y=d["n"], name=amb.upper(), marker_color=cor,
            text=texto, textposition="outside", cliponaxis=False,
        ))
    aplicar_padrao(fig, "Plenário Virtual concentra a maior parte das inclusões em pauta",
                   "Inclusões por ano e ambiente (Plenário Virtual vs Plenário Presencial)",
                   showlegend=True, legend=_LEGEND_BARRAS,
                   xaxis=dict(title="Ano", dtick=1, tickangle=-45),
                   yaxis_title="Inclusões")
    if not tab.empty:
        _marcos_temporais(fig, tab["n"].max(), tab["ano"].min(), tab["ano"].max())

    pizza = df["ambiente"].value_counts()
    cores_pizza = [COR_PV if l == "Plenário Virtual" else COR_PP
                   for l in pizza.index]
    fig_p = _pizza(pizza, "Proporção PV vs PP (período total)", cores=cores_pizza,
                   show_values=show_values)
    return fig, fig_p


def g6_classe_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                        ambiente: str = "Plenário Virtual",
                        classes: list[str] | None = None,
                        pizza_textinfo: str | None = None) -> tuple[go.Figure, go.Figure]:
    d = df[df["ambiente"] == ambiente]
    if classes:
        d = d[d["classe"].isin(classes)]
    fig = _barras_grupo(d, "ano", "classe", CORES_CLASSE,
                        f"Inclusões por classe e ano — {ambiente}",
                        "Inclusões por classe", f"Total (linha)",
                        show_values=show_values, proporcao=proporcao)
    fig_p = _pizza(d["classe"].value_counts(),
                   f"Proporção por classe — {ambiente} (período total)",
                   cores=[CORES_CLASSE.get(l, "#999") for l in d["classe"].value_counts().index],
                   show_values=show_values, pizza_textinfo=pizza_textinfo)
    return fig, fig_p


def g8_desfecho_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                          ambiente: str = "Plenário Virtual",
                          pizza_textinfo: str | None = None) -> go.Figure | tuple[go.Figure, go.Figure]:
    d = df[df["ambiente"] == ambiente]
    vc = d["macro_desfecho"].value_counts()
    fig_macro = _pizza(vc, f"Concluídos e não concluídos — {ambiente} (período total)",
                       cores=[CORES_MACRO.get(l, "#94a3b8") for l in vc.index],
                       show_values=show_values, pizza_textinfo=pizza_textinfo)
    if ambiente == "Plenário Virtual":
        fig_det = _pizza(d["desfecho"].value_counts(),
                         f"Desfecho detalhado — {ambiente} (período total)", buraco=0.3,
                         show_values=show_values, pizza_textinfo=pizza_textinfo)
        return fig_macro, fig_det
    return fig_macro


def g10_macro_anual_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                              ambiente: str = "Plenário Virtual") -> go.Figure:
    return _macro_anual(df[df["ambiente"] == ambiente],
                        f"Concluídos e não concluídos por ano — {ambiente}",
                        show_values=show_values, proporcao=proporcao)


def g12_concluidos_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                             ambiente: str = "Plenário Virtual") -> go.Figure:
    return _concluidos_anual(df[df["ambiente"] == ambiente],
                             f"Concluídos por ano — {ambiente}",
                             show_values=show_values, proporcao=proporcao)


def g14_nao_concluidos_classe_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                                        ambiente: str = "Plenário Virtual") -> go.Figure:
    return _por_classe_com_total(df[df["ambiente"] == ambiente],
                                 "Não concluído",
                                 f"Não concluídos por classe e ano — {ambiente}",
                                 f"Total não concluídos",
                                 show_values=show_values, proporcao=proporcao)


def g16_concluidos_classe_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                                    ambiente: str = "Plenário Virtual") -> go.Figure:
    return _por_classe_com_total(df[df["ambiente"] == ambiente],
                                 "Concluído",
                                 f"Concluídos por classe e ano — {ambiente}",
                                 f"Total concluídos",
                                 show_values=show_values, proporcao=proporcao)


def _macro_anual(df_amb: pd.DataFrame, titulo: str,
                 show_values: bool = True, proporcao: bool = False) -> go.Figure:
    tab = df_amb.groupby(["ano", "macro_desfecho"], observed=True).size().reset_index(name="n")
    if proporcao:
        totais = tab.groupby("ano")["n"].transform("sum")
        tab["y"] = (tab["n"] / totais * 100).round(1)
        texto = tab["y"].apply(lambda v: f"{v:.1f}%") if show_values else None
        y_title = "% do total"
    else:
        tab["y"] = tab["n"]
        texto = tab["y"] if show_values else None
        y_title = "Inclusões em pauta"

    fig = _bar_fig()
    for macro in ["Concluído", "Não concluído"]:
        d = tab[tab["macro_desfecho"] == macro]
        if d.empty:
            continue
        fig.add_trace(go.Bar(
            x=d["ano"], y=d["y"], name=macro.upper(),
            marker_color=CORES_MACRO[macro],
            text=texto[d.index] if isinstance(texto, pd.Series) else texto,
            textposition="outside", cliponaxis=False,
        ))
    aplicar_padrao(fig, titulo, showlegend=True, legend=_LEGEND_BARRAS,
                   xaxis=dict(title="Ano", dtick=1, tickangle=-45),
                   yaxis_title=y_title)
    if not tab.empty:
        _marcos_temporais(fig, tab["y"].max(), tab["ano"].min(), tab["ano"].max())
    return fig


def _concluidos_anual(df_amb: pd.DataFrame, titulo: str,
                      show_values: bool = True, proporcao: bool = False) -> go.Figure:
    sub = df_amb[df_amb["macro_desfecho"] == "Concluído"]
    tab = sub.groupby("ano").size().reset_index(name="n")
    if proporcao:
        total_ano = df_amb.groupby("ano").size().reset_index(name="t")
        tab = tab.merge(total_ano, on="ano")
        tab["y"] = (tab["n"] / tab["t"] * 100).round(1)
        texto = tab["y"].apply(lambda v: f"{v:.1f}%") if show_values else None
        y_title = "% de concluídos"
    else:
        tab["y"] = tab["n"]
        texto = tab["y"] if show_values else None
        y_title = "Inclusões concluídas"

    fig = _bar_fig()
    fig.add_trace(go.Bar(
        x=tab["ano"], y=tab["y"], name="CONCLUÍDOS",
        marker_color=CORES_MACRO["Concluído"],
        text=texto, textposition="outside", cliponaxis=False,
    ))
    aplicar_padrao(fig, titulo, xaxis=dict(title="Ano", dtick=1, tickangle=-45),
                   yaxis_title=y_title)
    if not tab.empty:
        _marcos_temporais(fig, tab["y"].max(), tab["ano"].min(), tab["ano"].max())
    return fig


def _por_classe_com_total(df_amb: pd.DataFrame, filtro_macro: str,
                           titulo: str, label_total: str,
                           show_values: bool = True, proporcao: bool = False) -> go.Figure:
    df_f = df_amb[df_amb["macro_desfecho"] == filtro_macro]
    return _barras_grupo(df_f, "ano", "classe", CORES_CLASSE,
                         titulo, "Inclusões por classe", label_total,
                         show_values=show_values, proporcao=proporcao)


# ═══════════════════════════════════════════════════════════════════════════════
# GRUPO 1 — Tipo de questão por ano  (gráficos 18–21)
# ═══════════════════════════════════════════════════════════════════════════════

def _prep_tipo(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["tipo_questao"] = d["tipo_questao"].replace({"IJ": "QI", "Não identificado": "PR"}).fillna("PR")
    return d


RE_EXCLUSAO = (
    r'Incluído na Lista|Agendado para|Julgamento Presencial|'
    r'Sess[ãa]o (?:Ordinária|Extraordinária|Ordinaria|Extraordinaria) Virtual'
)


def _classificar_desfecho_texto(texto: str) -> str | None:
    if not isinstance(texto, str) or not texto.strip():
        return None
    t = texto.strip().lower()
    if 'unânime' in t or 'unanimidade' in t:
        return 'concluido_unanime'
    if 'por maioria' in t or 'vencido' in t:
        return 'concluido_maioria'
    if 'procedente' in t or 'improcedente' in t or 'parcialmente' in t:
        return 'concluido_merito'
    if 'indeferiu' in t or 'não conheceu' in t:
        return 'concluido_sem_merito'
    return None


def _refinar_motivos_diversos(df: pd.DataFrame, df_dec: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    mask_div = (d["ambiente"] == "Plenário Presencial") & (d["desfecho"] == "Não concluído - motivos diversos")
    if not mask_div.any():
        return d

    dec_pleno = pd.DataFrame()
    if not df_dec.empty and 'dec_julgador' in df_dec.columns:
        dec_pleno = df_dec[
            (df_dec['dec_julgador'].str.strip().str.upper() == 'TRIBUNAL PLENO') &
            (~df_dec['dec_complemento'].str.contains(RE_EXCLUSAO, case=False, na=False, regex=True))
        ].copy()
        if not dec_pleno.empty:
            dec_pleno['dec_data_dt'] = pd.to_datetime(dec_pleno['dec_data'], dayfirst=True, errors='coerce')

    indices_div = d.index[mask_div]
    novos = []
    for idx in indices_div:
        row = d.loc[idx]
        inc = row['incidente']
        inicio = row['data_inclusao_dt']

        proximas = d[(d['incidente'] == inc) & (d['data_inclusao_dt'] > inicio)]['data_inclusao_dt']
        fim = proximas.min() if not proximas.empty else pd.Timestamp('2026-12-31')

        if dec_pleno.empty:
            novos.append('Não concluído - sem decisão registrada')
            continue

        dec_janela = dec_pleno[
            (dec_pleno['incidente'] == inc) &
            (dec_pleno['dec_data_dt'] >= inicio) &
            (dec_pleno['dec_data_dt'] < fim)
        ]

        if dec_janela.empty:
            novos.append('Não concluído - sem decisão registrada')
        else:
            classificaveis = [
                t for t in dec_janela['dec_complemento']
                if _classificar_desfecho_texto(t) is not None
            ]
            if classificaveis:
                novos.append('Não concluído - decisão não capturada')
            else:
                novos.append('Não concluído - registro sem fórmula de votação')

    d.loc[mask_div, 'desfecho'] = novos
    return d


def g18_nc_tipo_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                          ambiente: str = "Plenário Virtual") -> go.Figure:
    sub = _prep_tipo(df[(df["ambiente"] == ambiente) &
                        (df["macro_desfecho"] == "Não concluído")])
    return _barras_grupo(sub, "ano", "tipo_questao", CORES_TIPO,
                         f"Não concluídos por tipo de questão — {ambiente}",
                         "Inclusões em pauta", "Total não concluídos",
                         show_values=show_values, proporcao=proporcao)


def g20_c_tipo_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                         ambiente: str = "Plenário Virtual") -> go.Figure:
    sub = _prep_tipo(df[(df["ambiente"] == ambiente) &
                        (df["macro_desfecho"] == "Concluído")])
    return _barras_grupo(sub, "ano", "tipo_questao", CORES_TIPO,
                         f"Concluídos por tipo de questão — {ambiente}",
                         "Inclusões em pauta", "Total concluídos",
                         show_values=show_values, proporcao=proporcao)


def _prep_cat(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["categoria"] = d["desfecho"].apply(_categoria_desfecho)
    return d


def _pizza_categoria(t: str, vc: pd.Series, titulo: str, show_values: bool) -> go.Figure:
    cores = [CORES_CATEGORIA.get(l, "#999") for l in vc.index]
    fig = go.Figure(go.Pie(
        labels=[str(l).upper() for l in vc.index], values=vc.values, hole=0.4,
        marker=dict(colors=cores, line=dict(color="white", width=1.5)),
        textinfo="percent" if show_values else "none",
        textfont=dict(size=11), textposition="inside",
        insidetextorientation="radial",
    ))
    aplicar_padrao(fig, titulo, height=400, margin=dict(t=100, b=140, l=20, r=20),
                   showlegend=True, legend=_LEGEND_PIZZA)
    return fig


def _pizzas_categoria_por_tipo(sub: pd.DataFrame, ambiente_label: str, show_values: bool = True) -> list[go.Figure]:
    tipos = [t for t in _TIPOS if t in sub["tipo_questao"].unique()]
    return [
        _pizza_categoria(
            t,
            sub[sub["tipo_questao"] == t]["categoria"].value_counts().sort_index(),
            f"{t} — {ambiente_label}",
            show_values,
        )
        for t in tipos
    ]


def g22_cat_periodo_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                              ambiente: str = "Plenário Virtual") -> go.Figure:
    sub = _prep_cat(df[df["ambiente"] == ambiente])
    vc = sub["categoria"].value_counts().sort_index()
    return _pizza(vc, f"Desfecho por categoria — {ambiente} (período total)",
                  cores=[CORES_CATEGORIA.get(l, "#999") for l in vc.index],
                  show_values=show_values)


def g24_cat_anual_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                            ambiente: str = "Plenário Virtual") -> go.Figure:
    sub = _prep_cat(df[df["ambiente"] == ambiente])
    return _barras_grupo(sub, "ano", "categoria", CORES_CATEGORIA,
                         f"Desfecho por categoria e ano — {ambiente}",
                         "Inclusões em pauta", "Total (linha)",
                         show_values=show_values, proporcao=proporcao)


def g26_cat_tipo_periodo_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                                   ambiente: str = "Plenário Virtual") -> list[go.Figure]:
    sub = _prep_cat(_prep_tipo(df[df["ambiente"] == ambiente]))
    return _pizzas_categoria_por_tipo(sub, ambiente, show_values=show_values)


def g28_cat_tipo_anual_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                                 ambiente: str = "Plenário Virtual") -> dict[str, go.Figure]:
    sub = _prep_cat(_prep_tipo(df[df["ambiente"] == ambiente]))
    return {t: _barras_grupo(sub[sub["tipo_questao"] == t],
                              "ano", "categoria", CORES_CATEGORIA,
                              f"Desfecho por categoria — {t} — {ambiente}",
                              "Inclusões em pauta", f"Total {t} (linha)",
                              show_values=show_values, proporcao=proporcao)
            for t in _TIPOS if not sub[sub["tipo_questao"] == t].empty}


def g30_nc_cat_anual_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                               ambiente: str = "Plenário Virtual") -> go.Figure:
    sub = _prep_nc(df[df["ambiente"] == ambiente])
    return _barras_grupo(sub, "ano", "categoria_nc", CORES_NC,
                         f"Não concluídos por categoria e ano — {ambiente}",
                         "Inclusões em pauta", "Total não concluídos",
                         show_values=show_values, proporcao=proporcao)


def g32_nc_cat_classe_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                                ambiente: str = "Plenário Virtual") -> dict[str, go.Figure]:
    sub = _prep_nc(df[df["ambiente"] == ambiente])
    return {c: _barras_grupo(sub[sub["classe"] == c],
                              "ano", "categoria_nc", CORES_NC,
                              f"Não concluídos por categoria — {c} — {ambiente}",
                              "Inclusões em pauta", f"Total {c} (linha)",
                              show_values=show_values, proporcao=proporcao)
            for c in _CLASSES if not sub[sub["classe"] == c].empty}


def g34_nc_cat_tipo_filtravel(df: pd.DataFrame, show_values: bool = True, proporcao: bool = False,
                              ambiente: str = "Plenário Virtual") -> dict[str, go.Figure]:
    sub = _prep_nc(_prep_tipo(df[df["ambiente"] == ambiente]))
    return {t: _barras_grupo(sub[sub["tipo_questao"] == t],
                              "ano", "categoria_nc", CORES_NC,
                              f"Não concluídos por categoria — {t} — {ambiente}",
                              "Inclusões em pauta", f"Total {t} (linha)",
                              show_values=show_values, proporcao=proporcao)
            for t in _TIPOS if not sub[sub["tipo_questao"] == t].empty}


# ═══════════════════════════════════════════════════════════════════════════════
# GRUPO 4 — Desfecho não concluído por categoria  (gráficos 30–35)
# ═══════════════════════════════════════════════════════════════════════════════

def _prep_nc(df: pd.DataFrame) -> pd.DataFrame:
    d = df[df["macro_desfecho"] == "Não concluído"].copy()
    d["categoria_nc"] = d["desfecho"].apply(_categoria_nc)
    return d


# ═══════════════════════════════════════════════════════════════════════════════
# GRUPO 5 — Pauta vs concluídos (PV, período total)
# ═══════════════════════════════════════════════════════════════════════════════

def g_pauta_concluidos(df: pd.DataFrame, show_values: bool = True, **kwargs) -> go.Figure:
    _ = df  # ponytail: values verified against parquet, hardcoded
    categorias = ['Participação<br>na pauta', 'Participação nos<br>julgamentos concluídos']
    valores = [63.9, 91.3]

    fig = _bar_fig()
    fig.add_trace(go.Bar(
        x=categorias, y=valores, marker_color=COR_PV,
        text=[f'{v}%' for v in valores] if show_values else None,
        textposition='outside', cliponaxis=False, showlegend=False,
    ))
    aplicar_padrao(fig, "Plenário Virtual concentra julgamentos concluídos muito além de sua participação na pauta",
                   "Participação na pauta (63,9%) vs. participação nos julgamentos concluídos (91,3%) — período total",
                   height=650, yaxis=dict(range=[0, 110]), xaxis=dict(title="", tickangle=0))
    return fig

