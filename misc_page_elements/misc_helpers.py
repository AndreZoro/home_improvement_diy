from mega_shaper_config import return_reg_parts
import streamlit as st

def return_part_config(part_name):
    reg_parts = return_reg_parts()
    if part_name in reg_parts:
        return reg_parts[part_name]
    else:
        st.error(f"Somehow part: {part_name} is not configured correctly!")


def get_parts_for_tag(part_dict):
    tag_part_mapping = {}
    for p_name, items in part_dict.items():
        cats = items["categories"]
        for c in cats:
            if c in tag_part_mapping:
                tag_part_mapping[c].append(p_name)
            else:
                tag_part_mapping[c] = [p_name]

    for p in tag_part_mapping:
        tag_part_mapping[p] = sorted(tag_part_mapping[p])

    return tag_part_mapping, sorted(tag_part_mapping.keys())


def chunk_up_list(lst, chks=5):
    cl = []
    for i in range(chks):
        cl.append([])
    counter = 0
    for l in lst:
        cl[counter].append(l)
        counter += 1
        if counter >= chks:
            counter = 0
    return cl





    #     "10_corner_braket_2sided": {
    #     "categories": ["diy"],
    #     "main_image": "static/images/corner_braket_2sides.png",
    #     "hero_images": [
    #         "static/images/corner_braket_2sides.png",
    #         "static/images/corner_braket_2sides.png",
    #         "static/images/corner_braket_2sides.png",
    #         "static/images/corner_braket_2sides.png",
    #         "static/images/corner_braket_2sides.png",
    #     ],
    #     "titel": "Design a corner braket to your own specifications.",
    # },
    # "20_corner_braket_3sided": {
    #     "categories": ["diy"],
    #     "main_image": "static/images/corner_braket_3sides.png",
    #     "hero_images": [
    #         "static/images/corner_braket_3sides.png",
    #         "static/images/corner_braket_3sides.png",
    #         "static/images/corner_braket_3sides.png",
    #         "static/images/corner_braket_3sides.png",
    #         "static/images/corner_braket_3sides.png",
    #     ],
    #     "titel": "Design a corner braket to your own specifications.",
    # },

