import streamlit as st
import segno
import io
import time
from src.database.db import get_subject_by_code, get_subject_student, enroll_student_to_subject

@st.dialog("Enroll in Course")
def auto_enroll_dialog(join_code):
    student = st.session_state["student_data"]
    student_id = student["student_id"]
    try:
        exist_subject = get_subject_by_code(join_code)
        if not exist_subject:
            st.toast("❌ Subject Not Exist")
            time.sleep(1)
            st.query_params.clear()
            st.rerun() 
        else:
            is_enrolled_student = get_subject_student(subject_id=exist_subject[0]["subject_id"], student_id=student_id)
            if is_enrolled_student:
                st.toast("You have Already Registered") 
                # time.sleep(1)
                # st.query_params.clear() 
                # st.rerun()         
    except Exception as e:
                st.error(f"Error {str(e)}")
                st.stop()
                
    st.markdown(f"Would you like to enroll in **{exist_subject[0]["name"]}**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("No thanks", type="tertiary", width="stretch"):
            st.query_params.clear()
            st.rerun()
            
    with col2:
        if st.button("Enroll", type="primary", width="stretch"):
                        try:
                            enroll_student_to_subject(subject_id=exist_subject[0]["subject_id"], student_id=student_id)
                            st.toast("👍 Subject Enrolled Successfully")
                            time.sleep(1)
                            st.query_params.clear() 
                            st.rerun() 
                        except Exception as e:
                            st.error("fail to enroll")
            