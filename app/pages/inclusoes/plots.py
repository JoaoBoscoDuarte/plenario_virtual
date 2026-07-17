"""Figuras Plotly para a página de Inclusões em Pauta."""

from __future__ import annotations
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

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
COR_LINHA = "#7f7f7f"
COR_PV    = "#2563eb"
COR_PP    = "#94a3b8"

_LEGEND = dict(
    orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
    font=dict(size=10, color="#333333"),
    bgcolor="#fcfcfc", bordercolor="#cccccc", borderwidth=1,
)
_LAYOUT = dict(
    template="plotly_white",
    height=500,
    margin=dict(t=120, b=80, l=60, r=60),
    legend=_LEGEND,
    xaxis=dict(dtick=1, title="Ano", tickangle=-45),
)
_CLASSES = ["ADI", "ADPF", "ADC", "ADO"]
_TIPOS   = ["PR", "RC", "QI"]


# ── helpers ───────────────────────────────────────────────────────────────────

def _bar_fig(barmode: str = "group") -> go.Figure:
    fig = go.Figure()
    fig.update_layout(**_LAYOUT, barmode=barmode)
    return fig


def _bar_com_linha(label_y: str, label_total: str,
                   x_title: str = "Ano") -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    layout = {**_LAYOUT, "xaxis": dict(dtick=1, title=x_title, tickangle=-45)}
    fig.update_layout(**layout, barmode="group")
    fig.update_yaxes(title_text=label_y, secondary_y=False)
    fig.update_yaxes(title_text=label_total, secondary_y=True)
    return fig


def _pizza(series: pd.Series, titulo: str, buraco: float = 0.4,
           cores: list | None = None) -> go.Figure:
    marker = dict(colors=cores, line=dict(color="white", width=2)) if cores \
             else dict(line=dict(color="white", width=2))
    fig = go.Figure(go.Pie(
        labels=series.index, values=series.values, hole=buraco,
        textinfo="label+percent+value",
        textposition="auto",
        insidetextorientation="radial",
        marker=marker,
    ))
    fig.update_layout(
        title_text=titulo, template="plotly_white", height=420,
        margin=dict(t=80, b=60), legend=_LEGEND,
    )
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
                  label_total: str, x_title: str = "Ano") -> go.Figure:
    """Barras agrupadas por col_grupo + linha do total no eixo secundário."""
    tab   = df_amb.groupby([col_x, col_grupo], observed=True).size().reset_index(name="n")
    total = df_amb.groupby(col_x, observed=True).size().reset_index(name="n")
    grupos = list(cores.keys())

    fig = _bar_com_linha(label_y, label_total, x_title=x_title)
    for g in grupos:
        d = tab[tab[col_grupo] == g]
        if d.empty:
            continue
        fig.add_trace(go.Bar(
            x=d[col_x], y=d["n"], name=g,
            marker_color=cores[g],
            text=d["n"], textposition="outside", cliponaxis=False,
        ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=total[col_x], y=total["n"], mode="lines+markers",
        line=dict(color=COR_LINHA, width=2), marker=dict(size=5),
        name=label_total,
    ), secondary_y=True)
    fig.update_layout(title_text=titulo)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICOS 5–17  (bloco INCLUSÕES EM PAUTA)
# ═══════════════════════════════════════════════════════════════════════════════

def g5_anual_ambiente(df: pd.DataFrame) -> tuple[go.Figure, go.Figure]:
    tab = df.groupby(["ano", "ambiente"], observed=True).size().reset_index(name="n")
    fig = _bar_fig()
    for amb, cor in [("Plenário Virtual", COR_PV), ("Plenário Físico", COR_PP)]:
        d = tab[tab["ambiente"] == amb]
        fig.add_trace(go.Bar(
            x=d["ano"], y=d["n"], name=amb, marker_color=cor,
            text=d["n"], textposition="outside", cliponaxis=False,
        ))
    fig.update_layout(title_text="Inclusões em Pauta por Ano e Ambiente")

    pizza = df["ambiente"].value_counts()
    cores_pizza = [COR_PV if l == "Plenário Virtual" else COR_PP
                   for l in pizza.index]
    fig_p = _pizza(pizza, "Proporção PV vs PP (período total)", cores=cores_pizza)
    return fig, fig_p


