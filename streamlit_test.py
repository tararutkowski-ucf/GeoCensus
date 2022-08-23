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
 
def closest(stores, house, number):
    min_distance1 = 556200
    close_store1 = "NaN"
    min_distance2 = 556300
    close_store2 = "NaN"
    min_distance3 = 556400
    close_store3 = "NaN"
    min_distance4 = 556500
    close_store4 = "NaN"
    min_distance5 = 556600
    close_store5 = "NaN"
    min_distance6 = 556300
    close_store6 = "NaN"
    min_distance7 = 556400
    close_store7 = "NaN"
    min_distance8 = 556500
    close_store8 = "NaN"
    min_distance9 = 556600
    close_store9 = "NaN"
    min_distance10 = 556700
    close_store10 = "NaN"
    for index, store in stores.iterrows():
        distance = haversine(house['Lat'],house['Lon'],store['Lat'],store['Lon'])
        if (distance < min_distance1): #& (distance > 0):
            min_distance1 = distance
            close_store1 = store
        elif (distance < min_distance2) and (number < 1):
            min_distance2 = distance
            close_store2 = store
        elif (distance < min_distance3) and (number < 2):
            min_distance3 = distance
            close_store3 = store
        elif (distance < min_distance4)  and (number < 3):
            min_distance4 = distance
            close_store4 = store
        elif (distance < min_distance5) and (number < 4):
            min_distance5 = distance
            close_store5 = store
        elif (distance < min_distance6) and (number < 5):
            min_distance6 = distance
            close_store6 = store
        elif (distance < min_distance7) and (number < 6):
            min_distance7 = distance
            close_store7 = store
        elif (distance < min_distance8) and (number < 7):
            min_distance8 = distance
            close_store8 = store
        elif (distance < min_distance9) and (number < 8):
            min_distance9 = distance
            close_store9 = store
        elif (distance < min_distance10) and (number < 9):
            min_distance10 = distance
            close_store10 = store
        else:
            continue

    close_store1["Distance"] = min_distance1
    close_store2["Distance"] = min_distance2
    close_store3["Distance"] = min_distance3
    close_store4["Distance"] = min_distance4
    close_store5["Distance"] = min_distance5
    close_store6["Distance"] = min_distance6
    close_store7["Distance"] = min_distance7
    close_store8["Distance"] = min_distance8
    close_store9["Distance"] = min_distance9
    close_store10["Distance"] = min_distance10
    return close_store1, close_store2, close_store3, close_store4, close_store5, close_store6, close_store7, close_store8, close_store9, close_store10
    #return close_store2


@st.cache
def test_fn(stores, house, number):
    test= closest(stores, house, number)
    #test = test.add_prefix('store_')
    return test[number]

@st.cache
def run_algo(df, store, max_i):
    for i in range(0,max_i):
        appiled_df = df.apply(lambda row: test_fn(store, row, i), axis='columns', result_type='expand')
        df = pd.concat([df, appiled_df], axis='columns')
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

st.text('Please input a number from 1 to 10 specifying how many "Stores" you would like to return for each "House"')
number = st.number_input(label = 'Enter a number 1-10', min_value=1, max_value=10)

if st.button('Run Algorithm'):
    if house is not None:
        if store is not None:
            data_load_state = st.text('Loading data...')
            data = run_algo(house_df, store_df, number)
            data_load_state.text("Done!")
            #st.write(data)
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



