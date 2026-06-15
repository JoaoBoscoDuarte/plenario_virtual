"""
Centralized bootstrap.

Importing this module ensures that the project root is on sys.path,
making both the `app` package and the `src` package importable.

It is imported at the top of the page modules (andamentos.py, etc.)
because Streamlit can load individual pages in contexts where the
path setup from the main app.py hasn't taken effect yet.

The main app.py does its own (equivalent) direct sys.path setup
at the very top before any package-relative imports.
"""

import sys
from pathlib import Path

_root = Path(__file__).resolve().parents[1]

if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))