def g6_pv_por_classe(df: pd.DataFrame) -> tuple[go.Figure, go.Figure]:
    df_pv = df[df["ambiente"] == "Plenário Virtual"]
    fig = _barras_grupo(df_pv, "ano", "classe", CORES_CLASSE,
                        "Inclusões por Classe e Ano — Plenário Virtual",
                        "Inclusões por classe", "Total PV (Linha)")
    fig_p = _pizza(df_pv["classe"].value_counts(),
                   "Proporção por Classe — PV (período total)",
                   cores=[CORES_CLASSE.get(l, "#999") for l in df_pv["classe"].value_counts().index])
    return fig, fig_p


def g7_pp_por_classe(df: pd.DataFrame) -> tuple[go.Figure, go.Figure]:
    df_pp = df[df["ambiente"] == "Plenário Físico"]
    fig = _barras_grupo(df_pp, "ano", "classe", CORES_CLASSE,
                        "Inclusões por Classe e Ano — Plenário Físico",
                        "Inclusões por classe", "Total PP (Linha)")
    fig_p = _pizza(df_pp["classe"].value_counts(),
                   "Proporção por Classe — PP (período total)",
                   cores=[CORES_CLASSE.get(l, "#999") for l in df_pp["classe"].value_counts().index])
    return fig, fig_p


def g8_desfecho_pv(df: pd.DataFrame) -> tuple[go.Figure, go.Figure]:
    df_pv = df[df["ambiente"] == "Plenário Virtual"]
    vc = df_pv["macro_desfecho"].value_counts()
    fig_macro = _pizza(vc, "Concluídos e Não Concluídos — PV (período total)",
                       cores=[CORES_MACRO.get(l, "#94a3b8") for l in vc.index])
    fig_det = _pizza(df_pv["desfecho"].value_counts(),
                     "Desfecho Detalhado — PV (período total)", buraco=0.3)
    return fig_macro, fig_det


def g9_desfecho_pp(df: pd.DataFrame) -> go.Figure:
    df_pp = df[df["ambiente"] == "Plenário Físico"]
    vc = df_pp["macro_desfecho"].value_counts()
    return _pizza(vc, "Concluídos e Não Concluídos — PP (período total)",
                  cores=[CORES_MACRO.get(l, "#94a3b8") for l in vc.index])


def g10_macro_anual_pv(df: pd.DataFrame) -> go.Figure:
    return _macro_anual(df[df["ambiente"] == "Plenário Virtual"],
                        "Concluídos e Não Concluídos por Ano — PV")


def g11_macro_anual_pp(df: pd.DataFrame) -> go.Figure:
    return _macro_anual(df[df["ambiente"] == "Plenário Físico"],
                        "Concluídos e Não Concluídos por Ano — PP")


def _macro_anual(df_amb: pd.DataFrame, titulo: str) -> go.Figure:
    tab = df_amb.groupby(["ano", "macro_desfecho"], observed=True).size().reset_index(name="n")
    fig = _bar_fig()
    for macro in ["Concluído", "Não concluído"]:
        d = tab[tab["macro_desfecho"] == macro]
        if d.empty:
            continue
        fig.add_trace(go.Bar(
            x=d["ano"], y=d["n"], name=macro,
            marker_color=CORES_MACRO[macro],
            text=d["n"], textposition="outside", cliponaxis=False,
        ))
    fig.update_layout(title_text=titulo)
    return fig


def g12_concluidos_pv(df: pd.DataFrame) -> go.Figure:
    return _concluidos_anual(df[df["ambiente"] == "Plenário Virtual"],
                             "Concluídos por Ano — PV")


def g13_concluidos_pp(df: pd.DataFrame) -> go.Figure:
    return _concluidos_anual(df[df["ambiente"] == "Plenário Físico"],
                             "Concluídos por Ano — PP")


