import plotly.graph_objects as go

# ==========================================
# PALETA DE CORES (Baseada nas instruções)
# ==========================================
COR_PV = '#2962FF'      # Azul (Plenário Virtual)
COR_PP = '#9CA3AF'      # Cinza (Plenário Presencial - Padrão João)
COR_AMBOS = '#93C5FD'   # Azul claro (Ambos os ambientes)
COR_ESPIN = '#DC2626'   # Vermelho (Linha do fim da ESPIN)

# ==========================================
# Gráfico NA: Participação estável
# ==========================================
def plot_grafico_na():
    anos = ['2020', '2021', '2022', '2023', '2024', '2025']
    valores = [59.8, 68.0, 64.1, 66.8, 59.0, 66.6]
    
    fig = go.Figure(data=[
        go.Bar(x=anos, y=valores, marker_color=COR_PV, text=[f'{v}%' for v in valores], textposition='outside')
    ])
    
    # Marcador vertical do fim da ESPIN (Abril de 2022)
    fig.add_vline(x=2.25, line_width=2, line_dash="dash", line_color=COR_ESPIN,
                  annotation_text="fim da ESPIN<br>(abril de 2022)", 
                  annotation_position="top", annotation_font_color=COR_ESPIN)

    fig.update_layout(
        title="<b>A participação do Plenário Virtual mantém-se entre 59% e 68% ao ano</b><br><sup>Percentual das inclusões em pauta destinadas ao ambiente virtual, 2020-2025</sup>",
        yaxis=dict(visible=False, range=[0, 85]), # Espaço para o texto fora da barra
        plot_bgcolor='white',
        margin=dict(t=100)
    )
    fig.show()

# ==========================================
# Gráfico NB: Pauta versus concluídos
# ==========================================
def plot_grafico_nb():
    categorias = ['Participação<br>na pauta', 'Participação nos<br>julgamentos concluídos']
    valores = [63.9, 91.3]
    
    fig = go.Figure(data=[
        go.Bar(x=categorias, y=valores, marker_color=COR_PV, text=[f'{v}%' for v in valores], textposition='outside')
    ])
    
    fig.update_layout(
        title="<b>O Plenário Virtual concentra os julgamentos concluídos</b><br><sup>Participação do ambiente virtual na pauta e nos 3.187 julgamentos concluídos, 2020-2025</sup>",
        yaxis=dict(visible=False, range=[0, 110]),
        plot_bgcolor='white',
        margin=dict(t=100)
    )
    fig.show()

# ==========================================
# Gráfico NC: Tramitação por ambiente
# ==========================================
def plot_grafico_nc():
    categorias = ['Somente<br>Plenário Presencial', 'Ambos os<br>ambientes', 'Somente<br>Plenário Virtual']
    valores = [5.6, 16.9, 77.5]
    processos = [159, 478, 2197]
    cores = [COR_PP, COR_AMBOS, COR_PV]
    textos = [f'<b>{v}%</b>  ({p} processos)' for v, p in zip(valores, processos)]
    
    fig = go.Figure(data=[
        go.Bar(y=categorias, x=valores, orientation='h', marker_color=cores, text=textos, textposition='outside')
    ])
    
    fig.update_layout(
        title="<b>Três de cada quatro processos nunca passam pelo Plenário Presencial</b><br><sup>Tramitação em pauta dos 2.834 processos de controle concentrado, 2020-2025</sup>",
        xaxis=dict(visible=False, range=[0, 110]),
        plot_bgcolor='white',
        margin=dict(t=100)
    )
    fig.show()

# ==========================================
# Gráfico ND: Recursos
# ==========================================
def plot_grafico_nd():
    fig = go.Figure()

    # Barra do Plenário Virtual
    fig.add_trace(go.Bar(
        y=['Recursos'], x=[94.3], name='Plenário Virtual', orientation='h', marker_color=COR_PV,
        text="<b>Plenário Virtual<br>94,3% (1.048 recursos)</b>", textposition='inside', insidetextanchor='middle'
    ))
    
    # Barra do Plenário Presencial
    fig.add_trace(go.Bar(
        y=['Recursos'], x=[5.7], name='Plenário Presencial', orientation='h', marker_color=COR_PP,
        text="PP: 5,7%<br>(63)", textposition='outside'
    ))

    fig.update_layout(
        title="<b>A atividade recursal migrou quase integralmente para o ambiente virtual</b><br><sup>Destino das 1.111 inclusões em pauta de recursos (AgR, ED e afins), 2020-2025</sup>",
        barmode='stack',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
        plot_bgcolor='white',
        margin=dict(t=100)
    )
    fig.show()

# ==========================================
# Gráfico NE: Inclusões por processo
# ==========================================
def plot_grafico_ne():
    categorias = ['Plenário Virtual', 'Plenário Presencial']
    valores = [1.8, 4.3]
    cores = [COR_PV, COR_PP]
    
    fig = go.Figure(data=[
        go.Bar(x=categorias, y=valores, marker_color=cores, text=[str(v).replace('.', ',') for v in valores], textposition='outside')
    ])
    
    fig.update_layout(
        title="<b>Cada julgamento presencial consome mais que o dobro de inclusões em pauta</b><br><sup>Média de inclusões em pauta por processo em cada ambiente, 2020-2025</sup>",
        yaxis=dict(visible=False, range=[0, 5.5]),
        plot_bgcolor='white',
        margin=dict(t=100)
    )
    fig.show()

# ==========================================
# Gráfico NF: Conclusão por processo
# ==========================================
def plot_grafico_nf():
    categorias = ['Plenário Virtual', 'Plenário Presencial']
    valores = [86.0, 39.2]
    cores = [COR_PV, COR_PP]
    
    fig = go.Figure(data=[
        go.Bar(x=categorias, y=valores, marker_color=cores, text=[f'{str(v).replace(".", ",")}%' for v in valores], textposition='outside')
    ])
    
    fig.update_layout(
        title="<b>Considerado o processo, o ambiente virtual conclui 86% do que pauta</b><br><sup>Percentual de processos pautados que tiveram julgamento concluído, 2020-2025</sup>",
        yaxis=dict(visible=False, range=[0, 105]),
        plot_bgcolor='white',
        margin=dict(t=100)
    )
    fig.show()

# Descomente as linhas abaixo para gerar os gráficos individualmente
# plot_grafico_na()
# plot_grafico_nb()
# plot_grafico_nc()
# plot_grafico_nd()
# plot_grafico_ne()
# plot_grafico_nf()
