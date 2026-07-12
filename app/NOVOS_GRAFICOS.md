Quanto o data frame:
Salva o df_final com a coluna teve_reajuste — pronto para os gráficos e para cruzar com outras análises.
Salva os andamentos de reajuste com uma coluna extra familia_mudanca (Reajuste / Alteração / Reformulação), permitindo você ver a distribuição dos tipos de mudança de voto e auditar os textos originais.


```
CORES_CLASSE = {
    'ADI':  '#2563eb',
    'ADPF': '#f59e0b',
    'ADC':  '#16a34a',
    'ADO':  '#ef4444',
}
CORES_REAJUSTE = {
    'Com reajuste de voto': '#dc2626',   # vermelho
    'Sem reajuste de voto': '#e5e7eb',   # cinza claro
}


def plotar_pizza_reajuste(serie, titulo, cores=None):
    """Pizza simples para proporção com/sem reajuste."""
    cores_lista = [cores.get(k, '#999999') for k in serie.index] if cores else None
    fig = go.Figure(data=[go.Pie(
        labels=serie.index,
        values=serie.values,
        hole=0.4,
        marker=dict(colors=cores_lista),
        textinfo='label+value+percent',
        textfont=dict(size=13),
    )])
    fig.update_layout(
        title=dict(text=titulo, x=0.5, xanchor='center', font=dict(size=14)),
        showlegend=False,
        margin=dict(t=60, b=40, l=40, r=40),
        height=420,
    )
    fig.show()
    return fig


def plotar_barras_reajuste(df_dados, col_x, col_grupo=None, titulo='',
                            label_y='Inclusões com reajuste', cores=None):
    """Barras (agrupadas ou simples) para contagens de reajuste."""
    fig = go.Figure()

    if col_grupo:
        grupos = sorted(df_dados[col_grupo].unique())
        for g in grupos:
            sub = df_dados[df_dados[col_grupo] == g]
            fig.add_trace(go.Bar(
                x=sub[col_x], y=sub['n'], name=str(g),
                marker_color=(cores.get(g) if cores else None),
                text=sub['n'], textposition='outside',
            ))
        fig.update_layout(barmode='group')
    else:
        fig.add_trace(go.Bar(
            x=df_dados[col_x], y=df_dados['n'],
            text=df_dados['n'], textposition='outside',
            marker_color='#dc2626',
        ))

    fig.update_layout(
        title=dict(text=titulo, x=0.5, xanchor='center', font=dict(size=14)),
        xaxis=dict(title='', dtick=1),
        yaxis=dict(title=label_y),
        margin=dict(t=60, b=40, l=50, r=30),
        height=440,
        legend=dict(orientation='h', yanchor='top', y=-0.12, xanchor='center', x=0.5),
    )
    fig.show()
    return fig
```

```
# ===========================================================================
# GRÁFICOS DE REAJUSTE DE VOTO — os 6 solicitados
# ===========================================================================
# Pré-requisitos já executados:
#   - df_final com a coluna 'teve_reajuste' (Célula 4)
#   - funções plotar_pizza_reajuste e plotar_barras_reajuste (Célula 5)
#   - CORES_CLASSE e CORES_REAJUSTE definidos

# ---------------------------------------------------------------------------
# GRÁFICO 1 e 2 — GERAL — PERÍODO — PV e PP (pizza com/sem reajuste)
# ---------------------------------------------------------------------------
for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    sub = df_final[df_final['ambiente'] == ambiente]
    serie = sub['teve_reajuste'].map({
        True:  'Com reajuste de voto',
        False: 'Sem reajuste de voto'
    }).value_counts()

    print(f"{ambiente}: {sub['teve_reajuste'].sum():,} com reajuste "
          f"de {len(sub):,} inclusões ({100*sub['teve_reajuste'].mean():.1f}%)")

    _ = plotar_pizza_reajuste(
        serie,
        titulo=f'Inclusões com reajuste de voto — {ambiente} (2020–2025)',
        cores=CORES_REAJUSTE,
    )

# ---------------------------------------------------------------------------
# GRÁFICO 3 e 4 — GERAL — ANUAL — PV e PP (barras por ano)
# ---------------------------------------------------------------------------
for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    sub = df_final[(df_final['ambiente'] == ambiente) & (df_final['teve_reajuste'])]
    tab = sub.groupby('ano').size().reset_index(name='n')

    # Garante todos os anos 2020-2025, mesmo com zero
    tab = tab.set_index('ano').reindex(range(2020, 2026), fill_value=0).reset_index()

    _ = plotar_barras_reajuste(
        tab, col_x='ano',
        titulo=f'Inclusões com reajuste de voto por ano — {ambiente} (2020–2025)',
    )

# ---------------------------------------------------------------------------
# GRÁFICO 5 e 6 — ANUAL — POR CLASSE — PV e PP (barras agrupadas por classe)
# ---------------------------------------------------------------------------
for ambiente in ['Plenário Virtual', 'Plenário Físico']:
    sub = df_final[(df_final['ambiente'] == ambiente) & (df_final['teve_reajuste'])]
    tab = sub.groupby(['ano', 'classe']).size().reset_index(name='n')

    _ = plotar_barras_reajuste(
        tab, col_x='ano', col_grupo='classe',
        titulo=f'Reajuste de voto por ano e classe — {ambiente} (2020–2025)',
        cores=CORES_CLASSE,
    )
```
