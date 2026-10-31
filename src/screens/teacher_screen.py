import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta
from src.components.header import header_dashboard
from src.components.footer import footer_home
from src.components.subject_card import subject_card
from src.components.create_subject_dialog import create_subject_dialog
from src.components.share_subject_dialog import share_subject_dialog
from src.components.attendance_result_dialog import attendance_result_dialog
from src.components.add_photos_dialog import add_photos_dialog
from src.components.dialog_voice_attendance import dialog_voice_attendance
from ui.base_layout import style_base_layout, style_background_dashboard
from src.pipelines.face_pipeline import predict_attendance
from src.database.db import check_teacher_exist,create_teacher, teacher_login, get_my_subjects, get_enrolled_student, get_attendance_for_teacher, create_class, delete_class

def teacher_screen():
    style_base_layout()
    style_background_dashboard()
    
    col1, col2 = st.columns(2,gap="small", vertical_alignment="center")
    
    with col1:
        header_dashboard()
       
    with col2:
        if "teacher" in st.session_state:
            teacher = st.session_state["teacher"]
            st.subheader(f"""Welcome {teacher["name"]}""")
            if st.button("Logout", width="stretch" , shortcut='control+shift+backspace', icon=':material/logout:'):
                st.session_state['login_type'] = None
                del st.session_state.teacher
                st.rerun()
        else:
            if st.button("Home", width="stretch" , shortcut='control+backspace', icon=':material/home:'):
                st.session_state['login_type'] = None
                st.rerun()
    
    if "teacher" in st.session_state:
        teacher_dashboard()
    elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_login_form()
    elif st.session_state.teacher_login_type == "register":
        teacher_register_form()
    
    footer_home()
    
def register_teacher(teacher_user_name, teacher_name, teacher_password,confirm_password):
    if not teacher_user_name or not teacher_name or not teacher_password or not confirm_password:
        return False, "All fields are required!"
    if check_teacher_exist(teacher_user_name):
        return False, "username already taken"
    if teacher_password != confirm_password:
        return False, "password dose not match"
    
    try:
        create_teacher(teacher_user_name, teacher_name, teacher_password)
        return True, "registration successful, Now Login"
    except Exception as e:
        return False, "un expected Error"
 
 
def login_teacher(teacher_user_name,teacher_password):
    if not teacher_user_name or not teacher_password:
        return False
    
    teacher =  teacher_login(teacher_user_name,teacher_password)
    if teacher:
        st.session_state.teacher = teacher
        st.session_state.user_role = "teacher"
        st.session_state.is_logged_in = True
        return True
    else:
        return False 

     
def teacher_dashboard():
    # teacher = st.session_state["teacher"]
    
    
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"
    
    tab1,tab2,tab3 = st.columns(3)
    
    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == "take_attendance" else "tertiary"
        if st.button("Take Attendance", type=type1, width="stretch" , icon=":material/ar_on_you:"):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()
    
    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == "manage_subject" else "tertiary"
        if st.button("Manage Subjects", type=type2, width="stretch" , icon=":material/book_ribbon:"):
            st.session_state.current_teacher_tab = "manage_subject"
            st.rerun()
    
    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == "attendance_record" else "tertiary"
        if st.button("Attendances", type=type3, width="stretch" , icon=":material/cards_stack:"):
            st.session_state.current_teacher_tab = "attendance_record"
            st.rerun()
    st.divider()
    if st.session_state.current_teacher_tab == "attendance_record":
        teacher_tab_attendance_record()
    elif st.session_state.current_teacher_tab == "manage_subject":
        teacher_tab_manage_subject()
    elif st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    
def teacher_login_form():
        st.header("Login Your Teacher profile!",text_alignment="center")
        st.space()
        st.space()
        teacher_user_name = st.text_input("Enter username", placeholder="teacher123")
        teacher_password = st.text_input("Enter password", placeholder="teacher@123",type="password")
        
        st.divider()
        
        btn_col1, btn_col2 = st.columns(2,gap="small", vertical_alignment="center")
    
        with btn_col1:
            if st.button("Login", width="stretch" , shortcut='control+enter', icon=':material/login:'):
                with st.spinner("please wait"):
                    if login_teacher(teacher_user_name,teacher_password):
                        st.toast(f"👋 welcome back {st.session_state.teacher["name"]}")
                        import time
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
            
               
        with btn_col2:
            if st.button("Register instead", width="stretch" , type="primary", icon=':material/app_registration:'):
               st.session_state["teacher_login_type"] = "register"
               st.rerun()
    
def teacher_register_form():
        st.header("Register Your Teacher profile!",text_alignment="center")   
        st.space()
        st.space()
        teacher_user_name = st.text_input("Enter username", placeholder="teacher123")
        teacher_name = st.text_input("Enter Fullname", placeholder="Amarenda sahoo")
        teacher_password = st.text_input("Enter password", placeholder="teacher@123",type="password")
        confirm_password = st.text_input("Confirm password", placeholder="teacher@123",type="password")
        
        st.divider()
        
        btn_col1, btn_col2 = st.columns(2,gap="small", vertical_alignment="center")
    
        with btn_col1:
            if st.button("Register Now", width="stretch" , shortcut='control+enter', icon=':material/login:'):
               success, message = register_teacher(teacher_user_name, teacher_name, teacher_password,confirm_password)
               if success:
                   st.success(message)
                   import time
                   time.sleep(2)
                   st.session_state["teacher_login_type"] = "login"
                   st.rerun()
               else :
                   st.error(message)
        with btn_col2:
            if st.button("Login instead", width="stretch" , type="primary", icon=':material/app_registration:'):
               st.session_state["teacher_login_type"] = "login"
               st.rerun()    
 
