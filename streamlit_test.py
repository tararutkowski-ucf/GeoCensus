# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 14:24:33 2022

@author: trutkowski
"""

import streamlit as st
import pandas as pd
import math

@st.cache
def haversine(lat1, lon1, lat2, lon2):
    R = 3959.87433
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2*math.asin(math.sqrt(a))

    return R * c

@st.cache
def closest(stores, house):
    min_distance1 = 556200
    close_store1 = "NaN"
    
    for index, store in stores.iterrows():
        distance = haversine(house['Lat'],house['Lon'],store['Lat'],store['Lon'])
        if (distance < min_distance1): #& (distance > 0):
            min_distance1 = distance
            close_store1 = store
        else:
            continue

    close_store1["Distance"] = min_distance1
    return close_store1

@st.cache
def test_fn(stores, house, number):
    test= closest(stores, house)
    test = test.add_prefix('store_')
    return test

@st.cache
def run_algo(df, store):
    i = 0
    appiled_df = df.apply(lambda row: test_fn(store, row, i), axis='columns', result_type='expand')
    df = df.add_prefix('house_')
    df = pd.concat([df, appiled_df], axis='columns')
    return df

@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')
 
st.title('Closest Locations to Batch Addresses')
st.write('Please upload two files, one representing your "Houses" and one representing your "Stores" ')
st.write('This program will find the closest "Store" to each "House" Address')
st.write('It is very important that you ensure your file has columns named "Lat" and "Lon" (Case sensitive)\n\n')

house = st.file_uploader("Choose a file to use as your houses")
if house is not None:
     # Can be used wherever a "file-like" object is accepted:
     house_df = pd.read_csv(house)
     st.write(house_df)
     try:
         test = house_df['Lat'] 
     except:
         st.markdown(""" <style> .font {font-size:20px ; font-family: 'Arial'; color: #FF0000;} </style> """, unsafe_allow_html=True)
         st.markdown('<p class="font">No column named Lat</p>', unsafe_allow_html=True)

     try:
         test = house_df['Lon'] 
     except:
         st.markdown(""" <style> .font {font-size:20px ; font-family: 'Arial'; color: #FF0000;} </style> """, unsafe_allow_html=True)
         st.markdown('<p class="font">No column named Lon</p>', unsafe_allow_html=True)

     
store = st.file_uploader("Choose a file to use as your stores")
if store is not None:
     # Can be used wherever a "file-like" object is accepted:
     store_df = pd.read_csv(store)
     st.write(store_df)
     
     try:
         test = store_df['Lat'] 
     except:
         st.markdown(""" <style> .font {font-size:20px ; font-family: 'Arial'; color: #FF0000;} </style> """, unsafe_allow_html=True)
         st.markdown('<p class="font">No column named Lat</p>', unsafe_allow_html=True)

     try:
         test = store_df['Lon'] 
     except:
         st.markdown(""" <style> .font {font-size:20px ; font-family: 'Arial'; color: #FF0000;} </style> """, unsafe_allow_html=True)
         st.markdown('<p class="font">No column named Lon</p>', unsafe_allow_html=True)

     
if st.button('Run Algorithm'):
    if house is not None:
        if store is not None:
            data_load_state = st.text('Loading data...')
            data = run_algo(house_df, store_df)
            data_load_state.text("Done!")
            st.write(data)
            csv = convert_df(data)
            st.download_button(
                 label="Download data as CSV",
                 data=csv,
                 file_name='GeocodingOutput.csv',
                 mime='text/csv',
             )
        else:
            st.write('Need to select Data for store')
    else:
        st.write('Need to select Data for house')



