import streamlit as st
import pandas as pd

def date_filter(df: pd.DataFrame, col: str):
    min_d, max_d = df[col].min(), df[col].max()
    return st.sidebar.date_input("Período", (min_d, max_d))

def multiselect_filter(df: pd.DataFrame, col: str, label: str):
    options = df[col].unique().tolist()
    selected = st.sidebar.multiselect(label, options, default=options)
    return df[df[col].isin(selected)]

