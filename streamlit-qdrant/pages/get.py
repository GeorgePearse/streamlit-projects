import os
import streamlit as st
import requests

st.write("Check DB State")

# determining the values of the parameters
options = ["collections"]

vector_db_host = os.environ.get("VECTOR_DB_HOST", "http://192.168.54.124:6333")
request = st.text_input("request")
response = requests.get(f"{vector_db_host}/{request}").json()
st.json(response)
