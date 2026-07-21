import streamlit as st
from src.database.db import create_attendance_log, delete_class
import time
@st.dialog("Create New Subject")
def attendance_result_dialog(df, logs):
    st.write("please review the attendance before conforming")
    st.dataframe(df, hide_index=True, width="stretch")
    
    c1, c2 = st.columns(2)
    
    with c1:
        if st.button("Discard", width="stretch"):
            st.session_state["voice_attendance_result"] = None
            delete_class(logs[0]["class_id"])
            st.rerun()
    
    with c2:
        if st.button("Confirm", width="stretch", type="primary"):
            try:
                create_attendance_log(logs)
                st.toast("Attendance taken")
                time.sleep(1)
                st.session_state.attendance_images = []
                st.session_state["voice_attendance_result"] = None
                st.rerun()
            except Exception as e:
                st.error(f"Sync failed: {e}")
            st.rerun()