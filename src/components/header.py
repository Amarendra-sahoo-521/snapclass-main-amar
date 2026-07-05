import streamlit as st

def header_home():
    logo_path = "https://i.ibb.co/YTYGn5qV/logo.png"
    # st.image(logo_path, width=100 )
    
    st.markdown(f""" 
                <div style="display: flex;  flex-direction: column; align-items: center; justify-content: center; height: 100px; margin:30px 10px 50px 10px;">
                    <img src="{logo_path}" alt="Logo" style="height: 100px; ">
                    <h1 style="color: #333; font-size: 32px; margin-left: 20px;">SnapClass</h1></div>
                """, unsafe_allow_html=True)
    