def _concluidos_anual(df_amb: pd.DataFrame, titulo: str) -> go.Figure:
    tab = (df_amb[df_amb["macro_desfecho"] == "Concluído"]
           .groupby("ano").size().reset_index(name="n"))
    fig = _bar_fig()
    fig.add_trace(go.Bar(
        x=tab["ano"], y=tab["n"], name="Concluídos",
        marker_color=CORES_MACRO["Concluído"],
        text=tab["n"], textposition="outside", cliponaxis=False,
    ))
    fig.update_layout(title_text=titulo, yaxis_title="Inclusões concluídas")
    return fig


def g14_nao_concluidos_classe_pv(df: pd.DataFrame) -> go.Figure:
    return _por_classe_com_total(df[df["ambiente"] == "Plenário Virtual"],
                                 "Não concluído",
                                 "Não Concluídos por Classe e Ano — PV",
                                 "Total Não Concluídos PV")


def g15_nao_concluidos_classe_pp(df: pd.DataFrame) -> go.Figure:
    return _por_classe_com_total(df[df["ambiente"] == "Plenário Físico"],
                                 "Não concluído",
                                 "Não Concluídos por Classe e Ano — PP",
                                 "Total Não Concluídos PP")


def g16_concluidos_classe_pv(df: pd.DataFrame) -> go.Figure:
    return _por_classe_com_total(df[df["ambiente"] == "Plenário Virtual"],
                                 "Concluído",
                                 "Concluídos por Classe e Ano — PV",
                                 "Total Concluídos PV")


def g17_concluidos_classe_pp(df: pd.DataFrame) -> go.Figure:
    return _por_classe_com_total(df[df["ambiente"] == "Plenário Físico"],
                                 "Concluído",
                                 "Concluídos por Classe e Ano — PP",
                                 "Total Concluídos PP")


def _por_classe_com_total(df_amb: pd.DataFrame, filtro_macro: str,
                           titulo: str, label_total: str) -> go.Figure:
    df_f = df_amb[df_amb["macro_desfecho"] == filtro_macro]
    return _barras_grupo(df_f, "ano", "classe", CORES_CLASSE,
                         titulo, "Inclusões por classe", label_total)


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
    mask_div = (d["ambiente"] == "Plenário Físico") & (d["desfecho"] == "Não concluído - motivos diversos")
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


def g18_nc_tipo_pv(df: pd.DataFrame) -> go.Figure:
    sub = _prep_tipo(df[(df["ambiente"] == "Plenário Virtual") &
                        (df["macro_desfecho"] == "Não concluído")])
    return _barras_grupo(sub, "ano", "tipo_questao", CORES_TIPO,
                         "Não Concluídos por Tipo de Questão — PV",
                         "Inclusões em pauta", "Total Não Concluídos PV")


def g19_nc_tipo_pp(df: pd.DataFrame) -> go.Figure:
    sub = _prep_tipo(df[(df["ambiente"] == "Plenário Físico") &
                        (df["macro_desfecho"] == "Não concluído")])
    return _barras_grupo(sub, "ano", "tipo_questao", CORES_TIPO,
                         "Não Concluídos por Tipo de Questão — PP",
                         "Inclusões em pauta", "Total Não Concluídos PP")


def g20_c_tipo_pv(df: pd.DataFrame) -> go.Figure:
    sub = _prep_tipo(df[(df["ambiente"] == "Plenário Virtual") &
                        (df["macro_desfecho"] == "Concluído")])
    return _barras_grupo(sub, "ano", "tipo_questao", CORES_TIPO,
                         "Concluídos por Tipo de Questão — PV",
                         "Inclusões em pauta", "Total Concluídos PV")


def g21_c_tipo_pp(df: pd.DataFrame) -> go.Figure:
    sub = _prep_tipo(df[(df["ambiente"] == "Plenário Físico") &
                        (df["macro_desfecho"] == "Concluído")])
    return _barras_grupo(sub, "ano", "tipo_questao", CORES_TIPO,
                         "Concluídos por Tipo de Questão — PP",
                         "Inclusões em pauta", "Total Concluídos PP")


