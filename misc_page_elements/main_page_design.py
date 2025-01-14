import os
import random
from pathlib import Path
import streamlit as st
import pyvista as pv

from pyvista import themes

pv.set_plot_theme(themes.DarkTheme())

from stpyvista import stpyvista
from stpyvista.utils import start_xvfb

from stpyvista.trame_backend import stpyvista as stpv_trame

import tempfile
import requests

from misc_page_elements.part_selection_bar import build_random_top_bar_part_selection
from misc_page_elements.footer import add_footer
from misc_page_elements.misc_helpers import return_part_config
from misc_page_elements.feedback_helpers import client_feedback_section
from misc_page_elements.download_helpers import download_part

from geo_parts.drawer_handle_V01 import create_handle

from misc_page_elements.session import get_session



def build_page(part_config):

    build_random_top_bar_part_selection()

    help_expander_place_holder = st.empty()

    part_images, three_d_window, part_controls = st.columns([1, 4, 2])

    with part_images:
        images = part_config["hero_images"]
        random.shuffle(images)
        for image in images:
            st.image(image[0])


    with three_d_window:
        three_dee_placeholder = st.empty()
        # with three_dee_placeholder:
        #     plotter = pv.Plotter(border=False)
        #     plotter.background_color = "#f0f8ff"
        #     "static/stl_files/simple_strap_clip_V01.stl"
        #     if st.session_state["stl_file"] is None:
        #         part_file, _ = create_handle(sid=session_id)
        #         st.session_state["stl_file"] = part_file
        #     # if st.session_state['stl_file'] == "static/stl_files/simple_strap_clip_V01.stl":
        #     # st.write(f"READING STL FILE : {st.session_state['stl_file']}")
        #     reader = pv.STLReader(st.session_state["stl_file"])
        #     ## Read data and send to plotter
        #     mesh = reader.read()
        #     # mesh = mesh.subdivide(3, method='loop')
        #     # plotter.enable_eye_dome_lighting()
        #     plotter.add_mesh(
        #         mesh,
        #         color="orange",
        #         pbr=True,
        #         metallic=0.5,
        #         roughness=0.2,
        #         diffuse=0.9,
        #         smooth_shading=True,
        #         split_sharp_edges=True,
        #         specular=0.3,
        #     )
        #
        #     plotter.view_vector([1, 1, 1])
        #     stpyvista(plotter, key=f"plotter_{st.session_state['stl_file']}")

    with part_controls:
        part_controls_placeholder = st.container()
        # with st.form("Define Drawer Handle Design:"):
        #     with st.expander("Basic Settings", expanded=True):
        #         h_width = st.slider(
        #             "Handle Width",
        #             min_value=10.0,
        #             max_value=350.0,
        #             value=140.0,
        #             step=0.1,
        #             help="Wheel (rim) diameter in mm",
        #         )
        #         h_height = st.slider(
        #             "Handle Height",
        #             min_value=10.0,
        #             max_value=100.0,
        #             value=25.0,
        #             step=0.1,
        #             help="Axel diameter in mm",
        #         )
        #         h_thickness = st.slider(
        #             "Handle thickness",
        #             min_value=1.0,
        #             max_value=15.0,
        #             value=4.0,
        #             step=0.5,
        #             help="Wheel (rim) width in mm",
        #         )
        #
        #         b_width = st.slider(
        #             "Base Width",
        #             min_value=10.0,
        #             max_value=450.0,
        #             value=100.0,
        #             step=0.1,
        #             help="Wheel (rim) diameter in mm",
        #         )
        #         b_height = st.slider(
        #             "Base Height",
        #             min_value=2.0,
        #             max_value=30.0,
        #             value=8.0,
        #             step=0.1,
        #             help="Axel diameter in mm",
        #         )
        #         b_thickness = st.slider(
        #             "Base thickness",
        #             min_value=2.0,
        #             max_value=25.0,
        #             value=9.0,
        #             step=0.1,
        #             help="Wheel (rim) width in mm",
        #         )
        #
        #         st1, st2 = st.columns(2)
        #         with st1:
        #             screw_dia = st.slider(
        #                 "Screw Diameter",
        #                 min_value=1.0,
        #                 max_value=10.0,
        #                 value=3.2,
        #                 step=0.2,
        #                 help="Screw diameter in mm (An m4 screw would be 4mm)",
        #             )
        #         with st2:
        #             screw_distance = st.slider(
        #                 "Screw Distance in mm",
        #                 min_value=10.0,
        #                 max_value=200.0,
        #                 value=64.0,
        #                 step=0.5,
        #                 help="How far are the mounting screws appart?",
        #             )
        #     with st.expander("Front Face Design", expanded=False):
        #         st.write("This is still missing!")
        #
        #     submitted = st.form_submit_button(
        #         "Generate Your Part", use_container_width=True
        #     )
        #
        #     if submitted:
        #         # st.write("Creating part...")
        #
        #         part_file, msgs = create_handle(
        #             h_width,
        #             h_height,
        #             h_thickness,
        #             b_width,
        #             b_thickness,
        #             b_height,
        #             screw_dia,
        #             screw_distance,
        #             session_id,
        #         )
        #
        #         st.session_state["stl_file"] = part_file
        #
        #         for msg in msgs:
        #             st.toast(msg)
        #
        #         with three_dee_placeholder:
        #             plotter.clear()
        #             reader = pv.STLReader(st.session_state["stl_file"])
        #             ## Read data and send to plotter
        #             mesh = reader.read()
        #
        #             plotter.add_mesh(
        #                 mesh,
        #                 color="orange",
        #                 pbr=True,
        #                 metallic=0.5,
        #                 roughness=0.2,
        #                 diffuse=0.9,
        #                 smooth_shading=True,
        #                 split_sharp_edges=True,
        #                 specular=0.3,
        #             )
        #
        #             plotter.view_vector([1, 1, 1])
        #             stpyvista(plotter, key=f"plotter_{st.session_state['stl_file']}")

        # download_part(st.session_state["stl_file"], st.session_state["part_name"])
        # download_part()
        dl_buttons_placeholder = st.container()
        client_feedback_section()

    add_footer()

    return help_expander_place_holder, three_dee_placeholder, part_controls_placeholder, dl_buttons_placeholder

