import streamlit as st

def header_home():
    logo_path = "https://i.ibb.co/YTYGn5qV/logo.png"
    # st.image(logo_path, width=100 )
    
    st.markdown(f""" 
                <div style="display: flex;  flex-direction: column; align-items: center; justify-content: center; height: 100px; margin:30px 10px 50px 10px;">
                    <img src="{logo_path}" alt="Logo" style="height: 100px; ">
                    <h1 style=" font-size: 32px; margin-left: 20px;">SnapClass</h1></div>
                """, unsafe_allow_html=True)
    
    
def header_dashboard():
    logo_path = "https://i.ibb.co/YTYGn5qV/logo.png"
    # st.image(logo_path, width=100 )
    
    st.markdown(f""" 
               <div style="display: flex;width: 100%; align-items:center;">
                    <img src="{logo_path}" alt="Logo" style="height: 80px; ">
                    <h1 style=" padding:0px; margin-left: 10px;">SnapClass</h1>
                    </div>
                """, unsafe_allow_html=True)
    