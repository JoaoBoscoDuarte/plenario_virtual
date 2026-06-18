"""Bootstrap para imports no Streamlit.

Torna possível usar:
    from data.loader import load_parquet, load_evolucao_acervo

mesmo quando o Streamlit executa app/app.py ou app/pages/*.py diretamente.

Uso:
    import bootstrap   # no topo do arquivo, antes de qualquer import de "data"
"""

import sys
from pathlib import Path

_here = Path(__file__).resolve()

if _here.parent.name == "pages":
    _app_root = _here.parent.parent
else:
    _app_root = _here.parent

if str(_app_root) not in sys.path:
    sys.path.insert(0, str(_app_root))
