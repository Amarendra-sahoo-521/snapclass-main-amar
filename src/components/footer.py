import streamlit as st

def footer_home():
    # st.image(logo_path, width=100 )
    
    st.markdown(""" 
                <div style="display: flex;  align-items: center; justify-content: center; height: 100px; margin:0px auto;">
                    <p style="color: #333; font-size: 16px; margin: 0;">&copy; 2026 SnapClass. All rights reserved.</p>
                </div>
                """, unsafe_allow_html=True)
    