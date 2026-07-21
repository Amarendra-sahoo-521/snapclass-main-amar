import streamlit as st
import segno
import io
from datetime import datetime
import pandas as pd

from src.database.db import get_enrolled_student,create_class 
from src.pipelines.voice_pipeline import process_bulk_audio


@st.dialog("Voice Attendance")
def dialog_voice_attendance(selected_subject):
    st.write("Record audio of students saying I am present, Then AI will recognize the student")
    
    audio_data = None
    
    audio_data = st.audio_input("Record classroom audio")
    
    if st.button("Analyze the audio", width="stretch", type="primary"):
        class_data = create_class(selected_subject) 
        with st.spinner("analyzing the audio"):
            enroll_student = get_enrolled_student(selected_subject)
            if not enroll_student:
                st.warning("No student Enrolled in your subject")
                return
            candidate_dist = {
                s["students"]["student_id"]:s["students"]["voice_embedding"]
                for s in  enroll_student if s["students"].get("voice_embedding")
            }
            if not candidate_dist:
                st.error("No student have voice profile registered")
                return

            audio_bytes = audio_data.read()
            
            detected_scores = process_bulk_audio(audio_bytes,candidate_dist)
            
            result, attendance_log = [],[]
                        
            current_date_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S") 
                                    
            for record in enroll_student:
                student = record["students"]
                scores = detected_scores.get(int(student["student_id"]),0.0)
                is_present = bool(scores > 0)
                result.append({
                    "Name": student["name"],
                    "ID": student["student_id"],
                    "source": ", ".join(scores) if is_present else "-",
                    "status": "✅ Present" if is_present else "❌ Absent"
                })
                
                attendance_log.append({
                    "subject_id": selected_subject,
                    "student_id": student["student_id"],
                    "timestamp": current_date_time,
                    "is_present": is_present,
                    "class_id": class_data[0]["id"] 
                })
            st.session_state["voice_attendance_result"] = (pd.DataFrame(result),attendance_log)
        st.rerun()
    
    
            
            
    
    