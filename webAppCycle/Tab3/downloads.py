import streamlit as st
import pandas as pd

def show_download_buttons():
    # Create dummy data to download
    df = pd.DataFrame({"A": [1, 2, 3]})
    st.download_button(
        label="Download sample CSV",
        data=df.to_csv(index=False).encode(),
        file_name="sample.csv",
        mime="text/csv",
    )
