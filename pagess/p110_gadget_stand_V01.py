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

from geo_parts.gadget_stand_v01 import create_gadget_stand_V01, create_gadget_dummy_V01

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
    with st.expander(part_config["titel"] + " (expand for help)"):
        st.markdown(
            '''
            ## General:
            Design a simple stamd for your devices and gadgets. Basically, you only have to define the dimensions of your device:
            - Width,
            - Height
            - and thickness
            in mm. In addition you can define a slant angle in degrees. This value defines how much your device "layes back."
            The stand might appear a bit long, it is designed so you can put your device into it in either direction without it tipping over.

            And, if you have a light enough phone, you might want to attach it to the top of your laptop screen.
            If so, just activate the selector and enter the thickness of your screen.

            ## Design Hints:
            This part is pretty simple to define. The main dimensions that help to make your part nice and with a snug fit, are the thickness of the device and of the lapto screen. If you gap is too small, you are in back luck, as you cannot fit your device into the part. If your dimensions are too large the device will fit, but it might be a bit too loose.

            ## 3D Print:
            This part is very easy to print on a standard FDM printer. Just print with a side laying down. This way, the layers do not have to support the main loads and the thin parts will not snap off.
        '''
        )

with three_dee_placeholder:
    plotter = pv.Plotter(border=False)
    plotter.background_color = "#1e1e27"
    if "stl_file" not in st.session_state:
        part_file, _ = create_gadget_stand_V01()
        st.session_state.stl_file = part_file
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


    #Add the device dummy part
    if "stl_dummy_file" not in st.session_state:
        dummy_part_file = create_gadget_dummy_V01()
        st.session_state.stl_dummy_file = dummy_part_file
        dummy_reader = pv.STLReader(st.session_state["stl_dummy_file"])
        dummy_mesh = dummy_reader.read()
        plotter.add_mesh(
            dummy_mesh,
            color="grey",
            pbr=False,
            metallic=0.5,
            roughness=0.2,
            diffuse=0.9,
            smooth_shading=True,
            split_sharp_edges=True,
            specular=0.3,
            opacity = 0.6,
        )

    plotter.view_vector([ 1,  1, -1], [0,1,0])
    stpyvista(plotter, key=f"plotter_{st.session_state['stl_file']}")


with part_controls_placeholder:
    with st.form("Define main dimensions:"):

        dev_w = st.slider(
            "Device width in mm",
            min_value=15.0,
            max_value=120.0,
            value=80.0,
            step=1.0,
            help="Width of your device in mm",
        )
        dev_h = st.slider(
            "Device height in mm",
            min_value=30.0,
            max_value=220.0,
            value=140.0,
            step=1.0,
            help="Height of your device in mm",
        )
        dev_t = st.slider(
            "Device thickness in mm",
            min_value=2.0,
            max_value=20.0,
            value=12.0,
            step=0.2,
            help="Thickness of your device in mm. This one determines how snug your device will fit!",
        )
        slant = st.slider(
            "Slant angle in degrees",
            min_value=10.0,
            max_value=40.0,
            value=20.0,
            step=1.0,
            help="This one determines how much your device will lean back.",
        )
        ls_col1, ls_col2 = st.columns([4, 4])
        with ls_col1:
            laptop_slot = st.toggle(
                "Create a slot for your laptop screen.",
                value=True,
                help="With this slot, you can stick your phone on top of your laptop screen. Keep in mind, that this is a good way to damage your laptop!",
            )
        with ls_col2:
            laptop_thickness = st.slider(
                "Thickness of your laptop screen in mm",
                min_value=3.0,
                max_value=10.0,
                value=5.4,
                step=0.2,
                help="Thickness of your laptop screen in mm.",
            )

        submitted = st.form_submit_button(
            "Generate Your Part", use_container_width=True
        )

        if submitted:

            part_file, msgs = create_gadget_stand_V01(
                dev_w,
                dev_h,
                dev_t,
                slant,
                laptop_slot,
                laptop_thickness,
            )

            st.session_state["stl_file"] = part_file
            st.session_state["stl_dummy_file"] = create_gadget_dummy_V01(
                dev_w,
                dev_h,
                dev_t,
                slant,)

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

                #Add the device dummy part
                dummy_reader = pv.STLReader(st.session_state["stl_dummy_file"])
                dummy_mesh = dummy_reader.read()
                plotter.add_mesh(
                    dummy_mesh,
                    color="grey",
                    pbr=False,
                    metallic=0.5,
                    roughness=0.2,
                    diffuse=0.9,
                    smooth_shading=True,
                    split_sharp_edges=True,
                    specular=0.3,
                    opacity = 0.6,
                )

                plotter.view_vector([ 1,  1, -1], [0,1,0])
                stpyvista(plotter, key=f"plotter_{st.session_state['stl_file']}")

            # st.write(f'{st.session_state["stl_file"]} - {st.session_state["part_name"]}')

        with dl_buttons_placeholder:
            download_part(st.session_state["stl_file"], st.session_state["part_name"])
