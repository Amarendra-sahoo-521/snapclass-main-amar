import streamlit as st
import numpy as np
from PIL import Image
from ui.base_layout import style_base_layout, style_background_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer_home
from src.components.subject_card import subject_card
from src.components.enroll_dialog import enroll_dialog
from src.pipelines.face_pipeline import predict_attendance, get_face_embedding, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_student_by_id, create_student, get_my_enrolled_courses, remove_my_enrolled_courses, remove_my_enrolled_courses_attendance


def student_screen():
    style_base_layout()
    style_background_dashboard()
    
    
    
    col1, col2 = st.columns(2,gap="small", vertical_alignment="center")
    
    
    with col1:
        header_dashboard()
       
    with col2:
        if "student_data" in st.session_state:
                student = st.session_state["student_data"]
                st.subheader(f"""Welcome {student["name"]}""")
                if st.button("Logout", width="stretch" , shortcut='control+shift+backspace', icon=':material/logout:'):
                    st.session_state['login_type'] = None
                    del st.session_state.student_data
                    st.rerun()
        else:
            if st.button("Home", width="stretch" , shortcut='control+backspace', icon=':material/home:'):
                st.session_state['login_type'] = None
                st.rerun()
           
    if "student_data" in st.session_state:
        student_dashboard()
    # elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type == "login":
    elif "student_login_type" not in st.session_state or st.session_state.student_login_type == "login":
        student_login_form()
    elif st.session_state.student_login_type == "register":
        student_registration_form()
    
    
    
    footer_home()


def student_login_form():
    st.header("Login With FaceID",text_alignment="center")
    st.space()
    st.space()
    photo_src = st.camera_input("position your face in center")
    
    if photo_src:
       img = np.array(Image.open(photo_src))
       
       with st.spinner("AI is scanning"):
           detected, all_ids, num_faces = predict_attendance(img)
           
           if num_faces == 0:
               st.warning("face not found")
           elif num_faces > 1:
               st.warning("multiple face found")
           else:
               if detected:
                   with st.spinner("please wait"):
                        student_id = list(detected.keys())[0]
                        student = get_student_by_id(student_id)

                        if student:
                            st.session_state.student_data = student[0]
                            st.session_state.user_role = "student"
                            st.session_state['login_type'] = "student"
                            st.session_state.is_logged_in = True
                            st.toast(f"👋 welcome back {student[0]["name"]}")
                            import time
                            time.sleep(1)
                            st.rerun()
               else:
                   st.info("Face not recognized! you might be a new student!")
                   st.session_state.student_login_type = "register"
                   st.session_state.new_student_img_src = photo_src
                   import time
                   time.sleep(1)
                   st.rerun()
                

def student_registration_form():
    st.header("Enroll as a Student",text_alignment="center")
    st.space()
    st.space()
    new_name = st.text_input("Enter Your Full Name", placeholder="E.g. Amarendra Sahoo")
    
    st.subheader("Optional: Voice Enrollment")
    st.info("Enroll your voice only attendance")
    
    audio_data = None
    
    try:
        audio_data = st.audio_input("read a short sentence like i am present i am amarendra")
        # print("res--->",audio_data)
    except Exception:
        st.error("audio data failed")
    
    if st.button("Create Account",type="primary"):
        if new_name:
            with st.spinner("creating Student profile"):
                img = np.array(Image.open(st.session_state.new_student_img_src))
                embeddings = get_face_embedding(img)
                if embeddings:
                    face_emb = embeddings[0].tolist()
                    voice_emb = None
                    if audio_data :
                        voice_emb = get_voice_embedding(audio_data.read())
                        # print("res--->1",voice_emb)

                    response_data = create_student(name=new_name, face_embedding=face_emb, voice_embedding=voice_emb)
                    
                    if response_data:
                        train_classifier() 
                        st.session_state.student_data = response_data[0]
                        st.session_state.user_role = "student"
                        st.session_state['login_type'] = "student"
                        st.session_state.is_logged_in = True
                        st.toast(f"👋 Hi {new_name} profile create successfully")
                        import time
                        time.sleep(1)
                        st.rerun()
                else:
                    st.error("Could not find your facial feature for registration")
        else:
            st.warning("enter your name")
    


def student_dashboard():
    student = st.session_state["student_data"]
    s_id = student["student_id"]
    s1, s2 = st.columns(2)
    
    with s1:
        st.subheader("Your Enrolled Subjects")
    with s2:
        if st.button("Enroll in Subject", type="primary", width="stretch"):
           enroll_dialog() 
           
    with st.spinner("loading your Enrolled courses"):
        my_courses = get_my_enrolled_courses(student_id=s_id)
        
        if my_courses:
            cols = st.columns(2)
            for i,subject in enumerate(my_courses):
                subject_id = subject["subject_id"]
                sub = subject["subjects"]
                my_attendance =sub["attendance_log"]
                total_classes = len(my_attendance)
                present_classes = sum(1 for record in my_attendance if record["is_present"] )
                
                # print("total class",total_classes )
                # print("present class",present_classes )
                stats = [
                    ("⏰", "Classes", total_classes),
                    ("✅", "Attended", present_classes),
                ]
            
                st.space()
                def un_enroll():
                    if st.button("Un Enroll This Course",width="stretch", type="tertiary", icon=":material/delete_forever:" , key=sub["subject_code"] , ):
                        remove_my_enrolled_courses(subject_id,s_id)
                        remove_my_enrolled_courses_attendance(subject_id,s_id)
                        st.toast("👍course unEnrolled successfully")
                        st.rerun()
                with cols[i % 2]:
                    subject_card(
                        name=sub["name"],
                        code=sub["subject_code"],
                        section=sub["section"],
                        stats=stats,
                        footer_callback=un_enroll,
                    )
                        
       