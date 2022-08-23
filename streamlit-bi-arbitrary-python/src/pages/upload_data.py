import streamlit as st
from utils import create_connection
import pandas as pd
import os

st.markdown("# Upload Data")
# https://discuss.streamlit.io/t/uploading-csv-and-excel-files/10866/2
table_name = st.text_input("Table Name to Insert")
conn = create_connection("core.db")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # read csv
    try:
        df = pd.read_csv(uploaded_file)
        df.to_sql(name=table_name, con=conn)
        st.write("Data uploaded successfully. These are the first 5 rows.")
        st.dataframe(df.head(5))

    except Exception as e:
        st.write(e)
