import streamlit as st
from src.database.db import get_subject_by_code, get_subject_student,enroll_student_to_subject 
import time

@st.dialog("Enroll in subject")
def enroll_dialog():
    st.write("Enter the subject code provided by your teacher")
    s_code = st.text_input("Subject Code", placeholder="CS101") 
    
    if st.button("Enroll Now", type="primary", width="stretch"):
        if s_code:
            try:
                exist_subject = get_subject_by_code(s_code)
                if not exist_subject:
                    st.toast("❌ Subject Not Exist")
                else:
                    student = st.session_state["student_data"]
                    s_id = student["student_id"]
                    is_enrolled_student = get_subject_student(subject_id=exist_subject[0]["subject_id"], student_id=s_id)
                    if is_enrolled_student:
                        st.toast("❗Student Already Registered")
                    else:
                        try:
                            enroll_student_to_subject(subject_id=exist_subject[0]["subject_id"], student_id=s_id)
                            st.toast("👍 Subject Enrolled Successfully")
                        except Exception as e:
                            st.error("fail to enroll")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error {str(e)}")
                st.stop()
        
        else:
            st.warning("please Enter the Subject code")
    
    if st.button("cancel", type="tertiary", width="stretch"):
        st.rerun()