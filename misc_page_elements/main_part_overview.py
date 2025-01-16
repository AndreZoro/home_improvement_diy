import streamlit as st

from mega_shaper_config import return_reg_parts
from misc_page_elements.misc_helpers import return_part_config, get_parts_for_tag, chunk_up_list
from misc_page_elements.image_helpers import get_img_with_href

N_PART_COLS = 5

reg_parts = return_reg_parts()
tag_to_part, tags = get_parts_for_tag(reg_parts)
tags.remove("first_demo_parts")
tags = ["first_demo_parts"] + tags


@st.dialog("All Parts Overview:")
def part_overview_overlay():
    build_part_overview()


def build_part_overview():
    overview_container = st.container()
    with overview_container:
        for tag in tags:
            st.subheader(f"{tag}", divider="blue")
            sub_parts = tag_to_part[tag]
            chunked_sub_parts = chunk_up_list(sub_parts, N_PART_COLS)
            cols = st.columns(N_PART_COLS)
            for idx, col in enumerate(cols):
                with col:
                    for p in chunked_sub_parts[idx]:
                        get_img_with_href(reg_parts[p]["main_image"][0],reg_parts[p]["main_image"][1],p)
                        st.write(reg_parts[p]["name"])
    return overview_container



