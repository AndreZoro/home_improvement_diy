import streamlit as st


@st.dialog("Download part")
def download_cad(file_name, part_name):
    st.write("\n\n- WIP - \n\n")
    st.header("Download your part either as stl or step.")
    stl_col, step_col = st.columns(2)
    with stl_col:
        # st.button("Download stl", help="Download your part as stl.", use_container_width=True)
        # print(f"\nABOUT TO DOWNLOAD FILE: {file_name}\n")
        with open(file_name, "rb") as stl_file:
            # st.download_button('Download your rim as stl', stl_file, file_name='your_cool_rim.stl')
            st.download_button('Download stl', stl_file, file_name=f'{part_name}.stl')

    with step_col:
        st.button("Download STEP", help="Download your part as STEP.", use_container_width=True)

    st.write("\n\n- WIP - \n\n")

@st.dialog("Buy your part")
def buy_3d_part():
    st.write("\n\n- WIP - \n\n")
    st.header("Get your part 3D printed and shipped to you by one of our partners.")
    st.write("\n\n- WIP - \n\n")


def download_part(file_name, part_name):
# def download_part():
    # file_name, part_name = st.session_state["stl_file"], st.session_state["part_name"]
    download_col, buy_col = st.columns(2)
    with download_col:
        if st.button("Download Part", help="Downlaod your part, either as stl or step.", use_container_width=True):
            download_cad(file_name, part_name)
    with buy_col:
        if st.button("Buy your part", help="Get your part 3D printed and shipped to you by one of our partners.", use_container_width=True):
            buy_3d_part()
