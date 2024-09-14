import streamlit as st
from streamlit_extras.colored_header import colored_header
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
import numpy as np

def app():
    colored_header(
        label='Welcome to Data :red[Prediction] page 👋🏼',
        color_name='red-70',
        description='CarDekho Used Cars Price Prediction'
    )

    @st.cache_data
    def load_data():
        df = pd.read_csv('Cleaned_Car_Dheko.csv')
        df1 = pd.read_csv('Preprocessed_Car_Dheko.csv')
        return df, df1

    df, df1 = load_data()

    # Create LabelEncoders for categorical variables
    le_model = LabelEncoder()
    le_model.fit(df['Car_Model'])
    
    le_brand = LabelEncoder()
    le_brand.fit(df['Manufactured_By'])
    
    le_fuel = LabelEncoder()
    le_fuel.fit(df['Fuel_Type'])

    le_location = LabelEncoder()
    le_location.fit(df['Location'])

    # Function to encode categorical variables
    def encode_categorical(value, encoder):
        try:
            return encoder.transform([value])[0]
        except ValueError:
            return -1  # Default value for unseen categories

    # Load the model
    @st.cache_resource
    def load_model():
        with open('GradientBoost_model.pkl', 'rb') as file:
            return pickle.load(file)

    model = load_model()

    # Create the form
    with st.form(key='prediction_form'):
        car_brand = st.selectbox("Select Car Brand", options=df['Manufactured_By'].unique())
        car_model = st.selectbox("Select Car Model", options=df[df['Manufactured_By'] == car_brand]['Car_Model'].unique())
        model_year = st.selectbox("Select Car Produced Year", options=df['Car_Produced_Year'].unique())
        transmission = st.radio("Select Transmission Type", options=df['Transmission_Type'].unique(), horizontal=True)
        location = st.selectbox("Select Location", options=df['Location'].unique())
        km_driven = st.number_input(f"Enter Kilometer Driven (Min: {df['Kilometers_Driven'].min()}, Max: {df['Kilometers_Driven'].max()})")
        engine_cc = st.number_input(f"Enter Engine CC (Min: {df['Engine_CC'].min()}, Max: {df['Engine_CC'].max()})")
        mileage = st.number_input(f"Enter Mileage (Min: {df['Mileage(kmpl)'].min()}, Max: {df['Mileage(kmpl)'].max()})")
        
        fuel_type = st.selectbox("Select Fuel Type", options=df['Fuel_Type'].unique())
        no_of_owners = st.number_input("Enter Number of Previous Owners", min_value=1, max_value=5, value=1)
        no_of_seats = st.number_input("Enter Number of Seats", min_value=2, max_value=10, value=5)

        submit_button = st.form_submit_button('Predict')

    if submit_button:
        # Prepare input data
        car_model_encoded = encode_categorical(car_model, le_model)
        car_brand_encoded = encode_categorical(car_brand, le_brand)
        transmission_encoded = 0 if transmission == "Automatic" else 1
        location_encoded = encode_categorical(location, le_location)
        fuel_type_encoded = encode_categorical(fuel_type, le_fuel)

        def inv_trans(x):
            return 1/x if x != 0 else 0

        input_data = [
            inv_trans(km_driven),
            transmission_encoded,
            car_model_encoded,
            model_year,
            engine_cc,
            mileage,
            location_encoded,
            fuel_type_encoded,
            no_of_owners,
            car_brand_encoded,
            no_of_seats
        ]

        # Make prediction
        result = model.predict([input_data])
        
        # Calculate feature importances
        feature_importances = model.feature_importances_
        feature_names = ['Inv_Kilometers_Driven', 'Transmission_Type', 'Car_Model', 'Car_Produced_Year', 
                         'Engine_CC', 'Mileage(kmpl)', 'Location', 'Fuel_Type', 'No_of_Owners', 
                         'Manufactured_By', 'No_of_Seats']
        
        # Create a DataFrame of feature importances
        importance_df = pd.DataFrame({'feature': feature_names, 'importance': feature_importances})
        importance_df = importance_df.sort_values('importance', ascending=False)

        # Display prediction and feature importances
        st.markdown(f"## :green[*Predicted Car Price is {result[0]:,.2f}*]")
        st.markdown("## Feature Importances")
        st.bar_chart(importance_df.set_index('feature'))

        # Display how each feature contributed to the prediction
        st.markdown("## Feature Contributions to Prediction")
        contributions = np.array(input_data) * feature_importances
        contribution_df = pd.DataFrame({'feature': feature_names, 'contribution': contributions})
        contribution_df = contribution_df.sort_values('contribution', ascending=False)
        st.bar_chart(contribution_df.set_index('feature'))

        # Explain the prediction
        st.markdown("## Explanation of Prediction")
        for feature, contribution in zip(contribution_df['feature'], contribution_df['contribution']):
            if contribution > 0:
                st.write(f"- The {feature} increased the predicted price by {contribution:.2f}")
            else:
                st.write(f"- The {feature} decreased the predicted price by {abs(contribution):.2f}")