"""app package for the Streamlit dashboard.

This file makes 'app' a proper package, which helps with imports
when running `streamlit run app/app.py` (especially for multipage apps
and when doing `from app.data_loader import ...` or similar).

The actual path setup for reliable "app.*" and "src" imports is done
at runtime in app.py and the individual pages (see sys.path hacks).
"""
