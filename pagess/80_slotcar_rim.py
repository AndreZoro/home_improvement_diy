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

from geo_parts.slotcar_rim_V01 import make_rim_tire

from misc_page_elements.session import get_session


part_config = return_part_config(str(Path(__file__).stem))
session_id = get_session()

st.session_state["rim_stl_file"] = None
st.session_state["tire_stl_file"] = None


if "IS_XVFB_RUNNING" not in st.session_state:
    start_xvfb()
    st.session_state.IS_XVFB_RUNNING = True


build_random_top_bar_part_selection()

with st.expander(part_config["titel"]):
    st.write(
        """
        General dimensions to design the rim:
    """
    )
    img_col_01,img_col_02,img_col_03 = st.columns(3)
    with img_col_01:
        st.image("static/images/slotcar_rim/main_dims_anot.png")
    with img_col_02:
        st.image("static/images/slotcar_rim/des_dims_anot.png")
    with img_col_03:
        st.image("static/images/slotcar_rim/shoulder_dims_anot.png")


part_images, three_d_window, part_controls = st.columns([1, 4, 2])

with part_images:
    for image in part_config["hero_images"][:3]:
        st.image(image[0])


with three_d_window:
    three_dee_placeholder = st.empty()
    with three_dee_placeholder:
        plotter = pv.Plotter(border=False)
        plotter.background_color = "#f0f8ff"
        "static/stl_files/simple_strap_clip_V01.stl"
        if st.session_state["rim_stl_file"] is None:
            tire_file, _ = make_rim_tire(geo_part="tire", sid = session_id)
            rim_file, _ = make_rim_tire(geo_part="rim", sid = session_id)
            st.session_state["tire_stl_file"] = tire_file
            st.session_state["rim_stl_file"] = rim_file
        # if st.session_state['stl_file'] == "static/stl_files/simple_strap_clip_V01.stl":
        # st.write(f"READING STL FILE : {st.session_state['stl_file']}")
        tire_reader = pv.STLReader(st.session_state["tire_stl_file"])
        rim_reader = pv.STLReader(st.session_state["rim_stl_file"])
        ## Read data and send to plotter
        tire_mesh = tire_reader.read()
        rim_mesh = rim_reader.read()

        plotter.add_mesh(
            tire_mesh,
            color="black", specular=0.25, opacity = 0.6
        )
        plotter.add_mesh(
            rim_mesh,
            color="orange",
            specular=0.5,
        )

        plotter.view_vector([1, 1, 1])
        stpyvista(plotter, key=f"plotter_{st.session_state['rim_stl_file']}")

with part_controls:
    # width=20, thickness=3, height=22, layer_width=0.4, n_shells=3,sid='none'
    # with st.expander("Basic Settings", expanded=True):
    with st.form("Define Slotcar Rim Design:"):
        with st.expander("Basic Settings", expanded=True):
            whl_dia = st.slider("Wheel Diameter", min_value=2.0, max_value=50.0, value=20.0, step=0.1, help="Wheel (rim) diameter in mm")
            axl_dia = st.slider("Axle Diameter", min_value=0.2, max_value=10.0, value=3.0, step=0.1, help="Axel diameter in mm")
            whl_wdt = st.slider("Wheel Width", min_value=2.0, max_value=50.0, value=10.0, step=0.1, help="Wheel (rim) width in mm")
            tre_dia = st.slider("Tire Diameter", min_value=whl_dia, max_value=60.0, value=1.2 * whl_dia, step=0.1, help="Tire diameter in mm\n(Only needed for visualisation purposes)")

        with st.expander("Advanced Settings", expanded=False):
            bck_spc = st.slider("Back Spacing", min_value=0.0, max_value=10.0, value=2.0, step=0.1, help="Help not ready yet")
            cnv_dtp = st.slider("Convex Depth", min_value=0.0, max_value=10.0, value=2.0, step=0.1, help="Help not ready yet")

        with st.expander("Shoulder Settings", expanded=False):
            sld_hgt = st.slider("Shoulder Height", min_value=0.0, max_value=10.0, value=1.0, step=0.1, help="Shoulder Height in mm")
            sld_wdt = st.slider("Shoulder Width", min_value=1.0, max_value=40.0, value=5.0, step=0.1, help="Shoulder Width in mm")
            sld_pos = st.slider("Shoulder Position", min_value=0.0, max_value=30.0, value=2.5, step=0.1, help="Shoulder Position in mm")

        with st.expander("Spoke Design", expanded=False):
            spoke_dropdown = st.selectbox('Select Spoke Type:', ['Speed Disk', 'Lambo Style', 'Spokes'],)
            st.write("Lambo Style rim settings:")
            ls_col1, ls_col2, ls_col3 = st.columns(3)
            with ls_col1:
                n_holes = st.slider("Number of holes in rim", min_value=1, max_value=12, value=5, step=1, help="Choose the number of holes along the main diameter")
            with ls_col2:
                main_dia = st.slider("Main diameter", min_value=1, max_value=12, value=6, step=1, help="In mm, the holes get arranged along this contruction geometry")
            with ls_col3:
                hole_dia = st.slider("Diameter of lambo holes", min_value=1, max_value=12, value=5, step=1, help="In mm")
            st.divider()
            st.write("Spoke Rims are not implemented yet!")

        with st.expander("Printer Settings", expanded=False):
            prt_col1, prt_col2 = st.columns(2)
            with prt_col1:
                lyr_hgt = st.slider("Layer Height", min_value=0.04, max_value=1.0, value=0.12, step=0.01, help="Layer height in mm of fdm 3D printer.")
            with prt_col2:
                nzl_wdt = st.slider("Nozzle Diameter", min_value=0.04, max_value=1.0, value=0.4, step=0.01, help="Nozzel diameter in mm of fdm 3D printer.")

        submitted = st.form_submit_button(
            "Generate Your Part", use_container_width=True
        )
        if submitted:
            # st.write("Creating part...")

            tire_file, _ = make_rim_tire("tire", whl_dia, axl_dia, whl_wdt, tre_dia, bck_spc, cnv_dtp, sld_hgt, sld_wdt, sld_pos, n_holes, main_dia, hole_dia, lyr_hgt, nzl_wdt, spoke_dropdown, session_id)
            rim_file, rim_msgs = make_rim_tire("rim", whl_dia, axl_dia, whl_wdt, tre_dia, bck_spc, cnv_dtp, sld_hgt, sld_wdt, sld_pos, n_holes, main_dia, hole_dia, lyr_hgt, nzl_wdt, spoke_dropdown, session_id)

            st.session_state["tire_stl_file"] = tire_file
            st.session_state["rim_stl_file"] = rim_file

            for msg in rim_msgs:
                st.info(msg)

            with three_dee_placeholder:
                plotter.clear()
                tire_reader = pv.STLReader(st.session_state["tire_stl_file"])
                rim_reader = pv.STLReader(st.session_state["rim_stl_file"])
                ## Read data and send to plotter
                tire_mesh = tire_reader.read()
                rim_mesh = rim_reader.read()

                plotter.add_mesh(
                    tire_mesh,
                    color="black", specular=0.25, opacity = 0.6
                )
                plotter.add_mesh(
                    rim_mesh,
                    color="orange",
                    specular=0.5,
                )

                plotter.view_vector([1, 1, 1])
                stpyvista(plotter, key=f"plotter_{st.session_state['rim_stl_file']}")

    download_part(st.session_state['rim_stl_file'], "slotcar_rim")
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
