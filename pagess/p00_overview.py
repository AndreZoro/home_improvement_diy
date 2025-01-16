import streamlit as st
from misc_page_elements.footer import add_footer
from mega_shaper_config import return_reg_parts
from misc_page_elements.misc_helpers import return_part_config, get_parts_for_tag, chunk_up_list
from misc_page_elements.image_helpers import get_img_with_href
from misc_page_elements.main_part_overview import build_part_overview

N_PART_COLS = 5

reg_parts = return_reg_parts()
tag_to_part, tags = get_parts_for_tag(reg_parts)




@st.dialog("Coming Soon")
def coming_soon_dialog(link_str):
    st.header(link_str)
    st.write("will soon be ready for you to visit")

st.title(
    "The best geometry designer out there (maybe not, but at least easy to use...)"
)


build_part_overview()

# for tag in tags:
#     st.subheader(f"{tag}", divider="blue")
#     sub_parts = tag_to_part[tag]
#     chunked_sub_parts = chunk_up_list(sub_parts, N_PART_COLS)
#     cols = st.columns(N_PART_COLS)
#     for idx, col in enumerate(cols):
#         with col:
#             for p in chunked_sub_parts[idx]:
#                 get_img_with_href(reg_parts[p]["main_image"])
#                 st.write(p)

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

add_footer()

# app_col_01, app_col_02 = st.columns(2)
#
# with app_col_01:
#     if st.button("Go to Home Decoration Super Shapes"):
#         coming_soon_dialog("DIY Home Deco parts, ")
#
# with app_col_02:
#     if st.button("Gadget Super Shapes"):
#         coming_soon_dialog("DIY parts for your gadgets, ")
