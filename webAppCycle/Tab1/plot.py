import streamlit as st
import pandas as pd
from . import calculations as calc

def show_load_chart(load_dict: dict):
    """Bar chart of the individual load components."""
    df = pd.DataFrame(load_dict, index=["Load (W)"]).T
    st.bar_chart(df)