# ═══════════════════════════════════════════════════════════════════════════════
# GRUPO 2 — Desfecho concluído por categoria  (gráficos 22–25)
# ═══════════════════════════════════════════════════════════════════════════════

def _prep_cat(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["categoria"] = d["desfecho"].apply(_categoria_desfecho)
    return d


def g22_cat_periodo_pv(df: pd.DataFrame) -> go.Figure:
    sub = _prep_cat(df[df["ambiente"] == "Plenário Virtual"])
    vc = sub["categoria"].value_counts().sort_index()
    return _pizza(vc, "Desfecho por Categoria — PV (período total)",
                  cores=[CORES_CATEGORIA.get(l, "#999") for l in vc.index])


def g23_cat_periodo_pp(df: pd.DataFrame) -> go.Figure:
    sub = _prep_cat(df[df["ambiente"] == "Plenário Físico"])
    vc = sub["categoria"].value_counts().sort_index()
    return _pizza(vc, "Desfecho por Categoria — PP (período total)",
                  cores=[CORES_CATEGORIA.get(l, "#999") for l in vc.index])


def g24_cat_anual_pv(df: pd.DataFrame) -> go.Figure:
    sub = _prep_cat(df[df["ambiente"] == "Plenário Virtual"])
    return _barras_grupo(sub, "ano", "categoria", CORES_CATEGORIA,
                         "Desfecho por Categoria e Ano — PV",
                         "Inclusões em pauta", "Total PV (Linha)")


def g25_cat_anual_pp(df: pd.DataFrame) -> go.Figure:
    sub = _prep_cat(df[df["ambiente"] == "Plenário Físico"])
    return _barras_grupo(sub, "ano", "categoria", CORES_CATEGORIA,
                         "Desfecho por Categoria e Ano — PP",
                         "Inclusões em pauta", "Total PP (Linha)")


# ═══════════════════════════════════════════════════════════════════════════════
# GRUPO 3 — Categoria × tipo de questão  (gráficos 26–29)
# ═══════════════════════════════════════════════════════════════════════════════

def _pizzas_categoria_por_tipo(sub: pd.DataFrame, ambiente_label: str) -> go.Figure:
    tipos = [t for t in _TIPOS if t in sub["tipo_questao"].unique()]
    n = len(tipos)
    fig = make_subplots(
        rows=1, cols=n,
        specs=[[{'type': 'domain'} for _ in range(n)]],
        subplot_titles=[f"{t}" for t in tipos],
    )
    for i, t in enumerate(tipos):
        vc = sub[sub["tipo_questao"] == t]["categoria"].value_counts().sort_index()
        cores = [CORES_CATEGORIA.get(l, "#999") for l in vc.index]
        fig.add_trace(go.Pie(
            labels=vc.index, values=vc.values, hole=0.4,
            marker=dict(colors=cores, line=dict(color="white", width=1.5)),
            textinfo="label+percent",
            textfont=dict(size=10),
            textposition="auto",
            insidetextorientation="radial",
            showlegend=i == 0,
            legendgroup="cat",
        ), row=1, col=i + 1)
    fig.update_layout(
        title_text=f"Desfecho por Categoria e Tipo de Questão — {ambiente_label} (período total)",
        template="plotly_white", height=420,
        margin=dict(t=100, b=40, l=40, r=40),
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.15,
            xanchor="center", x=0.5,
            font=dict(size=10), bgcolor="#fcfcfc",
        ),
    )
    return fig


def g26_cat_tipo_periodo_pv(df: pd.DataFrame) -> go.Figure:
    sub = _prep_cat(_prep_tipo(df[df["ambiente"] == "Plenário Virtual"]))
    return _pizzas_categoria_por_tipo(sub, "Plenário Virtual")


