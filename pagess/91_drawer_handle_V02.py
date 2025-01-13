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
from misc_page_elements.main_page_design import build_page

from geo_parts.drawer_handle_V02 import create_handle_v02

from misc_page_elements.session import get_session


part_config = return_part_config(str(Path(__file__).stem))
session_id = get_session()
st.session_state["stl_file"] = None


if "IS_XVFB_RUNNING" not in st.session_state:
    start_xvfb()
    st.session_state.IS_XVFB_RUNNING = True

help_expander_place_holder, three_dee_placeholder, part_controls_placeholder = (
    build_page(part_config)
)

with help_expander_place_holder:
    with st.expander(part_config["titel"]):
        st.write(
            """
            General dimensions to design the drawer pull / handle.:
        """
        )

with three_dee_placeholder:
    plotter = pv.Plotter(border=False)
    plotter.background_color = "#1e1e27"
    "static/stl_files/simple_strap_clip_V01.stl"
    if st.session_state["stl_file"] is None:
        part_file, _ = create_handle_v02(sid=session_id)
        st.session_state["stl_file"] = part_file
    # if st.session_state['stl_file'] == "static/stl_files/simple_strap_clip_V01.stl":
    # st.write(f"READING STL FILE : {st.session_state['stl_file']}")
    reader = pv.STLReader(st.session_state["stl_file"])
    ## Read data and send to plotter
    mesh = reader.read()
    # mesh = mesh.subdivide(3, method='loop')
    # plotter.enable_eye_dome_lighting()
    plotter.add_mesh(
        mesh,
        color="orange",
        pbr=True,
        metallic=0.5,
        roughness=0.2,
        diffuse=0.9,
        smooth_shading=True,
        split_sharp_edges=True,
        specular=0.3,
    )

    plotter.view_vector([1, 1, 1])
    stpyvista(plotter, key=f"plotter_{st.session_state['stl_file']}")


with part_controls_placeholder:
    with st.form("Define Drawer Handle Design:"):
        with st.expander("Basic Settings", expanded=True):
            h_width = st.slider(
                "Handle Width",
                min_value=10.0,
                max_value=350.0,
                value=120.0,
                step=0.5,
                help="Main handle width in mm",
            )
            h_height = st.slider(
                "Handle Height",
                min_value=10.0,
                max_value=100.0,
                value=30.0,
                step=0.5,
                help="Main handle height in mm",
            )
            h_thickness = st.slider(
                "Handle thickness",
                min_value=1.0,
                max_value=15.0,
                value=4.0,
                step=0.25,
                help="Main handle thickness in mm",
            )
            h_rad = st.slider(
                "Handle Edge Radius",
                min_value=0,
                max_value=100,
                value=30,
                step=1,
                help="Relative slider for corner radius of front face.",
            )
            slant_ang = st.slider(
                "Slant Angle",
                min_value=-45.0,
                max_value=45.0,
                value=20.0,
                step=1.0,
                help="Slant angle of front face in deg.",
            )

        with st.expander("Additional Settings", expanded=False):
            b_thickness = st.slider(
                "Base Thickness",
                min_value=2.0,
                max_value=40.0,
                value=8.0,
                step=0.5,
                help="Defines the distance between drawer and front face of handle (how much space your finger will need) in mm.",
            )
            screw_distance = st.slider(
                "Screw Distance",
                min_value=10.0,
                max_value=120.0,
                value=64.0,
                step=0.1,
                help="Defines the distance between the two mounting screws in mm",
            )
            screw_dia = st.select_slider(
                "Metric Screw Choice",
                options=[
                    "m2",
                    "m3",
                    "m4",
                    "m5",
                    "m6",
                    "m7",
                    "m8",
                ],
                value="m4",
                help="Select the screw size based on metric system.",
            )
        with st.expander("Add Optional Text", expanded=False):
            front_text = st.text_input(
                "Enter some optional text for your handle", value=""
            )

        submitted = st.form_submit_button(
            "Generate Your Part", use_container_width=True
        )

        if submitted:

            # st.write("Hell Yeah Brother")
            part_file, msgs = create_handle_v02(
                h_width,
                h_thickness,
                h_height,
                h_rad,
                b_thickness,
                screw_distance,
                screw_dia,
                slant_ang,
                front_text,
                session_id,
            )

            st.session_state["stl_file"] = part_file

            for msg in msgs:
                st.toast(msg)

            with three_dee_placeholder:
                plotter.clear()
                reader = pv.STLReader(st.session_state["stl_file"])
                ## Read data and send to plotter
                mesh = reader.read()

                plotter.add_mesh(
                    mesh,
                    color="orange",
                    pbr=True,
                    metallic=0.5,
                    roughness=0.2,
                    diffuse=0.9,
                    smooth_shading=True,
                    split_sharp_edges=True,
                    specular=0.3,
                )

                plotter.view_vector([1, 1, 1])
                stpyvista(plotter, key=f"plotter_{st.session_state['stl_file']}")
