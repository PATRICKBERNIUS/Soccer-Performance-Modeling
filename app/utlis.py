import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    data = pd.read_csv("agg_data_for_clustering.csv")
    return data