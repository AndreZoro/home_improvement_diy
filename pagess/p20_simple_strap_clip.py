import os
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

from geo_parts.simple_strap_clip_V01 import build_strap_clip

from misc_page_elements.session import get_session


part_config = return_part_config(str(Path(__file__).stem))
session_id = get_session()

# st.session_state["stl_file"] = None
st.session_state["part_name"] = part_config["name"]

if "IS_XVFB_RUNNING" not in st.session_state:
    start_xvfb()
    st.session_state.IS_XVFB_RUNNING = True


build_random_top_bar_part_selection()

# st.subheader("Design a corner braket to your own specifications.")
with st.expander(part_config["titel"]):
    st.write(
        """
        Here we can add help for the current part.
    """
    )


part_images, three_d_window, part_controls = st.columns([1, 4, 2])

with part_images:
    for image in part_config["hero_images"][:3]:
        st.image(image[0])


with three_d_window:
    three_dee_placeholder = st.empty()
    with three_dee_placeholder:
        plotter = pv.Plotter(border=False)
        # plotter.background_color = "#f0f8ff"
        plotter.background_color = "#1e1e27"
        "static/stl_files/simple_strap_clip_V01.stl"
        # if st.session_state["stl_file"] is None:
        if "stl_file" not in st.session_state:
            stl_file_name, _ = build_strap_clip()
            st.session_state["stl_file"] = stl_file_name
        # if st.session_state['stl_file'] == "static/stl_files/simple_strap_clip_V01.stl":
        # st.write(f"READING STL FILE : {st.session_state['stl_file']}")
        reader = pv.STLReader(st.session_state["stl_file"])
        ## Read data and send to plotter
        mesh = reader.read()
        plotter.add_mesh(
            mesh,
            color="orange",
            specular=0.5,
            # show_edges=True,
        )

        plotter.view_vector([1, -1, 1])
        stpyvista(plotter, key=f"plotter_{st.session_state['stl_file']}")

with part_controls:
    # width=20, thickness=3, height=22, layer_width=0.4, n_shells=3,sid='none'
    # with st.expander("Basic Settings", expanded=True):
    with st.form("Define Strap Clip Design:"):
        width = st.slider(
            "Strap Width [mm]",
            min_value=5.0,
            max_value=100.0,
            value=20.0,
            step=1.0,
            help="Width of your strap in mm.",
        )
        thickness = st.slider(
            "Strap Thickness [mm]",
            min_value=1.0,
            max_value=20.0,
            value=3.0,
            step=0.25,
            help="Total thickness of your strap in mm.",
        )
        height = st.slider(
            "Clip Height [mm]",
            min_value=2.0,
            max_value=200.0,
            value=20.0,
            step=1.0,
            help="How tall you want your clip to be in mm.",
        )
        layer_width = st.slider(
            "Layer Width [mm]",
            min_value=0.1,
            max_value=1.0,
            value=0.4,
            step=0.1,
            help="Approx width of the layers created by your printer in mm. Nozzel diameter is perfect for this.",
        )
        n_shells = st.slider(
            "N Shells",
            min_value=1,
            max_value=20,
            value=3,
            step=1,
            help="How many shells / layer lines the clip should be made of. Too many makes the clip very rigid while too few make it too flexible. 3 seems to be the best compromize.",
        )

        submitted = st.form_submit_button(
            "Generate Your Part", use_container_width=True
        )
        if submitted:
            # st.write("Creating part...")

            stl_file_name, messages = build_strap_clip(
                width, thickness, height, layer_width, n_shells
            )

            st.session_state["stl_file"] = stl_file_name
            for msg in messages:
                st.toast(msg)

            # st.write(f"ST STL STATE: {st.session_state['stl_file']}")
            with three_dee_placeholder:
                plotter.clear()
                # st.write(f"About to read {stl_file_name}")
                reader = pv.STLReader(st.session_state["stl_file"])
                ## Read data and send to plotter
                mesh = reader.read()
                # Add the new mesh
                plotter.add_mesh(mesh, color="orange", specular=0.5)
                # st.write("Added new mesh")
                #
                # # Render the updated plot
                plotter.render()
                stpyvista(plotter)
            #
            # # st.write(stl_file_name)

    download_part(st.session_state["stl_file"], "strap_clip")
    client_feedback_section()

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
