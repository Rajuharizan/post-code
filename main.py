import streamlit as st
import pandas as pd
import os

CSV_PATH = "Nepal_Service_Network.csv"

# Security configurations
st.set_page_config(layout="centered")

# Disable download and copy options
st.markdown("""
<style>
    .stDownloadButton, .stDataFrame div[data-testid="stElementToolbar"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Main app
st.write("This app is built by OnlyRj")
st.title("Search Your Posts or zip code")
st.write("Only Nepal's postcode and zip code are available.")

search = st.text_input("Search", placeholder="Search your posts here", key="search")
button = st.button("Search")

if os.path.exists(CSV_PATH):
    @st.cache_data  # Cache for performance
    def load_data():
        return pd.read_csv(CSV_PATH)
    
    df = load_data()
    
    if search and button:
        mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        filtered_df = df[mask]
        st.subheader("Search Results")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    else:
        st.subheader("All Data")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
    # Block right-click and text selection
    st.markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        document.addEventListener('contextmenu', event => event.preventDefault());
        document.styleSheets[0].insertRule('body { user-select: none !important; }', 0);
    });
    </script>
    """, unsafe_allow_html=True)
    
else:
    st.error(f"Data file not found at {CSV_PATH}")