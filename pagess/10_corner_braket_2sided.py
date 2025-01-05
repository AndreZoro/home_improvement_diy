import os
from pathlib import Path
import streamlit as st
import pyvista as pv

from pyvista import themes
pv.set_plot_theme(themes.DarkTheme())

from stpyvista import stpyvista
from stpyvista.utils import start_xvfb

import tempfile
import requests

from misc_page_elements.part_selection_bar import build_random_top_bar_part_selection
from misc_page_elements.footer import add_footer
from misc_page_elements.misc_helpers import return_part_config
from misc_page_elements.feedback_helpers import client_feedback_section
from misc_page_elements.download_helpers import download_part


part_config = return_part_config(str(Path(__file__).stem))


if "IS_XVFB_RUNNING" not in st.session_state:
    start_xvfb()
    st.session_state.IS_XVFB_RUNNING = True
# st.set_page_config(
#     page_title="MEGA Shaper - Home Improvement DIY Edition",
#     page_icon=":nut_and_bolt:",
#     layout="wide",
#     initial_sidebar_state="collapsed",
#     menu_items=None,
# )





build_random_top_bar_part_selection()

# st.subheader("Design a corner braket to your own specifications.")
with st.expander("Design a corner braket to your own specifications (expand for help)."):
    st.write('''
        Here we can add help for the current part.
    ''')


plotter = pv.Plotter(border=False)
plotter.background_color = "#f0f8ff"
reader = pv.STLReader("static/stl_files/corner_bracket_2sided_V02.stl")
## Read data and send to plotter
mesh = reader.read()
plotter.add_mesh(mesh, color="orange", specular=0.5)
# plotter.view_xz()
plotter.view_vector([1, 1, 1])


part_images, three_d_window, part_controls = st.columns([1,4,2])

with part_images:
    for image in part_config["hero_images"][:3]:
        st.image(image)

    # st.image("static/images/corner_braket_3sides.png", caption="Corner Braket with 3 sides")
    # st.image("static/images/corner_braket_3sides.png", caption="Corner Braket with 3 sides")
    # st.image("static/images/corner_braket_3sides.png", caption="Corner Braket with 3 sides")
    # st.image("static/images/corner_braket_3sides.png", caption="Corner Braket with 3 sides")
    # st.image("static/images/corner_braket_3sides.png", caption="Corner Braket with 3 sides")

with three_d_window:
    stpyvista(plotter)

with part_controls:
    with st.expander("Basic Settings", expanded=True):
        st.slider("CB Dummy Var 01", min_value=0, max_value=100, value = 20)
        st.slider("CB Dummy Var 02", min_value=0, max_value=100, value = 10)
    with st.expander("Important Settings"):
        st.slider("CB Dummy Var 03", min_value=0, max_value=100, value = 30)
        st.slider("CB Dummy Var 04", min_value=0, max_value=100, value = 50)
    with st.expander("Crazy Settings"):
        st.slider("CB Dummy Var 05", min_value=0, max_value=100, value = 70)
        st.slider("CB Dummy Var 06", min_value=0, max_value=100, value = 30)

    client_feedback_section()
    download_part()


    # lc_r1_c1, lc_r1_c2, lc_r1_c3 = st.columns(3)
    # lc_r2_c1, lc_r2_c2, lc_r2_c3 = st.columns(3)
    #
    # with lc_r1_c1:
    #     st.slider("CB Dummy Var 01", min_value=0, max_value=100, value = 20)
    #
    # with lc_r1_c2:
    #     st.slider("CB Dummy Var 02", min_value=0, max_value=100, value = 10)
    #
    # with lc_r1_c3:
    #     st.slider("CB Dummy Var 03", min_value=0, max_value=100, value = 30)
    #
    # with lc_r2_c1:
    #     st.slider("CB Dummy Var 04", min_value=0, max_value=100, value = 50)
    #
    # with lc_r2_c2:
    #     st.slider("CB Dummy Var 05", min_value=0, max_value=100, value = 70)
    #
    # with lc_r2_c3:
    #     st.slider("CB Dummy Var 06", min_value=0, max_value=100, value = 30)





add_footer()
