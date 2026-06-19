import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    data = pd.read_csv("app/agg_data_for_app.csv.gz")
    return data
