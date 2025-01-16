import random
import streamlit as st
from misc_page_elements.image_helpers import get_img_with_href
from mega_shaper_config import return_reg_parts

reg_parts = return_reg_parts()
random_part_list=list(reg_parts.keys())

def build_random_top_bar_part_selection(total_cols = 7):
    """
    Creates the top bar with the 7 suggested parts.

    TODO: 1. take an input number to set the number of columns
          2. take the category string to show more parts of the same category
    """

    random.shuffle(random_part_list)
    random_parts = random_part_list[:total_cols-2]
    # breakpoint()
    col1, col2, col3, col4, col5, col6, col7 = st.columns(total_cols)

    with col1:
        # st.image("static/images/all_parts.png", caption="Check out all parts")
        get_img_with_href("static/images/all_parts.png","0.0.0.0")

        # st.markdown("[![Check out all parts](static/images/all_parts.png)](https://mantiumcae.com/)")
    with col2:
        get_img_with_href(reg_parts[random_parts[0]]["main_image"][0],random_parts[0],random_parts[0])
        # get_img_with_href("static/images/all_parts.png","bla")
        # st.image("static/images/all_parts.png", caption="Corner Braket with 2 sides")
    with col3:
        get_img_with_href(reg_parts[random_parts[1]]["main_image"][0],random_parts[1],random_parts[1])
        # st.image("static/images/all_parts.png", caption="Corner Braket with 2 sides")
    with col4:
        get_img_with_href(reg_parts[random_parts[2]]["main_image"][0],random_parts[2],random_parts[2])
        # st.image("static/images/all_parts.png", caption="Corner Braket with 2 sides")
    with col5:
        get_img_with_href(reg_parts[random_parts[3]]["main_image"][0],random_parts[3],random_parts[3])
        # st.image("static/images/all_parts.png", caption="Corner Braket with 2 sides")
    with col6:
        get_img_with_href(reg_parts[random_parts[4]]["main_image"][0],random_parts[4],random_parts[4])
        # st.image("static/images/all_parts.png", caption="Corner Braket with 2 sides")
    with col7:
        get_img_with_href("static/images/random_part.png",random_part_list[-1])
        # st.image("static/images/random_part.png", caption="Check out a random part")
