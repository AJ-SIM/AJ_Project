# app.py
import streamlit as st
import importlib
import json
import os

# Page layout
st.set_page_config(layout="wide", page_title="HVAC Simulation App")
col1, col2 = st.columns([1, 4])  # 20% / 80% ratio

# Left column: tab selector
with col1:
    st.title("Tabs")
    tabs = [f"Tab {i}" for i in range(1, 6)]
    selected_tab = st.radio("Select a tab:", tabs, index=0)

# Right column: dynamic content based on tab selection
with col2:
    tab_index = selected_tab.split()[1]
    try:
        report_mod = importlib.import_module(f"Tab{tab_index}.report")
        importlib.reload(report_mod)
        calc_mod = importlib.import_module(f"Tab{tab_index}.calculations")
        importlib.reload(calc_mod)
        plot_mod = importlib.import_module(f"Tab{tab_index}.plot")
        importlib.reload(plot_mod)
    except ModuleNotFoundError:
        st.error(f"Modules for {selected_tab} not found.")
    else:
        st.header("Inputs & Description")
        params = report_mod.display_report()
        st.session_state['last_params'] = params

        # Save user input for future reuse
        os.makedirs("user_data", exist_ok=True)
        with open(f"user_data/params_tab{tab_index}.json", "w") as f:
            json.dump(params, f, indent=2)

        results = calc_mod.calculate_outputs(params)

        st.header("Plots")
        if hasattr(plot_mod, 'render_plots'):
            plot_mod.render_plots(results)
        elif hasattr(plot_mod, 'render_plot'):
            plot_mod.render_plot(results)
        elif hasattr(plot_mod, 'show_load_chart'):
            plot_mod.show_load_chart(results)
        else:
            st.info("No plotting function found for this tab.")

