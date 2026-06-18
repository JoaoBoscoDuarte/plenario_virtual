Aqui está o conteúdo completo e detalhado estruturado para um arquivo **`README.md`** ou um guia de documentação interna do seu projeto. Você pode simplesmente copiar o bloco de código abaixo e salvar como um arquivo `.md` na raiz do seu projeto.

---

````markdown
# 📊 Documentação: Arquitetura de Dados (Hugging Face + Parquet) e Painel do Acervo (Streamlit)

Este documento detalha a implementação da pipeline de dados e da interface gráfica do módulo **Acervo Histórico**. A arquitetura foi desenhada para produção, separando o código-fonte (hospedado no GitHub) dos arquivos de dados (hospedados no Hugging Face Datasets em formato `.parquet` de alta performance).

---

## 🏛️ 1. Desenho da Arquitetura de Dados

Para contornar as limitações de armazenamento do GitHub e mitigar gargalos de memória RAM no deploy gratuito do Streamlit Cloud, adotamos a seguinte divisão:

- **GitHub:** Armazena estritamente códigos Python (`.py`), configurações (`.txt`, `.toml`) e documentação.
- **Hugging Face Datasets:** Funciona como nosso Data Lake na nuvem, armazenando arquivos brutos e processados.
- **Formato Parquet:** Substitui o formato CSV por ser colunar, altamente compactado e otimizado para leitura veloz via Pandas.

### Estrutura de Pastas do Data Lake (Hugging Face)

```text
seu-repositorio-hf/
├── raw/
│   └── processos_stf_brutos.json          # Massa de dados original sem tratamento
├── interim/
│   └── base_limpa_processos.parquet       # Dados limpos e tipados, antes da agregação
└── processed/
    └── acervo/
        └── evolucao_acervo.parquet        # Produto final consumido pelo Streamlit (Ano, Classe, Vol)
```
````

---

## 🚀 2. Passo a Passo: Preparação e Importação no Hugging Face

### Passo 2.1: Exportando os dados locais para Parquet

No seu ambiente de processamento (Notebook/Colab), exporte o DataFrame final agregado utilizando o motor padrão do pandas:

```python
# Exportando para o formato binário Parquet (sem incluir o índice numérico)
df_evolucao_acervo.to_parquet("evolucao_acervo.parquet", index=False)

```

### Passo 2.2: Criando o Token de Acesso no Hugging Face

Para autorizar a persistência de dados via código ou terminal:

1. Acesse **Hugging Face > Settings > Access Tokens**.
2. Clique em **New token** e selecione o tipo **Fine-grained**.
3. Defina um nome (ex: `streamlit-data-sync`).
4. Na seção **Repositories permissions**, selecione o repositório específico do seu dataset e marque a caixinha:

- 🟩 `Write access to contents/settings of selected repos`

5. Clique em **Generate token** e salve o código gerado em local seguro.

### Passo 2.3: Realizando o Upload para o Hugging Face via CLI

Com o token em mãos, instale o utilitário de upload no seu terminal:

```bash
pip install huggingface_hub

```

Rode o comando abaixo para enviar o arquivo diretamente para a pasta correta do seu Data Lake sem precisar gerenciar múltiplos repositórios Git locais:

```bash
huggingface-cli upload SEU_USUARIO/SEU_REPOSITORIO ./evolucao_acervo.parquet /processed/acervo/evolucao_acervo.parquet --repo-type=dataset

```

---

## 💻 3. Implementação do Código no Streamlit

### 📄 3.1: Configuração de Dependências (`requirements.txt`)

O ecossistema Streamlit Cloud precisa saber que deve instalar o motor `pyarrow` para ler arquivos `.parquet`. Garanta que seu arquivo de dependências contenha:

```text
streamlit
pandas
plotly
pyarrow

```

### 📄 3.2: Centralizador de Dados (`app/data/loader.py`)

Este arquivo é o ponto único de contato com a internet. Ele utiliza o decorador `@st.cache_data` para que o download do arquivo Parquet só ocorra **uma única vez** (no primeiro acesso de qualquer usuário), guardando o dataset na memória cache do servidor.

```python
import pandas as pd
import streamlit as st

# URL base apontando para o resolvedor de downloads diretos do Hugging Face
HF_BASE_URL = "[https://huggingface.co/datasets/SEU_USUARIO/SEU_REPOSITORIO/resolve/main/processed](https://huggingface.co/datasets/SEU_USUARIO/SEU_REPOSITORIO/resolve/main/processed)"

@st.cache_data
def load_evolucao_acervo():
    """
    Baixa e lê o dataset de evolução do acervo histórico
    direto da pasta processed do Hugging Face em formato Parquet.
    """
    url = f"{HF_BASE_URL}/acervo/evolucao_acervo.parquet"

    # O pandas infere o formato parquet automaticamente através da extensão e do pyarrow
    df = pd.read_parquet(url)
    return df

```

