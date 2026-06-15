# stf-plenario-virtual

Estrutura de projeto para análise de dados do Plenário Virtual do STF.

## Estrutura de diretórios

```
stf-plenario-virtual/
├── data/
│   ├── raw/          # Dados originais e imutáveis da raspagem — nunca editar
│   ├── processed/    # Dados limpos, padronizados e prontos para análise
│   └── interim/      # Dados em etapas intermediárias de limpeza
├── notebooks/
│   ├── helena/       # Notebooks de análise da Helena (doutorado)
│   ├── mestranda_1/  # Notebooks da primeira mestranda
│   └── mestranda_2/  # Notebooks da segunda mestranda
├── src/
│   ├── cleaning.py   # Funções de limpeza e padronização
│   ├── filters.py    # Funções de recorte e filtragem
│   └── viz.py        # Funções de visualização reutilizáveis
├── app/              # Código do dashboard Streamlit
├── docs/             # Documentação técnica e acadêmica
├── requirements.txt
├── README.md
└── LICENSE
```

## Uso

- Coloque dados crus (imutáveis) em `data/raw/`.
- Use `src/cleaning.py`, `src/filters.py` e `src/viz.py` para código reutilizável.
- Notebooks pessoais vão em `notebooks/<pessoa>/`.
- Dashboard Streamlit em `app/`.
- Documentação em `docs/`.

## Instalação

```bash
pip install -r requirements.txt
```
