import streamlit as st


def student_screen():
    
    st.write("Welcome, Student!")
    col1, col2 = st.columns(2,gap="small")
    with col1:
       if st.button("Teacher portal", width="stretch"):
           st.session_state['login_type'] = "teacher"
           st.rerun()

    with col2:
        if st.button("Home", width="stretch"):
           st.session_state['login_type'] = None
           st.rerun()
