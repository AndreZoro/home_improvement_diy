import streamlit as st

@st.dialog("Give us your feedback!")
def feedback_window():
    st.write("\n\n- WIP - \n\n")
    st.header("Please let us know what you think!")
    st.write("\n\n- WIP - \n\n")

def client_feedback_section():
    fb_col1, fb_col2 = st.columns([3,2])
    with fb_col1:
        if st.button("Get in touch with us! (or just rate ->)", help="Any comments, cool ideas or complaints? Please let us know!", use_container_width=True):
            feedback_window()
    with fb_col2:
        st.feedback(options="stars")

