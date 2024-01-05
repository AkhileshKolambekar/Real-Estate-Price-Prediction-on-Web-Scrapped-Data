import streamlit as st
import pickle

st.set_page_config(page_title='Real Estate Price Prediction',layout='centered')

model = pickle.load(open('model.pkl','rb'))

st.header("Real Estate Price Prediction :house:")

property_type = st.selectbox('Enter the property',('Flat','Apartment','Builder','Penthouse'),index = None,placeholder='Choose an option')
if property_type == 'Flat':
    prop = 1
elif property_type == 'Apartment':
    prop = 2
elif property_type == 'Builder':
    prop = 3
else:
    prop = 4
bhk = st.text_input('Enter BHK Specification')
floor = st.text_input("Enter the floor")
area = st.text_input("Enter the area of the property")

if st.button('Predict'):
    prediction = model.predict([[prop,bhk,floor,area]])
    st.write('Reasonable value of the property must be ',prediction[0])