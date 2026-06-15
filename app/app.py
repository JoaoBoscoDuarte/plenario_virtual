"""
Entry point principal do dashboard Streamlit — STF Plenário Virtual.

Recomendado após `pip install -e .`:

    PYTHONPATH=. streamlit run app/app.py

Ou:

    python -m streamlit run app/app.py

Estrutura multipage (páginas em app/pages/). Filtros globais na sidebar
são lidos pelas páginas via st.session_state ou re-leitura simples.

Segue fielmente a arquitetura do DEPLOY_GUIDE.md + orientações da especificacao v2.
"""

import sys
from pathlib import Path

import streamlit as st

# Bootstrap: put project root on sys.path BEFORE any import that mentions 'app' or 'src'.
# This is mandatory for `streamlit run app/app.py` because Streamlit runs the file
# as a script and the package context for 'app' is not set up.
root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

# Now safe to use absolute imports from the top level 'app' and 'src' packages.
from app.data_loader import load_all

st.set_page_config(
    page_title="STF — Plenário Virtual",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("⚖️ Painel de Análise — Plenário Virtual do STF")
st.markdown(
    """
    Análise empírica dos julgamentos do Plenário Virtual do Supremo Tribunal Federal.  
    Dados de ADI, ADC, ADO e ADPF processados a partir do portal oficial do STF.
    """
)

# Carregamento inicial (cached internamente)
with st.spinner("Carregando datasets processados..."):
    data = load_all()

# Filtros globais (simples no MVP; as páginas podem aplicar localmente ou ler daqui)
with st.sidebar:
    st.header("Filtros Globais")
    st.caption("Aplicam-se aproximadamente às visualizações (páginas podem refinar).")

    # Date range based on processos (data_protocolo) + fallback para and_data se necessário
    proc = data["processos"]
    if "data_protocolo" in proc.columns and proc["data_protocolo"].notna().any():
        min_date = proc["data_protocolo"].min().date()
        max_date = proc["data_protocolo"].max().date()
    else:
        min_date = None
        max_date = None

    date_range = st.date_input(
        "Período (data protocolo)",
        value=(min_date, max_date) if min_date and max_date else None,
        min_value=min_date,
        max_value=max_date,
    )

    classes = sorted(proc["classe"].dropna().unique().tolist()) if "classe" in proc.columns else []
    selected_classes = st.multiselect("Classe processual", classes, default=classes)

    tipos = sorted(proc["tipo_processo"].dropna().unique().tolist()) if "tipo_processo" in proc.columns else []
    selected_tipos = st.multiselect("Tipo de processo", tipos, default=tipos)

    st.divider()
    st.info("Navegue pelas páginas no menu lateral.\n\nOs dados são carregados de parquets locais (dev) ou Hugging Face (produção).")

# Expor filtros escolhidos para as páginas (páginas podem ler st.session_state ou re-implementar)
st.session_state["global_filters"] = {
    "date_range": date_range,
    "classes": selected_classes,
    "tipos": selected_tipos,
}

st.markdown("---")
st.caption(
    "Repositório: https://github.com/boscodeb/plenario_virtual  •  "
    "Para regenerar os dados: `python -m src.cleaning`  •  "
    "Deploy automático via Streamlit Community Cloud em pushes para main."
)
