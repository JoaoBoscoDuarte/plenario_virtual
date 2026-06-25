# Extração do Arcabouço de Plotagem para Dashboard Streamlit

Este documento extrai toda a lógica de visualização do notebook original (`acervo.ipynb`) e a adapta para uso no **Streamlit**, preservando integralmente os gráficos, a função de plotagem, os marcos históricos, as cores e a tabela de proporção.

---

## 1. Estrutura de Dados

O notebook gera e salva um dataset `evolucao_acervo.parquet` com as seguintes colunas:

- `ano` (int)
- `classe` (str): ADI, ADC, ADO, ADPF, CC
- `total_geral`
- `quantidade_ativos`
- `quantidade_inativos`
- `quantidade_baixas`
- `quantidade_distribuidos`

No Streamlit, carregamos esse arquivo uma única vez:

```python
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    return pd.read_parquet("caminho/para/evolucao_acervo.parquet")

df = load_data()
```

---

## 2. Função de Plotagem (adaptada para Streamlit)

A função `plotar_grafico_stf` foi extraída e adaptada para:

- Usar `st.plotly_chart(fig)` em vez de `fig.show()`
- Remover a configuração do renderizador do Colab
- Manter todos os elementos visuais (linhas de ER, ESPIN, legendas, eixos duplos)

```python
import plotly.graph_objects as go
import streamlit as st

# Cores padronizadas
CORES_CLASSE = {
    "ADI": "#3498db",
    "ADC": "#1abc9c",
    "ADO": "#9b59b6",
    "ADPF": "#e67e22",
}

def plotar_grafico_stf(df_dados, classe_nome, coluna_metrica, label_metrica, titulo_sufixo):
    """
    Gera gráfico com barras (classe ou total) e linha do total geral (se classe específica).
    """
    # Total geral anual para a métrica
    df_total_geral = df_dados.groupby("ano")[coluna_metrica].sum().reset_index()

    fig = go.Figure()

    if classe_nome.upper() == "TOTAL":
        fig.set_subplots(specs=[[{"secondary_y": False}]])
        max_y = df_total_geral[coluna_metrica].max()
        fig.add_trace(
            go.Bar(
                x=df_total_geral["ano"],
                y=df_total_geral[coluna_metrica],
                marker_color="#3498db",
                text=df_total_geral[coluna_metrica],
                textposition="outside",
                cliponaxis=False,
                name=f"Total Geral ({label_metrica})"
            )
        )
    else:
        fig.set_subplots(specs=[[{"secondary_y": True}]])
        df_filtrado = df_dados[df_dados["classe"] == classe_nome]
        max_y = df_filtrado[coluna_metrica].max()

        # Linha do total geral (eixo secundário)
        fig.add_trace(
            go.Scatter(
                x=df_total_geral["ano"],
                y=df_total_geral[coluna_metrica],
                mode="lines+markers",
                line=dict(color="#7f7f7f", width=2),
                marker=dict(size=4),
                name=f"Total Geral ({label_metrica})"
            ),
            secondary_y=True
        )

        # Barras da classe (eixo primário)
        fig.add_trace(
            go.Bar(
                x=df_filtrado["ano"],
                y=df_filtrado[coluna_metrica],
                marker_color=CORES_CLASSE.get(classe_nome, "#3498db"),
                text=df_filtrado[coluna_metrica],
                textposition="outside",
                cliponaxis=False,
                name=f"Classe: {classe_nome}"
            ),
            secondary_y=False
        )

    if max_y == 0 or pd.isna(max_y):
        max_y = 1

    # --- Marcos históricos (ERs e ESPIN) ---
    fig.add_vrect(x0=2020, x1=2022, fillcolor="green", opacity=0.08, layer="below", line_width=0)
    fig.add_annotation(
        x=2021, y=max_y * 0.95,
        text="<b>ESPIN</b>", showarrow=False,
        xanchor="center", yanchor="top",
        font=dict(color="green", size=9)
    )

    fig.add_shape(type="line", x0=2016, x1=2016, y0=0, y1=max_y * 1.15,
                  line=dict(color="purple", width=1.2, dash="dash"))
    fig.add_annotation(x=2016, y=max_y * 1.15, text="ER 51", showarrow=False,
                       xanchor="center", yanchor="bottom", font=dict(color="purple", size=9))

    fig.add_shape(type="line", x0=2019, x1=2019, y0=0, y1=max_y * 1.08,
                  line=dict(color="#d9822b", width=1.2, dash="dash"))
    fig.add_annotation(x=2019, y=max_y * 1.08, text="ER 52", showarrow=False,
                       xanchor="center", yanchor="bottom", font=dict(color="#d9822b", size=9))

    fig.add_shape(type="line", x0=2020, x1=2020, y0=0, y1=max_y * 1.00,
                  line=dict(color="red", width=1.2, dash="dash"))
    fig.add_annotation(x=2020, y=max_y * 1.00, text="ER 53", showarrow=False,
                       xanchor="center", yanchor="bottom", font=dict(color="red", size=9))

    # Itens fictícios para legenda
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines",
                  line=dict(color="purple", width=1.5, dash="dash"), name="ER 51/2016"))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines",
                  line=dict(color="#d9822b", width=1.5, dash="dash"), name="ER 52/2019"))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines",
                  line=dict(color="red", width=1.5, dash="dash"), name="ER 53/2020"))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
                  marker=dict(color="green", symbol="square", size=12, opacity=0.2), name="Período da ESPIN"))

    # Layout
    titulo_peca = "Total Geral" if classe_nome.upper() == "TOTAL" else f"Classe {classe_nome}"
    fig.update_layout(
        title_text=f"Evolução Anual ({titulo_sufixo}) — {titulo_peca}",
        template="plotly_white",
        margin=dict(t=120, b=160),
        legend=dict(
            orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5,
            font=dict(size=10, color="#333333"),
            bgcolor="#fcfcfc", bordercolor="#cccccc", borderwidth=1
        )
    )

    fig.update_xaxes(dtick=1, title_text="Ano de Referência", range=[1987.5, 2025.5])

    if classe_nome.upper() == "TOTAL":
        fig.update_yaxes(title_text=f"Quantidade Total de {label_metrica}")
    else:
        fig.update_yaxes(title_text=f"{label_metrica} da Classe (Barras)", secondary_y=False)
        fig.update_yaxes(title_text=f"Total Geral do Tribunal (Linha)", secondary_y=True)

    return fig
```

