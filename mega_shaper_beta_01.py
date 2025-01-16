import base64
import streamlit as st
import pyvista as pv

from pyvista import themes

pv.set_plot_theme(themes.DarkTheme())

from stpyvista import stpyvista
import tempfile

import requests

from misc_page_elements.session import get_session

session_id = get_session()

st.set_page_config(
    page_title="MEGA Shaper - Home Improvement DIY Edition",
    page_icon=":nut_and_bolt:",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None,
)


overview_page = st.Page(
    "pagess/p00_overview.py",
    # title="2 Sided Corner Braket",
    # icon=":material/add_circle:"
)
# drawer_handle = st.Page("pagess/90_drawer_handle.py",
#                       title="Design a Nice Drawer Handle",
#                       # icon=":material/add_circle:"
#                       )
drawer_handle_v02 = st.Page(
    "pagess/p91_drawer_handle_V02.py",
    title="Design a Nice Drawer Handle",
    # icon=":material/add_circle:"
)
two_sided_braket = st.Page(
    "pagess/p10_corner_braket_2sided.py",
    title="2 Sided Corner Braket",
    # icon=":material/add_circle:"
)
slotcar_rim = st.Page(
    "pagess/p80_slotcar_rim.py",
    title="Slotcar Rim Designer",
    # icon=":material/add_circle:"
)
simple_strap_clip = st.Page(
    "pagess/p20_simple_strap_clip.py",
    title="Simple Strap Clip",
    # icon=":material/add_circle:"
)
three_sided_braket = st.Page(
    "pagess/p40_corner_braket_3sided.py",
    title="3 Sided Corner Braket",
    # icon=":material/add_circle:"
)
coffee_dosing_funnel = st.Page(
    "pagess/p100_coffee_dosing_funnel_V01.py",
    title="Coffee Dosing Funnel",
    # icon=":material/add_circle:"
)
#
pg = st.navigation(
    [
        overview_page,
        # drawer_handle,
        drawer_handle_v02,
        two_sided_braket,
        slotcar_rim,
        simple_strap_clip,
        three_sided_braket,
        coffee_dosing_funnel,
    ]
)
#
#
#
pg.run()


# st.write(session_id)

# pv.start_xvfb()


#
# r1c1, r1c2, r1c3 = st.columns(3)
#
# with r1c1:
#     st.image("static/images/corner_braket_2sides.png", caption="Corner Braket with 2 sides")
#
# with r1c2:
#     st.image("static/images/cabel_clip.png", caption="Cabel Clip")
#
# with r1c3:
#     st.image("static/images/broomstick_hook.png", caption="Broomstick Hook")
#
#
# r2c1, r2c2, r2c3 = st.columns(3)
#
# with r2c1:
#     st.image("static/images/corner_braket_3sides.png", caption="Corner Braket with 3 sides")
#
# with r2c2:
#     st.image("static/images/vac_adaptor.png", caption="Vacuum Adaptor")
#
# with r2c3:
#     st.image("static/images/coat_hook.png", caption="Coat Hook")
