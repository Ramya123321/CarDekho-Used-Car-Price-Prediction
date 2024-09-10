import streamlit as st
from streamlit_extras.colored_header import colored_header

def app():
    # st.write('dfdsff')
    colored_header(
    label = 'Welcome to :orange[Home] Page 👋🏼',
    color_name = 'orange-70',
    description = '',
)
    with st.form(key = 'form',clear_on_submit=False):

        st.markdown("## :orange[*Project title*:]")
        st.subheader("&nbsp; &nbsp; &nbsp; &nbsp; *CarDekho Used Car Price Prediction*")
        st.markdown("## :orange[*Skills take away From This Project*:]")
        st.subheader("&nbsp; &nbsp; &nbsp; &nbsp; *Python scripting, Data Wrangling, EDA, Machine Learning, Streamlit.*")
        st.markdown("## :orange[*Domain*:]")
        st.subheader("&nbsp; &nbsp; &nbsp; &nbsp; *Automobile*")
        st.markdown("## :orange[*Problem Statement:*]")
        st.subheader("&nbsp; &nbsp; &nbsp; &nbsp; *The primary objective of is project is to create a data science solution for predicting used car prices accurately by analyzing a diverse dataset including car model, no. of owners, age, mileage, fuel type, kilometers driven, features and location. The aim is to build a machine learning model that offers users to find current valuations for used cars.*")
        st.markdown("## :orange[*Results:*]")
        st.subheader("&nbsp; &nbsp; &nbsp; &nbsp; *The culmination of this project will be a robust and user-friendly data science solution that leverages advanced machine learning techniques to predict used car prices with a high degree of accuracy. The end result will empower users to make informed decisions when buying or selling used cars, enhancing their overall experience in the automotive market.*")
        # st.markdown("## :orange[*Dataset:*]")
        button = st.form_submit_button('**Click here to get Data Set Link**',use_container_width = True)
        if button:
            url = "https://drive.google.com/drive/folders/16U7OH7URsCW0rf91cwyDqEgd9UoeZAJh"
            st.markdown("## :orange[Dataset : [Data Link](%s)]"% url)