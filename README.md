# stf-plenario-virtual

Estrutura de projeto para análise de dados do Plenário Virtual do STF (jurimetria).

**Objetivo principal:** permitir que qualquer pessoa (pesquisadoras, comunidade científica) acesse um dashboard interativo completo **sem precisar abrir ou executar notebooks**. Todo o pipeline de dados é executável de forma autônoma via scripts em `src/`.

## Estrutura de diretórios (alinhada com especificacao v2 + DEPLOY_GUIDE)

```
stf-plenario-virtual/
├── data/
│   ├── raw/          # CSV original imutável — NUNCA editar nem commitar
│   ├── processed/    # 4 parquets gerados (processos + andamentos + decisoes + deslocamentos) — gitignored
│   └── interim/      # Etapas intermediárias (se necessário)
├── notebooks/
│   ├── 01_etl/       # Notebook de auditoria/EDA do pipeline (secundário)
│   ├── helena/       # Notebooks individuais da doutoranda
│   ├── mestranda_1/
│   └── mestranda_2/
├── src/
│   ├── cleaning.py   # Pipeline completo (single source of truth) — rode isto para (re)gerar dados
│   ├── json_transforme.py  # Explosão robusta de JSONs + flags (virtual, unanimidade, tipo órgão etc.)
│   ├── filters.py    # Funções reutilizáveis de filtro
│   ├── viz.py        # Helpers de visualização (Plotly)
│   └── __init__.py
├── app/              # Dashboard Streamlit (multipage)
│   ├── app.py
│   ├── data_loader.py   # Local (dev) + Hugging Face (produção)
│   └── pages/
├── scripts/
│   └── upload_hf.py  # Publica/atualiza os parquets no Hugging Face Hub
├── .streamlit/
│   └── config.toml
├── docs/
├── requirements.txt
├── .gitignore        # Dados nunca entram no Git
├── README.md
└── LICENSE
```

## Como rodar o dashboard (sem abrir nenhum notebook)

1. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. (Recomendado para imports limpos e sem hacks) Instale o pacote em modo editável:
   ```bash
   pip install -e .
   ```

3. Tenha os dados processados (duas opções):
   - **Opção A (recomendada para dev / "só quero ver")**: rode o pipeline uma vez:
     ```bash
     stf-etl
     ```

     (Após `pip install -e .` esse é o comando mais limpo.  
     Alternativa: `python -m src.cleaning` — pode mostrar um warning de `sys.modules` por causa do layout `src/`, mas funciona.)
     Isso lê `data/raw/ArquivosConcatenados_1.csv` e gera/atualiza os 4 arquivos em `data/processed/`.

   - **Opção B (produção)**: os parquets são servidos do Hugging Face Hub (veja DEPLOY_GUIDE). O `app/data_loader.py` já suporta ambos os modos.

4. Inicie o Streamlit (após `pip install -e .`):

   **Forma mais confiável:**
   ```bash
   PYTHONPATH=. streamlit run app/app.py
   ```

   Ou:
   ```bash
   python -m streamlit run app/app.py
   ```

   O `app/_bootstrap.py` + early `sys.path` insert no `app/app.py` + `import app._bootstrap` nas páginas garantem que tanto `app.*` quanto `src.*` sejam encontrados mesmo quando o Streamlit runner executa os arquivos diretamente.

   Evitamos relative imports no script principal (app/app.py) porque ele é executado como __main__ pelo Streamlit (causa "attempted relative import with no known parent package"). Usamos imports absolutos depois do bootstrap.

Filtros globais na sidebar + páginas específicas (andamentos, decisões, deslocamentos). Tudo funciona localmente com zero dependência de Jupyter.

## Regenerar os dados (após nova raspagem do STF)

```bash
python -m src.cleaning
# (ou com caminhos customizados)
python -m src.cleaning --raw /caminho/para/novo.csv --out data/processed
```

Em seguida publique/atualize no Hugging Face (se for o caso de deploy):
```bash
export HF_TOKEN="hf_..."
python scripts/upload_hf.py
```

## Deploy (Streamlit Community Cloud)

- Siga o [DEPLOY_GUIDE.md](./DEPLOY_GUIDE.md) passo a passo.
- Main file: `app/app.py`
- Configure o segredo do Hugging Face (se dataset privado).
- Push na `main` → deploy automático.

## Notas importantes de organização

- `src/cleaning.py` + `src/json_transforme.py` são o coração do pipeline. O notebook `01_etl/` foi mantido para auditoria e EDA, mas **não é necessário** para usar o dashboard ou reproduzir os dados.
- Dados grandes ficam de fora do Git (`.gitignore` completo + Hugging Face Hub).
- Reuso: `src/filters.py` e `src/viz.py` são consumidos tanto pelo app quanto por notebooks de pesquisa.

## Instalação (detalhe)

```bash
pip install -r requirements.txt
```

Principais dependências para o dashboard: streamlit, pandas, pyarrow, plotly, datasets, huggingface-hub.

## Licença

MIT (código). Ver LICENSE.

---

*Projeto alinhado com os princípios de Ciência Aberta e reprodutibilidade descritos na especificacao_projeto_plenario_virtual_v2.md.*

