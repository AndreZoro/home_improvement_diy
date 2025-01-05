import streamlit as st
import pyvista as pv

from pyvista import themes
pv.set_plot_theme(themes.DarkTheme())

from stpyvista import stpyvista
from stpyvista.utils import start_xvfb


import tempfile

import requests


# st.set_page_config(
#     page_title="MEGA Shaper - Home Improvement DIY Edition",
#     page_icon=":nut_and_bolt:",
#     layout="wide",
#     initial_sidebar_state="collapsed",
#     menu_items=None,
# )


st.title(
    "Design a corner braket to your own specifications."
)

if "IS_XVFB_RUNNING" not in st.session_state:
    start_xvfb()
    st.session_state.IS_XVFB_RUNNING = True


plotter = pv.Plotter(border=False)
plotter.background_color = "#f0f8ff"
reader = pv.STLReader("static/stl_files/corner-bracket_3sided.stl")
## Read data and send to plotter
mesh = reader.read()
plotter.add_mesh(mesh, color="orange", specular=0.5)
plotter.view_xz()


left_controls, three_d_window = st.columns([2,1])

with left_controls:
    lc_r1_c1, lc_r1_c2, lc_r1_c3 = st.columns(3)
    lc_r2_c1, lc_r2_c2, lc_r2_c3 = st.columns(3)

    with lc_r1_c1:
        st.slider("CB Dummy Var 01", min_value=0, max_value=100, value = 20)

    with lc_r1_c2:
        st.slider("CB Dummy Var 02", min_value=0, max_value=100, value = 10)

    with lc_r1_c3:
        st.slider("CB Dummy Var 03", min_value=0, max_value=100, value = 30)

    with lc_r2_c1:
        st.slider("CB Dummy Var 04", min_value=0, max_value=100, value = 50)

    with lc_r2_c2:
        st.slider("CB Dummy Var 05", min_value=0, max_value=100, value = 70)

    with lc_r2_c3:
        st.slider("CB Dummy Var 06", min_value=0, max_value=100, value = 30)


with three_d_window:
    stpyvista(plotter)