---

## 3. Geração de Todos os Gráficos no Streamlit

No Streamlit, você pode organizar os gráficos em abas (`st.tabs`) ou colunas. Exemplo:

```python
import streamlit as st

st.set_page_config(layout="wide")
st.title("Evolução do Acervo do STF")

# Carregar dados
df = load_data()

classes = ["ADI", "ADC", "ADO", "ADPF"]

# Abas para organizar as visualizações
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Acervo Ativo", "Baixas", "Distribuições", "Tabela de Proporção", "Comparativos"]
)

with tab1:
    st.header("Acervo Ativo")
    # Total
    fig_total = plotar_grafico_stf(df, "TOTAL", "quantidade_ativos", "Processos Ativos", "Acervo Ativo Total")
    st.plotly_chart(fig_total, use_container_width=True)

    # Por classe
    for cls in classes:
        fig_classe = plotar_grafico_stf(df, cls, "quantidade_ativos", "Processos Ativos", "Evolução do Acervo Ativo")
        st.plotly_chart(fig_classe, use_container_width=True)

with tab2:
    st.header("Baixas Anuais")
    fig_total_baixas = plotar_grafico_stf(df, "TOTAL", "quantidade_baixas", "Processos Baixados", "Total Geral de Baixas por Ano")
    st.plotly_chart(fig_total_baixas, use_container_width=True)

    for cls in classes:
        fig_classe_baixas = plotar_grafico_stf(df, cls, "quantidade_baixas", "Processos Baixados", "Fluxo Anual de Baixas")
        st.plotly_chart(fig_classe_baixas, use_container_width=True)

with tab3:
    st.header("Distribuições Anuais")
    fig_total_dist = plotar_grafico_stf(df, "TOTAL", "quantidade_distribuidos", "Processos Distribuídos", "Volume Total de Distribuição Anual")
    st.plotly_chart(fig_total_dist, use_container_width=True)

    for cls in classes:
        fig_classe_dist = plotar_grafico_stf(df, cls, "quantidade_distribuidos", "Processos Distribuídos", "Novos Processos Distribuídos")
        st.plotly_chart(fig_classe_dist, use_container_width=True)

with tab4:
    st.header("Tabela de Proporção do Acervo por Classe")
    # Reconstruir a tabela de proporção
    df_tabela = df.pivot(index='ano', columns='classe', values='quantidade_ativos').fillna(0).astype(int)
    df_tabela['TOTAL_GERAL'] = df_tabela.sum(axis=1)
    for cls in ['ADC', 'ADI', 'ADO', 'ADPF']:
        df_tabela[f'%_{cls}'] = (df_tabela[cls] / df_tabela['TOTAL_GERAL'] * 100).round(2)
    colunas = ['TOTAL_GERAL'] + [c for cls in ['ADC', 'ADI', 'ADO', 'ADPF'] for c in (cls, f'%_{cls}')]
    st.dataframe(df_tabela[colunas], use_container_width=True)

with tab5:
    st.header("Comparativos entre classes")
    # Opcional: gráfico de linhas comparando as classes para uma métrica
    # Exemplo: ativos por classe ao longo do tempo
    fig_comp = go.Figure()
    for cls in classes:
        df_cls = df[df['classe'] == cls]
        fig_comp.add_trace(go.Scatter(
            x=df_cls['ano'], y=df_cls['quantidade_ativos'],
            mode='lines+markers', name=cls, line=dict(color=CORES_CLASSE[cls])
        ))
    fig_comp.update_layout(title="Comparação do Acervo Ativo por Classe",
                           xaxis_title="Ano", yaxis_title="Quantidade de Ativos",
                           template="plotly_white")
    st.plotly_chart(fig_comp, use_container_width=True)
```

---

## 4. Observações Finais

- **Cache**: Use `@st.cache_data` para carregar o parquet apenas uma vez.
- **Caminho do arquivo**: Ajuste o caminho para o local onde `evolucao_acervo.parquet` está armazenado (pode ser no mesmo diretório ou em um bucket S3, etc.).
- **Estilo**: A função de plotagem mantém todos os elementos visuais originais (ERs, ESPIN, eixos duplos). As cores das classes são preservadas.
- **Tabela de proporção**: Reconstruída exatamente como no notebook, com colunas de valores absolutos e percentuais.
- **Responsividade**: `use_container_width=True` faz os gráficos ocuparem toda a largura disponível.

Com essa estrutura, você terá um dashboard completo e fiel ao notebook original, pronto para ser executado no Streamlit.