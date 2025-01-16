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

from geo_parts.coffee_dosing_funnel_V01 import create_coffee_dosing_funnel_V01

from misc_page_elements.session import get_session


part_config = return_part_config(str(Path(__file__).stem))
session_id = get_session()
# st.session_state["stl_file"] = None
st.session_state["part_name"] = part_config["name"]


if "IS_XVFB_RUNNING" not in st.session_state:
    start_xvfb()
    st.session_state.IS_XVFB_RUNNING = True

(
    help_expander_place_holder,
    three_dee_placeholder,
    part_controls_placeholder,
    dl_buttons_placeholder,
) = build_page(part_config)

with help_expander_place_holder:
    with st.expander(part_config["titel"]):
        st.write(
            """
            General dimensions to design your own coffee dosing funnel:
        """
        )

with three_dee_placeholder:
    plotter = pv.Plotter(border=False)
    plotter.background_color = "#1e1e27"
    "static/stl_files/simple_strap_clip_V01.stl"
    # if st.session_state["stl_file"] is None:
    if "stl_file" not in st.session_state:
        # print("SOMEHOW ABOUT TO RECREATE FROM SCRATCH:")
        part_file, _ = create_coffee_dosing_funnel_V01()
        st.session_state.stl_file = part_file
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

    plotter.view_vector([-1, -1, 1])
    stpyvista(plotter, key=f"plotter_{st.session_state['stl_file']}")


with part_controls_placeholder:
    with st.form("Define main dimensions:"):

        i_dia = st.slider(
            "Inner filter diameter in mm",
            min_value=30.0,
            max_value=80.0,
            value=58.0,
            step=0.1,
            help="Inside diamater of the portafilter. Common sizes are 54, 57 and 58.3 mm",
        )
        i_dpth = st.slider(
            "Depth of inside part of funnel in mm",
            min_value=4.0,
            max_value=20.0,
            value=8.0,
            step=0.1,
            help="How deep should the inside part go into the filter. The deeper, the better the funnel will stay in place.",
        )
        o_dia = st.slider(
            "Outer filter diameter in mm",
            min_value=30.0,
            max_value=120.0,
            value=68.0,
            step=1.0,
            help="Outside diamater of the portafilter. Should be a bit larger than the inner diameter as it forms the shoulder the funnel will sit on.",
        )
        upper_dia = st.slider(
            "Funnel diameter in mm",
            min_value=30.0,
            max_value=140.0,
            value=74.0,
            step=0.1,
            help="Funnel diamater of the portafilter. Can be a bit larger than the prev. defined outer diameter to catch more coffee powder.",
        )
        top_height = st.slider(
            "Funnel height in mm",
            min_value=8.0,
            max_value=80.0,
            value=20.0,
            step=1.0,
            help="The higher the funnel, the more coffee you will catch. Should not exceed the dimensions of your grinder, though.",
        )
        # f_col1, f_col2 = st.columns([1, 4])
        # with f_col1:
        cutout = st.toggle(
            "Create coutout",
            value=True,
            help="Cutout width to fit into your grinder.",
        )
        # with f_col2:
        cutout_wdth = st.slider(
            "Coutout width in mm",
            min_value=10.0,
            max_value=60.0,
            value=24.0,
            step=1.0,
            help="Cutout width in mm to fit into your grinder.",
        )

        submitted = st.form_submit_button(
            "Generate Your Part", use_container_width=True
        )

        if submitted:

            part_file, msgs = create_coffee_dosing_funnel_V01(
                i_dia,
                i_dpth,
                o_dia,
                upper_dia,
                top_height,
                cutout,
                cutout_wdth,
                # sid=session_id,
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

            # st.write(f'{st.session_state["stl_file"]} - {st.session_state["part_name"]}')

        with dl_buttons_placeholder:
            download_part(st.session_state["stl_file"], st.session_state["part_name"])
