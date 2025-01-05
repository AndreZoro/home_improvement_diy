import streamlit as st
import base64

from misc_page_elements.main_part_overview import part_overview_overlay


@st.dialog("Data Privacy")
def build_data_priv_popup():
    st.header("!!!  -  WIP  -  !!!")
    st.write("Here is where we should put our data privacy text.")
    st.header("!!!  -  WIP  -  !!!")

@st.dialog("Impressum")
def build_impressum_popup():
    st.header("!!!  -  WIP  -  !!!")
    st.write("Here is where we should put our impressum text.")
    st.header("!!!  -  WIP  -  !!!")

@st.dialog("Get in Touch")
def temp_get_in_touch():
    # TODO: Remove this to a function used globaly on the page
    st.header("!!!  -  WIP  -  !!!")
    st.write("Messages to us will go here")
    st.header("!!!  -  WIP  -  !!!")


def add_footer():
    st.divider()
    st.write("SEO text goes here")
    st.divider()
    fc1, fc2, fc3 = st.columns([3,1,1])
    with fc1:
        st.write("Brought to you by:")
        st.markdown("[![MantiumCAE](https://mantiumcae.com/wp-content/uploads/mantium_CAE_Logo_rgb_small-1.png)](https://mantiumcae.com/)")
    with fc2:
        if st.button("Data Privacy"):
            build_data_priv_popup()
        if st.button("Impressum"):
            build_impressum_popup()
    with fc3:
        if st.button("Get in Touch"):
            temp_get_in_touch()
        if st.button("All Parts"):
            part_overview_overlay()


