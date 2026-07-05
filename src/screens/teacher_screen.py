import streamlit as st


def teacher_screen():
   
    st.write("Welcome, Teacher!")
    col1, col2 = st.columns(2,gap="small")
    with col1:
       if st.button("Home", width="stretch"):
           st.session_state['login_type'] = None
           st.rerun()
    with col2:
        if st.button("Student portal", width="stretch"):
            st.session_state['login_type'] = "student"
            st.rerun()