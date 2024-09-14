import streamlit as st
from streamlit_option_menu import option_menu
import Home, Filtering, Analysis, Predict
from PIL import Image
from streamlit_extras.dataframe_explorer import dataframe_explorer

img = Image.open("C:\\Users\\ukudh\\OneDrive\\Desktop\\MDTE11\\Project\CarDheko\\CarDekho.jpg")
st.set_page_config(page_title = "Cardekho Resale Price Prediction", page_icon = img,layout = "wide")

class multiapp:
    def __init__(self):
        self.apps = []
    def add_app(self, title, function):
        self.apps.append({'title':title,'function':function})
    def run(self):
        with st.sidebar:
            app = option_menu('Car Resale Price Prediction', ["Home","Data Filtering","Data Analysis","Data Prediction"], 
                icons=['house', 'search',"reception-4","dice-5-fill"], 
                menu_icon='cash-coin', default_index=0, orientation="vertical",
                styles={
                    "container": {"padding": "0!important", "background-color": "#A95C68"}, # #008080
                    "icon": {"color": "violet", "font-size": "20px"}, 
                    "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#C4A484"},
                    "nav-link-selected": {"background-color": "#C04000"}, 
                }
            )
        if app == 'Home':
            Home.app()
        elif app == 'Data Filtering':
            Filtering.app()
        elif app == 'Data Analysis':
            Analysis.app()
        elif app == 'Data Prediction':
            Predict.app()
        
    
        # Add submit button to the form
        #submitted = st.form_submit_button("Submit")
        #if submitted:
            #lst.success(f"Form submitted for {app}!")
                # Add any additional logic here for form submission    
        
    
        
app = multiapp()

# Add your apps to the multiapp instance
app.add_app("Home", Home.app)
app.add_app("Data Filtering", Filtering.app)
app.add_app("Data Analysis", Analysis.app)
app.add_app("Data Prediction", Predict.app)

# Run the multiapp
app.run()