def g27_cat_tipo_periodo_pp(df: pd.DataFrame) -> go.Figure:
    sub = _prep_cat(_prep_tipo(df[df["ambiente"] == "Plenário Físico"]))
    return _pizzas_categoria_por_tipo(sub, "Plenário Físico")


def g28_cat_tipo_anual_pv(df: pd.DataFrame) -> dict[str, go.Figure]:
    """Retorna dict {tipo: figura} para PV."""
    sub = _prep_cat(_prep_tipo(df[df["ambiente"] == "Plenário Virtual"]))
    return {t: _barras_grupo(sub[sub["tipo_questao"] == t],
                              "ano", "categoria", CORES_CATEGORIA,
                              f"Desfecho por Categoria — {t} — PV",
                              "Inclusões em pauta", f"Total {t} PV (Linha)")
            for t in _TIPOS if not sub[sub["tipo_questao"] == t].empty}


def g29_cat_tipo_anual_pp(df: pd.DataFrame) -> dict[str, go.Figure]:
    """Retorna dict {tipo: figura} para PP."""
    sub = _prep_cat(_prep_tipo(df[df["ambiente"] == "Plenário Físico"]))
    return {t: _barras_grupo(sub[sub["tipo_questao"] == t],
                              "ano", "categoria", CORES_CATEGORIA,
                              f"Desfecho por Categoria — {t} — PP",
                              "Inclusões em pauta", f"Total {t} PP (Linha)")
            for t in _TIPOS if not sub[sub["tipo_questao"] == t].empty}


# ═══════════════════════════════════════════════════════════════════════════════
# GRUPO 4 — Desfecho não concluído por categoria  (gráficos 30–35)
# ═══════════════════════════════════════════════════════════════════════════════

def _prep_nc(df: pd.DataFrame) -> pd.DataFrame:
    d = df[df["macro_desfecho"] == "Não concluído"].copy()
    d["categoria_nc"] = d["desfecho"].apply(_categoria_nc)
    return d


def g30_nc_cat_anual_pv(df: pd.DataFrame) -> go.Figure:
    sub = _prep_nc(df[df["ambiente"] == "Plenário Virtual"])
    return _barras_grupo(sub, "ano", "categoria_nc", CORES_NC,
                         "Não Concluídos por Categoria e Ano — PV",
                         "Inclusões em pauta", "Total Não Concluídos PV")


def g31_nc_cat_anual_pp(df: pd.DataFrame) -> go.Figure:
    sub = _prep_nc(df[df["ambiente"] == "Plenário Físico"])
    return _barras_grupo(sub, "ano", "categoria_nc", CORES_NC,
                         "Não Concluídos por Categoria e Ano — PP",
                         "Inclusões em pauta", "Total Não Concluídos PP")


def g32_nc_cat_classe_pv(df: pd.DataFrame) -> dict[str, go.Figure]:
    """Retorna dict {classe: figura} para PV."""
    sub = _prep_nc(df[df["ambiente"] == "Plenário Virtual"])
    return {c: _barras_grupo(sub[sub["classe"] == c],
                              "ano", "categoria_nc", CORES_NC,
                              f"Não Concluídos por Categoria — {c} — PV",
                              "Inclusões em pauta", f"Total {c} PV (Linha)")
            for c in _CLASSES if not sub[sub["classe"] == c].empty}


def g33_nc_cat_classe_pp(df: pd.DataFrame) -> dict[str, go.Figure]:
    """Retorna dict {classe: figura} para PP."""
    sub = _prep_nc(df[df["ambiente"] == "Plenário Físico"])
    return {c: _barras_grupo(sub[sub["classe"] == c],
                              "ano", "categoria_nc", CORES_NC,
                              f"Não Concluídos por Categoria — {c} — PP",
                              "Inclusões em pauta", f"Total {c} PP (Linha)")
            for c in _CLASSES if not sub[sub["classe"] == c].empty}


