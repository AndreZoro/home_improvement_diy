import os
import base64
import streamlit as st


def get_base64_of_bin_file(bin_file):
    # breakpoint()
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def get_img_with_href(local_img_path, img_desc="no description", target_url="not_defined", width=100, height=100):
    # breakpoint()
    img_format = os.path.splitext(local_img_path)[-1].replace(".", "")
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f"""
    <a href="{target_url}">
            <img src="data:image/{img_format};base64,{bin_str}" style="width:{100}%; height:{100}%" />
        </a>"""
    # return html_code
    return st.markdown(html_code,
            unsafe_allow_html=True
        )

