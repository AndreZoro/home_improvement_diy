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
    st.markdown("""
                #### Create & Download Custom 3D Models for 3D Printing
                Design and customize 3D models effortlessly with our online parametric modeling tool. Whether you're a maker, engineer, designer, or hobbyist, our web app allows you to create precise, customizable geometries tailored to your needs. Easily adjust parameters, visualize changes in real time, and export high-quality STL files ready for 3D printing. No software installation is required—simply use your browser to generate unique 3D objects for rapid prototyping, functional parts, or creative projects. Start designing today and bring your ideas to life with precision and flexibility!
                """)
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


