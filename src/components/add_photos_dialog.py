import streamlit as st
from src.database.db import create_subject
from PIL import Image


@st.dialog("Capture or upload photos")
def add_photos_dialog():
    st.write("Add classroom photos for attendance")
    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab =  "camera"
    
    
    tab1, tab2 = st.columns(2)
    
    with tab1:
        type_cmr = "primary" if st.session_state.photo_tab == "camera" else "tertiary"
        if st.button("Camera", width="stretch", type=type_cmr):
            st.session_state.photo_tab =  "camera"
            # st.rerun()
    
    with tab2:
        type_upl = "primary" if st.session_state.photo_tab == "upload" else "tertiary"
        if st.button("Upload", width="stretch", type=type_upl):
            st.session_state.photo_tab =  "upload"
            # st.rerun()
            
    if st.session_state.photo_tab == "camera":
        cam_photo = st.camera_input("Take snapshot", key="dialog_cam")
        
            # st.rerun()
            
    elif st.session_state.photo_tab == "upload":
        upload_files = st.file_uploader("chose image files",type=["jpg", "png", "jpeg"] ,accept_multiple_files=True, key="dialog_upl")
        
    
    st.divider()
    
    if st.button("Done", type='primary', width="stretch"):
        if st.session_state.photo_tab == "upload" and upload_files:
            for f in upload_files:
                st.session_state.attendance_images.append(Image.open(f))
            st.toast("Photo Uploaded successfully")
        elif st.session_state.photo_tab == "camera" and cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast("Photo captured successfully")
        st.rerun()