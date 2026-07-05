import streamlit as st

def style_base_layout():
    st.markdown(
        """
        <style>
           @import url('https://fonts.googleapis.com/css2?family=Saira:ital,wght@0,100..900;1,100..900&display=swap');
           @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&family=Saira:ital,wght@0,100..900;1,100..900&display=swap');
           @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&family=Saira:ital,wght@0,100..900;1,100..900&display=swap');
           
            /* Hide top bar in streamlit */
            MainMenu, footer, header{
                visibility: hidden;
            }
            
            .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem !important;
            }
            
            h1,h2 {
                font-family: "Saira", sans-serif !important;
                font-weight: 700 !important;
                font-size: 2.5rem !important;
                line-height: 1.1 !important;
                margin-bottom: 0rem !important;
            }
            
            h3, p {
                font-family: "Outfit", sans-serif !important;
                font-weight: 400 !important;
                font-size: 1rem !important;
                line-height: 1.5 !important;
            }
            
            button[kind="primary"] {
                border-radius: 1.5rem !important;
                background-color: #5865F2 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.3s ease-in-out !important;
            }
            
            button[kind="secondary"] {
                border-radius: 1.5rem !important;
                background-color: #EB459E !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.3s ease-in-out !important;
            }
            
            button[kind="tertiary"] {
                border-radius: 1.5rem !important;
                background-color: black !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.3s ease-in-out !important;
            }
            
            button:hover {
                transform: scale(1.05) !important;
                }
        </style>
        """, unsafe_allow_html=True)

def style_background_dashboard():
    st.markdown(
        """
        <style>
            /* Set the background color of the entire page */
            .stApp {
                background-color: #5865F2!important;
            }

            .stApp div[data-testid="stColumn"] {
                background-color: #e0e3ff  !important;    
                padding: 2.5rem !important;
                border-radius: 5rem !important;
                
            }
        </style>
        """, unsafe_allow_html=True)

def style_background_home():
    st.markdown(
        """
        <style>
            /* Set the background color of the entire page */
            .stApp {
                background-color: #E0E3FF!important;
            }

          
        </style>
        """, unsafe_allow_html=True)