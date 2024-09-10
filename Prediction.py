import streamlit as st
from streamlit_extras.let_it_rain import rain
from streamlit_extras.colored_header import colored_header
import pandas as pd
import pickle

def app():
    colored_header(
    label = 'Welcome to Data :red[Prediction] page 👋🏼',
    color_name = 'red-70',
    description = 'CarDekho Used Cars Price Prediction'
)

    @st.cache_data
    def data():
        df = pd.read_csv('Cleaned_Car_Dheko.csv')
        df1 = pd.read_csv('Preprocessed_Car_Dheko.csv')
        return df,df1
    df,df1 = data()

    df.drop(['Manufactured_By','No_of_Seats','No_of_Owners','Fuel_Type','Registration_Year','Car_Age'], axis = 1, inplace = True)
    df1.drop(['Manufactured_By','No_of_Seats','No_of_Owners','Fuel_Type','Registration_Year','Car_Age'], axis = 1, inplace = True)

    for i in df.columns:
        if (df[i].dtype == 'object'):
            col_name = i
            decode = df[i].sort_values().unique() # status
            encode = df1[i].sort_values().unique() # 0,1,2
            globals()[col_name] = {}
            globals()[i] = dict(zip(decode, encode))



    # st.dataframe(df1.head())

    with st.form(key = 'form',clear_on_submit=False):
        
        car_model = st.selectbox(
                "**Select a Car Model**",
                options = df['Car_Model'].unique(),
            )
        
        model_year = st.selectbox(
                "**Select a Car Produced Year**",
                options = df['Car_Produced_Year'].unique(),
            )
        
        transmission = st.radio(
                "**Select a Transmission Type**",
                options = df['Transmission_Type'].unique(),
                horizontal = True
            )

        location = st.selectbox(
                "**Select a location**",
                options = df['Location'].unique(),
            )

        km_driven = st.number_input(
                f"**Enter a Kilometer Driven in range of (Minimum : {df['Kilometers_Driven'].min()} & Maximum : {df['Kilometers_Driven'].max()})**",
               
            )

        engine_cc = st.number_input(
                f"**Enter an Engine CC in range of (Minimum : {df['Engine_CC'].min()} & Maximum : {df['Engine_CC'].max()})**",
              
            )

        mileage = st.number_input(
                f"**Enter a Mileage (Minimum : {df['Mileage(kmpl)'].min()} & Maximum : {df['Mileage(kmpl)'].max()})**",
              
            )

        def inv_trans(x):
            if x == 0:
                return x
            else:
                return 1/x
        inv_trans(km_driven)

        with open('GradientBoost_model.pkl', 'rb') as file:
            model = pickle.load(file)
        

        button = st.form_submit_button('**Predict**',use_container_width = True)

        if button == True:
            result = model.predict([[inv_trans(km_driven), "Transmission_Type"[transmission], "Car_Model"[car_model], model_year, engine_cc, mileage, "Location"[location]]])
            st.markdown(f"## :green[*Predicted Car Price is {result[0]}*]")