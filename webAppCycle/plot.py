
# plot.py (updated)
import streamlit as st
import pandas as pd

def render_plot(load_dict: dict):
    df = pd.DataFrame(load_dict, index=["Load (W)"]).T
    st.bar_chart(df)