### 📄 3.3: Interface e Visualizações (`app/pages/acervo.py`)

Este script constrói o layout responsivo em duas colunas, renderiza os gráficos interativos do Plotly com rótulos de valores explícitos nas barras/linhas e expõe o sumário executivo da análise jurimétrica.

```python
import streamlit as st
import plotly.express as px
from data.loader import load_evolucao_acervo

# 1. Configuração da Página para modo Expandido (Wide)
st.set_page_config(
    page_title="Acervo Histórico - STF",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Evolução e Perfil do Acervo")
st.markdown(
    "Análise evolutiva do estoque de processos ativos do Controle Concentrado (ADI, ADC, ADO e ADPF) entre 1988 e 2025."
)

# 2. Carregamento Seguro e Cacheado dos Dados
try:
    df_evolucao_acervo = load_evolucao_acervo()
except Exception as e:
    st.error(f"Erro crítico ao conectar com o Data Lake do Hugging Face: {e}")
    st.stop()

st.markdown("---")

# 3. Construção do Layout em Duas Colunas Paralelas
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Linha do Tempo por Classe")
    st.caption("Valores marcados nos nós. Clique na legenda lateral para isolar uma classe processual.")

    fig1 = px.line(
        df_evolucao_acervo,
        x="ano",
        y="quantidade_ativos",
        color="classe",
        text="quantidade_ativos",
        labels={
            "ano": "Ano de Referência",
            "quantidade_ativos": "Processos Ativos",
            "classe": "Classe",
        },
        markers=True,
    )
    # Garante que as etiquetas numéricas fiquem logo acima do ponto de marcação
    fig1.update_traces(textposition="top center")
    fig1.update_layout(
        template="plotly_white",
        xaxis=dict(dtick=4),
        margin=dict(l=20, r=20, t=20, b=20),
    )

    # Renderiza o gráfico adaptando-se automaticamente à largura da coluna
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📊 Composição Proporcional do Volume")
    st.caption("Visão empilhada demonstrando a volumetria total acumulada ano a ano.")

    fig2 = px.bar(
        df_evolucao_acervo,
        x="ano",
        y="quantidade_ativos",
        color="classe",
        text_auto=True,  # Ativa os valores literais internos ou sobre as fatias de barra
        labels={
            "ano": "Ano",
            "quantidade_ativos": "Volume Total",
            "classe": "Classe",
        },
    )
    fig2.update_layout(
        template="plotly_white",
        xaxis=dict(dtick=4),
        margin=dict(l=20, r=20, t=20, b=20),
    )

    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# 4. Painel de Diagnóstico Analítico e Conclusões Jurimétricas
with st.expander("📝 Ver Diagnóstico Analítico e Conclusões da Série Histórica", expanded=True):
    st.markdown(
        """
        ### 1. Crescimento Ininterrupto do Acervo Total
        O estoque total saltou de apenas **11 processos em 1988** para **9.142 processos ativos em 2025**. O crescimento linear e contínuo sinaliza que a taxa de entrada de novas ações e o tempo de tramitação superam consistentemente a capacidade de baixa definitiva do tribunal.

        ### 2. A Hegemonia Absoluta da ADI
        A Ação Direta de Inconstitucionalidade (ADI) é o principal motor do controle concentrado. Em 2025, com 7.678 processos, as **ADIs sozinhas respondem por aproximadamente 84% de todo o acervo ativo**.

        ### 3. A Ascensão Meteórica da ADPF
        A Arguição de Descumprimento de Preceito Fundamental (ADPF) surge no ano 2000 e apresentou o crescimento proporcional mais agressivo, atingindo **1.279 processos em 2025**. O maior salto ocorreu na última década, impulsionado pelo uso estratégico da classe para contestar atos do poder executivo e omissões governamentais.

        ### 4. O Papel Residual de ADCs e ADOs
        Tanto as Ações Declaratórias de Constitucionalidade (ADC) quanto as Ações Diretas por Omissão (ADO) mantêm volumes estritamente controlados e marginais (95 e 90 processos em 2025, respectivamente), refletindo o caráter mais específico e restrito de suas hipóteses de cabimento.
        """
    )

```

---

## 🛠️ 4. Como Executar o Projeto Localmente

1. Lembre-se de adicionar a pasta local `data/` no seu arquivo `.gitignore` para evitar o envio acidental de arquivos pesados ao GitHub.
2. Ative o seu ambiente virtual (`.venv`).
3. Certifique-se de executar o comando de inicialização **sempre a partir do diretório raiz** do seu repositório:

```bash
streamlit run app/app.py

```

```

```
