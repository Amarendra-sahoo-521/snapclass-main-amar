import streamlit as st

from src.components.footer import footer_home
from src.components.header import header_home
from ui.base_layout import style_background_home, style_base_layout



def home_screen():
    style_base_layout()
    style_background_home()
    header_home()

    col1, col2 = st.columns(2,gap="small")
    with col1:
        container = st.container(border=True)
        with container:
            st.header("I am a Student" )
            st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
            if st.button("Student portal", width="content", type="primary", icon=':material/arrow_outward:', icon_position='right' ):
                st.session_state['login_type'] = "student"
                st.rerun()
       

    with col2:
         container = st.container(border=True)
         with container:
            st.header("I am a Teacher" )
            st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=150,)
            if st.button("Teacher portal", width="content", type="primary", icon=':material/arrow_outward:', icon_position='right' ):
                st.session_state['login_type'] = "teacher"
                st.rerun()
           
    footer_home()
        