def g34_nc_cat_tipo_pv(df: pd.DataFrame) -> dict[str, go.Figure]:
    """Retorna dict {tipo: figura} para PV."""
    sub = _prep_nc(_prep_tipo(df[df["ambiente"] == "Plenário Virtual"]))
    return {t: _barras_grupo(sub[sub["tipo_questao"] == t],
                              "ano", "categoria_nc", CORES_NC,
                              f"Não Concluídos por Categoria — {t} — PV",
                              "Inclusões em pauta", f"Total {t} PV (Linha)")
            for t in _TIPOS if not sub[sub["tipo_questao"] == t].empty}


def g35_nc_cat_tipo_pp(df: pd.DataFrame) -> dict[str, go.Figure]:
    """Retorna dict {tipo: figura} para PP."""
    sub = _prep_nc(_prep_tipo(df[df["ambiente"] == "Plenário Físico"]))
    return {t: _barras_grupo(sub[sub["tipo_questao"] == t],
                              "ano", "categoria_nc", CORES_NC,
                              f"Não Concluídos por Categoria — {t} — PP",
                              "Inclusões em pauta", f"Total {t} PP (Linha)")
            for t in _TIPOS if not sub[sub["tipo_questao"] == t].empty}


# ═══════════════════════════════════════════════════════════════════════════════
# GRUPO 5 — Sustentação oral  (gráficos 36–39)
# ═══════════════════════════════════════════════════════════════════════════════

def _pizza_bool(df: pd.DataFrame, col: str, label_true: str,
                label_false: str, cores: dict, titulo: str) -> go.Figure:
    """Pizza para proporção de uma coluna booleana."""
    serie = df[col].map({True: label_true, False: label_false}).value_counts()
    return _pizza(serie, titulo,
                  cores=[cores.get(l, "#999") for l in serie.index])


def g36_sust_periodo_pv(df: pd.DataFrame) -> go.Figure:
    sub = df[df["ambiente"] == "Plenário Virtual"]
    return _pizza_bool(sub, "teve_sustentacao",
                       "Com sustentação oral", "Sem sustentação oral",
                       CORES_SUST,
                       "Inclusões com sustentação oral — Plenário Virtual (2020–2025)")


def g37_sust_periodo_pp(df: pd.DataFrame) -> go.Figure:
    sub = df[df["ambiente"] == "Plenário Físico"]
    return _pizza_bool(sub, "teve_sustentacao",
                       "Com sustentação oral", "Sem sustentação oral",
                       CORES_SUST,
                       "Inclusões com sustentação oral — Plenário Físico (2020–2025)")


def g38_sust_anual_pv(df: pd.DataFrame) -> go.Figure:
    sub = df[(df["ambiente"] == "Plenário Virtual") & df["teve_sustentacao"]]
    tab = (sub.groupby("ano").size().reset_index(name="n")
           .set_index("ano").reindex(range(2020, 2026), fill_value=0).reset_index())
    fig = _bar_fig()
    fig.add_trace(go.Bar(
        x=tab["ano"], y=tab["n"], name="Com sustentação oral",
        marker_color=CORES_SUST["Com sustentação oral"],
        text=tab["n"], textposition="outside", cliponaxis=False,
    ))
    fig.update_layout(title_text="Inclusões com sustentação oral por ano — Plenário Virtual",
                      yaxis_title="Inclusões com sustentação")
    return fig


def g39_sust_anual_pp(df: pd.DataFrame) -> go.Figure:
    sub = df[(df["ambiente"] == "Plenário Físico") & df["teve_sustentacao"]]
    tab = (sub.groupby("ano").size().reset_index(name="n")
           .set_index("ano").reindex(range(2020, 2026), fill_value=0).reset_index())
    fig = _bar_fig()
    fig.add_trace(go.Bar(
        x=tab["ano"], y=tab["n"], name="Com sustentação oral",
        marker_color=CORES_SUST["Com sustentação oral"],
        text=tab["n"], textposition="outside", cliponaxis=False,
    ))
    fig.update_layout(title_text="Inclusões com sustentação oral por ano — Plenário Físico",
                      yaxis_title="Inclusões com sustentação")
    return fig
