"""
Support for launching via module form (after `pip install -e .`):

    python -m streamlit run app/app.py

(The command `streamlit run -m app` is **not** supported by Streamlit's CLI.)

The actual bootstrap logic lives in `app/app.py`, and pages use relative imports
for things inside the `app` package.
"""
