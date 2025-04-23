import streamlit as st
import pandas as pd
import os

CSV_PATH = "Nepal_Service_Network.csv"

st.title("Search Your Posts")
search = st.text_input("Search", placeholder="Search your posts here", key="search")
button = st.button("Search")


if os.path.exists('Nepal_Service_Network.csv'):
    df = pd.read_csv('Nepal_Service_Network.csv')
    
    if search and button:
        mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        filtered_df = df[mask]
        st.subheader("Search Results")
        st.dataframe(filtered_df)
    else:
        st.subheader("All Data")
        st.dataframe(df)
else:
    st.error(f"CSV file not found at {'Nepal_Service_Network.csv'}")  # corrected file name
