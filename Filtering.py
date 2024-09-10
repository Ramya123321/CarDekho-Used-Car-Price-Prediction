import streamlit as st
import pandas as pd
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
#from  streamlit_pandas as sp

def app():

    colored_header(
    label = 'You are in Data :blue[Filtering] page',
    color_name = 'blue-70',
    description = ''
)
    @st.cache_data
    def data():
        df = pd.read_csv('Cleaned_Car_Dheko.csv')
        return df
    df = data()
    
    df['Car_Produced_Year'] = df['Car_Produced_Year'].astype('str')
    df['Registration_Year'] = df['Registration_Year'].astype('str')

    choice = st.sidebar.selectbox(label = '*Select a column to know unique values :*',options = ['Car_Model','Manufactured_By'],index=None)
    if choice == 'Car_Model':
        unique_Car_Model = df['Car_Model'].unique()
        unique_Car_Model_df = pd.DataFrame({'Car_Models': unique_Car_Model})
        st.sidebar.dataframe(unique_Car_Model_df,use_container_width = True)
    else:
        unique_Car_Manufacture = df['Car_Model'].unique()
        unique_Car_Manufacture_df = pd.DataFrame({'Car_Companies': unique_Car_Manufacture})
        st.sidebar.dataframe(unique_Car_Manufacture_df,use_container_width = True)


    filter = dataframe_explorer(df)
    button = st.button('**SUBMIT**',use_container_width = True)
    if button:
        st.dataframe(filter,use_container_width = True,hide_index=True)