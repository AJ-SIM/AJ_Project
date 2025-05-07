# tab1/__init__.py
import streamlit as st
from .report import display_report
from .downloads import display_download_buttons

def render_tab1():
    st.header("Tab 1: Input Parameters & Cooling Load Calculations")
    display_download_buttons()
    display_report()