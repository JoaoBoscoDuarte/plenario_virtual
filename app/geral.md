Erro na parte geral:

```py
ImportError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/mount/src/plenario_virtual/app/app.py", line 28, in <module>
    pg.run()
    ~~~~~~^^
File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/navigation/page.py", line 490, in run
    exec(code, module.__dict__)  # noqa: S102
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^
File "/mount/src/plenario_virtual/app/pages/geral/geral.py", line 12, in <module>
    from components.filters import multiselect_filter, year_range_filter
```

Visualização linha do tempo:

```
# Configurações de cores
cores_fases = {
    1: "#7f8c8d", 2: "#3498db", 3: "#9b59b6", 4: "#e67e22",
}

dados_timeline = [
    {"fase": 1, "data": "2007", "norma": "ER 21/2007", "desc": "Criação do formato eletrônico assíncrono para votação sobre repercussão geral em RE; prazo comum de 20 dias corridos."},
    {"fase": 1, "data": "2010", "norma": "ER 41/2010", "desc": "Redistribuição dos autos quando o relator é vencido."},
    {"fase": 1, "data": "2010", "norma": "ER 42/2010", "desc": "1ª ampliação: julgamento de mérito de RE com repercussão geral reconhecida (reafirmação de jurisprudência)."},
    {"fase": 2, "data": "2016", "norma": "ER 51/2016", "desc": "2ª ampliação: julgamento de agravos internos e EDs; possibilidade de julgamentos virtuais pelas Turmas; aproximação do controle concentrado."},
    {"fase": 2, "data": "2016", "norma": "Res. 587/2016", "desc": "Criação do 'destaque'; sessões semanais (7 dias corridos para votos)."},
    {"fase": 2, "data": "2018", "norma": "Res. 611/2018", "desc": "Prorrogação automática de prazo para 1º dia útil; abstenção computada como adesão ao relator."},
    {"fase": 3, "data": "2019", "norma": "ER 52/2019", "desc": "3ª ampliação: cautelares em controle concentrado, referendos; todas as classes em temas com jurisprudência dominante."},
    {"fase": 3, "data": "2019", "norma": "Res. 642/2019", "desc": "Prazo de votos reduzido p/ 5 dias úteis; destaque/sustentação oral deslocam ao presencial."},
    {"fase": 4, "data": "3/2/2020", "norma": "Portaria MS 188", "desc": "Declaração da ESPIN (início oficial da pandemia de Covid-19)."},
    {"fase": 4, "data": "18/3/2020", "norma": "ER 53/2020", "desc": "Expansão irrestrita: todas as classes processuais (inclui mérito concentrado); sustentação oral virtual; sessões extraordinárias."},
    {"fase": 4, "data": "2020", "norma": "Res. 669/2020", "desc": "Pedidos de vista formulados no presencial podem ser devolvidos ao PV."},
    {"fase": 4, "data": "2020", "norma": "Res. 672/2020", "desc": "Sessões síncronas por videoconferência autorizadas."},
    {"fase": 4, "data": "2020", "norma": "Res. 675/2020", "desc": "Publicidade em tempo real: votos disponíveis ao público externo durante o julgamento."},
    {"fase": 4, "data": "2020", "norma": "Res. 684/2020", "desc": "Prazo de voto elastecido de 5 para 6 dias úteis (sessão começa e termina sexta-feira)."},
    {"fase": 4, "data": "2020", "norma": "ER 54/2020", "desc": "Abstenção passa a constar como 'não participação'; expressão 'Plenário Virtual' inserida no RISTF."},
    {"fase": 4, "data": "22/4/2022", "norma": "Portaria MS 913", "desc": "Fim oficial da ESPIN (encerramento formal do período pandêmico e início do recorte pós-pandêmico)."},
    {"fase": 4, "data": "2022", "norma": "ER 58/2022", "desc": "Cautelares monocráticas submetidas automaticamente a referendo na pauta virtual subsequente."},
    {"fase": 4, "data": "2024", "norma": "Res. 844/2024", "desc": "Sessões virtuais com horário fixo de início (11h sexta) e encerramento (23h59 sexta seguinte)."},
    {"fase": 4, "data": "2024", "norma": "Portaria 249/2024", "desc": "Instituição de Grupo de Trabalho para atualização das normas do PV."},
    {"fase": 4, "data": "21/8/2025", "norma": "Portal de Sessões", "desc": "Lançamento de ferramenta unificada de consulta a deliberações síncronas e assíncronas."}
]

fig = go.Figure()
total_eventos = len(dados_timeline)
y_max = total_eventos + 1

# Linhas de fase
fig.add_shape(type="line", x0=0, x1=0, y0=17.5, y1=20.5, line=dict(color=cores_fases[1], width=6))
fig.add_shape(type="line", x0=0, x1=0, y0=14.5, y1=17.5, line=dict(color=cores_fases[2], width=6))
fig.add_shape(type="line", x0=0, x1=0, y0=12.5, y1=14.5, line=dict(color=cores_fases[3], width=6))
fig.add_shape(type="line", x0=0, x1=0, y0=0.5,  y1=12.5, line=dict(color=cores_fases[4], width=6))

# Anotações laterais
fig.add_annotation(x=-0.08, y=19.0, text="<b>ETAPA RESTRITA</b>", textangle=-90, font=dict(color=cores_fases[1], size=11), showarrow=False)
fig.add_annotation(x=-0.08, y=16.0, text="<b>ETAPA AMPLIATIVA 1</b>", textangle=-90, font=dict(color=cores_fases[2], size=11), showarrow=False)
fig.add_annotation(x=-0.08, y=13.5, text="<b>ETAPA AMPLIATIVA 2</b>", textangle=-90, font=dict(color=cores_fases[3], size=11), showarrow=False)
fig.add_annotation(x=-0.08, y=6.5,  text="<b>ETAPA AMPLIATIVA 3</b>", textangle=-90, font=dict(color=cores_fases[4], size=11), showarrow=False)

fig.add_hrect(y0=4.5, y1=12.5, fillcolor="green", opacity=0.08, line_width=0, layer="below")

for i, evt in enumerate(dados_timeline):
    y_coord = total_eventos - i
    texto_quebrado = "<br>".join(textwrap.wrap(evt['desc'], width=80))
    texto_final = f"<span style='font-size:12px; font-weight:bold; color:#2c3e50'>{evt['norma']} ({evt['data']})</span><br><span style='font-size:11px; color:#555555'>{texto_quebrado}</span>"

    fig.add_trace(go.Scatter(
        x=[0], y=[y_coord], mode="markers",
        marker=dict(size=12, color="white", line=dict(color=cores_fases[evt['fase']], width=3)),
        hoverinfo="skip"
    ))

    fig.add_annotation(
        x=0.03, y=y_coord, text=texto_final,
        showarrow=False, xanchor="left", yanchor="middle", align="left"
    )

fig.update_layout(
    title_text="<b>Evolução do Plenário Virtual e Controle Concentrado (STF)</b>",
    title_x=0.5, paper_bgcolor="white", plot_bgcolor="white", showlegend=False, height=1400,
)
fig.update_xaxes(range=[-0.15, 1.0], visible=False, fixedrange=True)
fig.update_yaxes(range=[0, y_max], visible=False, fixedrange=True)

# Exibe o gráfico
fig.show(config={'displayModeBar': True})

try:
    print("Gerando arquivos para download...")
    fig.write_image("timeline_stf.png", scale=2, engine="kaleido")
    files.download("timeline_stf.png")
    print("Sucesso! Download iniciado.")
except Exception as e:
    print(f"Erro: {e}")
```
