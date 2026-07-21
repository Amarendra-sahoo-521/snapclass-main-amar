import streamlit as st
from src.database.db import create_subject

@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of a new subject")
    s_name = st.text_input("Subject Name", placeholder="AI/ML") 
    s_code = st.text_input("Subject Code", placeholder="CS101") 
    s_sec = st.text_input("Section", placeholder="A")
    
    if st.button("Create New Subject", type="primary", width="stretch"):
        if s_name and s_code and s_sec:
            try:
                create_subject(name=s_name,subject_code=s_code,section=s_sec, teacher_id=teacher_id)
                st.toast("👍 Subject created Successfully")
                st.rerun()
            except Exception as e:
                st.error(f"Error {str(e)}")
        
        else:
            st.warning("please fill all the fields")
    
    if st.button("cancel", type="tertiary", width="stretch"):
        st.rerun()