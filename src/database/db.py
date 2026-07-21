from src.database.config import supabase

import bcrypt

def hash_pass(text):
    return bcrypt.hashpw(text.encode(), bcrypt.gensalt()).decode()

def check_pass(ep,op):
    return bcrypt.checkpw(ep.encode(), op.encode())

def check_teacher_exist(username):
    res = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(res.data) > 0

def create_teacher(username, name, password):
    data = {"username": username, "name":name, "password": hash_pass(password)}
    res = supabase.table("teachers").insert(data).execute()
    return res.data
    
def teacher_login(username, password):
    res = supabase.table("teachers").select("*").eq("username", username).execute()
    
    if res.data:
        teacher = res.data[0]
        if check_pass(password, teacher["password"]):
            return teacher

def get_all_students():
    res = supabase.table("students").select("*").execute()
    
    return res.data

def get_my_subjects(teacher_id):
    res = supabase.table("subjects").select("*, subject_student(count), attendance_log(timestamp)").eq("teacher_id",teacher_id).execute()

    subjects = res.data
    
    for sub in subjects:
        sub['total_students'] = sub.get("subject_student", [{}])[0].get("count", 0) if sub.get("subject_student") else 0
        attendance =  sub.get("attendance_log", [])
        unique_session = len(set(lg["timestamp"] for lg in attendance))
        sub["total_classes"] = unique_session
        
        sub.pop("subject_student", None)
        sub.pop("attendance_log", None)
    
    
    return subjects

def get_student_by_id(id):
    res = supabase.table("students").select("*").eq("student_id",id).execute()
    # print("res--->",res.data)
    return res.data

def get_subject_by_code(s_code):
    res = supabase.table("subjects").select("*").eq("subject_code",s_code).execute()
    return res.data

def get_subject_student(subject_id,student_id):
    res = supabase.table("subject_student").select("*").eq("subject_id",subject_id).eq("student_id",student_id).execute()
    return res.data

def get_my_enrolled_courses(student_id):
    res = supabase.table("subject_student").select("*, subjects(*,attendance_log(*))").eq("student_id",student_id).eq("subjects.attendance_log.student_id", student_id).execute()
    return res.data

def get_enrolled_student(subject_id):
    res = supabase.table("subject_student").select("*, students(*)").eq("subject_id",subject_id).execute()
    return res.data

def create_student(name, face_embedding,voice_embedding=None):
    data = {"face_embedding": face_embedding, "name":name, "voice_embedding": voice_embedding}
    res = supabase.table("students").insert(data).execute()
    return res.data

def create_subject(name, subject_code,section, teacher_id):
    data = {"name": name, "subject_code":subject_code, "section": section, "teacher_id":teacher_id}
    res = supabase.table("subjects").insert(data).execute()
    return res.data

def enroll_student_to_subject(subject_id,student_id):
    data = {"subject_id": subject_id, "student_id":student_id,}
    res = supabase.table("subject_student").insert(data).execute()
    return res.data

def create_class(subject_id):
    data = {"subject_id": subject_id, }
    res = supabase.table("class").insert(data).execute()
    return res.data

def create_attendance_log(logs):
    res = supabase.table("attendance_log").insert(logs).execute()
    return res.data


def remove_my_enrolled_courses(subject_id, student_id):
    res = supabase.table("subject_student").delete().eq("student_id",student_id).eq("subject_id", subject_id).execute()
    return res.data

def remove_my_enrolled_courses_attendance(subject_id, student_id):
    res = supabase.table("attendance_log").delete().eq("student_id",student_id).eq("subject_id", subject_id).execute()
    return res.data

def delete_class(id):
    res = supabase.table("class").delete().eq("id",id).execute()
    return res.data

def get_attendance_for_teacher(teacher_id):
    res =  supabase.table("class").select("*, subjects!inner(*), attendance_log(*)").eq("subjects.teacher_id", teacher_id).execute()
    return res.data