def teacher_tab_attendance_record():
    teacher_id = st.session_state.teacher["teacher_id"]
    attendance_for_teacher = get_attendance_for_teacher(teacher_id)
    # st.write("attendance",attendance_for_teacher)
    rows = []
    for cls in attendance_for_teacher:
        logs = cls.get("attendance_log")
        total_student = len(logs)
        present_std = sum(
            1  for present in logs if present["is_present"]
        )
        
        timestamp =  logs[0]["timestamp"] if logs else None
        if timestamp:
            dt_object = datetime.fromisoformat(timestamp.replace("+00", "+00:00"))
            readable_format = dt_object.strftime("%B %d, %Y at %I:%M:%S %p (IST)")
            
        rows.append({
            "Subject" : cls["subjects"]["name"],
            "Time" : readable_format,
            "Student" : f"✅ {present_std} / {total_student}",
        })
    df = pd.DataFrame(rows)
    
    st.dataframe(df, use_container_width=True,hide_index=True)
        
    
    
    
    
def teacher_tab_manage_subject():
    teacher_id = st.session_state.teacher["teacher_id"]
    l,r = st.columns(2)
    
    with l:
        st.subheader("Manage Subjects")
    with r:
        if st.button("Create Subject", width="stretch"):
            create_subject_dialog(teacher_id)
            
            
    # subject list
    subjects = get_my_subjects(teacher_id)
    # print("subjects",subjects)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "Students", sub["total_students"]),
                ("⏰", "Classes", sub["total_classes"]),
            ]
            def share_btn():
                if st.button(f"Share Code: {sub['name']}", key=f"{sub['subject_code']}",width="stretch", icon=":material/share:"):
                    share_subject_dialog(sub["name"], sub['subject_code'])
                    # print("abc")
            st.space()
            
            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=stats,
                footer_callback=share_btn,
            )
    
def teacher_tab_take_attendance():
    
    teacher_id = st.session_state.teacher["teacher_id"]
    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images =[]
        
    my_subjects = get_my_subjects(teacher_id)
    if my_subjects:
        subject_option = {f"{s["name"]} - {s["subject_code"]}": s["subject_id"] for s in my_subjects}
        
    else:
        st.warning("You have not create any subject yet! create a subject first")
        return
    st.subheader("Take Attendance")  
    l,r = st.columns([2,1],vertical_alignment="bottom") 
    with l:
        selected_subject_label = st.selectbox("select subject", options=list(subject_option.keys()))
        # print("selected_subject_label",selected_subject_label)
        
    with r:
        if st.button("Add Photos", width="stretch",type="primary" , icon=":material/photo_library:", ):
            add_photos_dialog()
    
    selected_subject = subject_option[selected_subject_label]
    # st.divider()
    if st.session_state.attendance_images:
        st.header("Added Photos")
        gal_cols = st.columns(4, vertical_alignment="bottom")
        
        for idx, img in enumerate(st.session_state.attendance_images):
            with gal_cols[idx % 4]:
                st.image(img, width="stretch", caption=f"photo {idx+1}")
    
    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        is_disable = bool(st.session_state.attendance_images)
        if st.button("Clear All Photos",type="primary", width="stretch", icon=":material/delete:",disabled=not is_disable):
            st.session_state.attendance_images = []
            st.rerun()
    
    with c2:
        is_disable = bool(st.session_state.attendance_images)
        if st.button("Run Face Analysis",type="primary", width="stretch", icon=":material/analytics:", disabled=not is_disable):
            with st.spinner("Scanning your classroom photos..."):
                all_detected_id = {}
                class_data = create_class(selected_subject) 
                for idx,img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert("RGB"))
                    detected,_,_ = predict_attendance(img_np)
                    
                    if detected:
                        for sid in detected:
                            student_id = int(sid)
                            
                            all_detected_id.setdefault(student_id, []).append(f"Photo {idx+1}")
                    
                        
                    enroll_student = get_enrolled_student(selected_subject)
                    if not enroll_student:
                        st.warning("No student Enrolled in your subject")
                        delete_class(class_data[0]["id"])
                    else:
                        result, attendance_log = [],[]
                        
                        current_date_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S") 
                                              
                        for record in enroll_student:
                            student = record["students"]
                            source = all_detected_id.get(int(student["student_id"]),[])
                            is_present = len(source) > 0
                            result.append({
                                "Name": student["name"],
                                "ID": student["student_id"],
                                "source": ", ".join(source) if is_present else "-",
                                "status": "✅ Present" if is_present else "❌ Absent"
                            })
                            
                            attendance_log.append({
                                "subject_id": selected_subject,
                                "student_id": student["student_id"],
                                "timestamp": current_date_time,
                                "is_present": is_present, 
                                "class_id": class_data[0]["id"]
                            })
                attendance_result_dialog(pd.DataFrame(result),attendance_log )
    
    with c3:
        if st.button("Voice Attendance",type="primary", width="stretch", icon=":material/mic:"):
            dialog_voice_attendance(selected_subject)
    
    if st.session_state.get("voice_attendance_result"):
        df_result, attendance_log = st.session_state["voice_attendance_result"]
        attendance_result_dialog(df_result,attendance_log)