import streamlit as st
import streamlit as st
import pandas as pd
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
import plotly.express as px

def app():
    colored_header(
    label = 'You are in Data :green[Analysis] page',
    color_name = 'green-70',
    description = ''
)
    @st.cache_data
    def dataframe():
        df = pd.read_csv('Cleaned_Car_Dheko.csv')
        return df
    df = dataframe()


    choice = st.selectbox("**Select an option to Explore their data**", (df.drop('Car_Price',axis = 1).columns))  
    
    st.markdown(f"## :rainbow[Car Price vs {choice}]")
    hist = px.histogram(df, x = choice, y = 'Car_Price',width = 950, height=500)
    st.plotly_chart(hist)

    st.markdown(f"## :rainbow[Which Car Brand is highly available]")
    brand = df.groupby('Manufactured_By').count().reset_index()[['Manufactured_By','Fuel_Type']]
    bar = px.bar(brand, x = 'Manufactured_By', y = 'Fuel_Type',width = 950, height=500, labels={'Fuel_Type':'Total Count of Car Brand'})
    st.plotly_chart(bar)

    st.markdown(f"## :rainbow[Which Car Model available in highest prices]")
    model = df[['Car_Model','Car_Price','Manufactured_By','Car_Produced_Year','Kilometers_Driven','No_of_Owners']].sort_values('Car_Price',ascending=False).head(60)
    data = model[model['Manufactured_By'].isin(['Maruti','Chevrolet','Hyundai','Honda','Tata'])]
    model.drop(data.index, inplace = True)
    bar = px.bar(model, x = 'Car_Model', y = 'Car_Price',width = 1000, height=500,color = 'Car_Price' ,color_continuous_scale='hot',hover_name='Manufactured_By',hover_data=['Car_Produced_Year','Kilometers_Driven','No_of_Owners'])
    st.plotly_chart(bar)
    # st.dataframe(model)

    st.markdown(f"## :rainbow[Which Car Model available in lowest prices]")
    model = df[['Car_Model','Car_Price','Manufactured_By','Car_Produced_Year','Kilometers_Driven','No_of_Owners']].sort_values('Car_Price',ascending=True).head(60)
    data = model[model['Manufactured_By'].isin(['BMW','Land Rover','Mercedes-Benz'])]
    model.drop(data.index, inplace = True)
    bar = px.bar(model, x = 'Car_Model', y = 'Car_Price',width = 1000, height=500,color = 'Car_Price' ,color_continuous_scale='turbo',hover_name='Manufactured_By',hover_data=['Car_Produced_Year','Kilometers_Driven','No_of_Owners'])
    st.plotly_chart(bar)
    # st.dataframe(model)


    col,col1 = st.columns([2,2])
    with col:
        select_brand = st.selectbox("**Select a Car Brand**", (df['Manufactured_By'].unique()))
        brand = df[df['Manufactured_By']==select_brand]
    with col1:
        select_model = st.selectbox('**Select a Car Model**', options = brand['Car_Model'].unique())
        
    model = brand.groupby(['Car_Model','Car_Produced_Year'])['Car_Price'].mean().reset_index()
    specific_model = model[model['Car_Model']==select_model]
    # st.dataframe(specific_model)
    st.markdown(f"## :rainbow[Car model year vs Prices]")
    bar = px.bar(specific_model, x = 'Car_Produced_Year', y = 'Car_Price',width = 950, height=500,color='Car_Price',color_continuous_scale='rainbow', hover_name='Car_Model')
    st.plotly_chart(bar)
    
    st.markdown(f"## :rainbow[Knowing about the Kilometre driven and their Car Prices]")
    scatter = px.scatter(brand, x = 'Kilometers_Driven', y = 'Car_Price', color = 'Car_Model',size = 'Car_Price',hover_name = 'Manufactured_By', hover_data = ['Car_Model','Fuel_Type','Car_Produced_Year','Transmission_Type','Mileage(kmpl)','No_of_Seats','Engine_CC'],width=1000,height=500)
    st.plotly_chart(scatter)

    st.markdown(f"## :rainbow[Knowing about the Car Mileage and their Car Prices]")
    scatter = px.scatter(brand, x = 'Mileage(kmpl)', y = 'Car_Price', color = 'Car_Model',size = 'Car_Price',hover_name = 'Manufactured_By', hover_data = ['Car_Model','Fuel_Type','Car_Produced_Year','Transmission_Type','Kilometers_Driven','No_of_Seats','Engine_CC'],width=1000,height=500)
    st.plotly_chart(scatter)

    st.markdown(f"## :rainbow[Car Age vs Car Prices]")
    scatter = px.scatter(brand, x = 'Car_Age', y = 'Car_Price', color = 'Car_Model',size = 'Car_Price',hover_name = 'Manufactured_By', hover_data = ['Car_Model','Fuel_Type','Car_Produced_Year','Transmission_Type','Kilometers_Driven','Mileage(kmpl)','No_of_Seats','Engine_CC'],width=1000,height=500)
    st.plotly_chart(scatter)

    col,col1 = st.columns([2,2])
    with col:
        radio = st.radio('**Select any Location 📍**', options = df['Location'].unique(), horizontal = True)
    with col1:
        select_CT = st.selectbox('**Select any Central Tendency**', options = ['mean','median','mode'])
    location_brand = df[(df['Manufactured_By'] == select_brand) & (df['Location'] == radio)]

    if select_CT == 'mean':
        result = location_brand.groupby(['Manufactured_By','Car_Model'])['Car_Price'].mean().reset_index()
    elif select_CT == 'median':
        result = location_brand.groupby(['Manufactured_By','Car_Model'])['Car_Price'].median().reset_index()
    elif select_CT == 'mode':
        result = location_brand.groupby(['Manufactured_By','Car_Model'])['Car_Price'].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else None).reset_index()
    # st.dataframe(result)
    st.markdown(f"## :rainbow[What are the cars available in specific location, brand and their {select_CT} Price values]")
    pie = px.pie(result, names = 'Car_Model', values = 'Car_Price',width=900,height=500,hover_name='Manufactured_By',hole=0.3)
    st.plotly_chart(pie)

    