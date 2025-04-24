import streamlit as st
import pandas as pd
import os
import base64
from io import BytesIO

CSV_PATH = "Nepal_Service_Network.csv"

# Security configurations
st.set_page_config(
    page_title="Secure Postcode Search",
    page_icon="🔒",
    layout="centered"
)

# Disable download options
def disable_download():
    st.markdown("""
    <style>
        .stDownloadButton, .stDataFrame div[data-testid="stElementToolbar"] {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

disable_download()

# Obfuscate data display
def obfuscate_dataframe(df):
    # Convert to string and apply basic obfuscation
    obfuscated = df.astype(str).apply(lambda x: x.str.replace(r'(?<=.{2}).', '•'))
    return obfuscated

# Main app
st.title("🔒 Search Your Posts")
st.write("Only Nepal's postcode and zip code are available.")

# Add authentication (basic example)
password = st.text_input("Enter access password:", type="password")
if password != "your_secure_password":  # Replace with secure password check
    st.error("Incorrect password. Access denied.")
    st.stop()

search = st.text_input("Search", placeholder="Search your posts here", key="search")
button = st.button("Search")

if os.path.exists(CSV_PATH):
    try:
        # Read and cache the data
        @st.cache_data(show_spinner=False)
        def load_data():
            return pd.read_csv(CSV_PATH)
        
        df = load_data()
        
        if search and button:
            mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
            filtered_df = df[mask]
            
            st.subheader("Search Results")
            # Display obfuscated data
            st.dataframe(obfuscate_dataframe(filtered_df), 
                         use_container_width=True,
                         hide_index=True)
            
            # Prevent right-click and text selection
            st.markdown("""
            <script>
            document.addEventListener('DOMContentLoaded', function() {
                document.addEventListener('contextmenu', event => event.preventDefault());
                document.styleSheets[0].insertRule('body { user-select: none !important; }', 0);
            });
            </script>
            """, unsafe_allow_html=True)
        else:
            st.subheader("All Data")
            st.dataframe(obfuscate_dataframe(df), 
                         use_container_width=True,
                         hide_index=True)
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
else:
    st.error(f"Data file not found at {CSV_PATH}")