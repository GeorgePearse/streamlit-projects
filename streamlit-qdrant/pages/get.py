import os

import requests
import streamlit as st

st.write("Check DB State")

vector_db_host = os.environ.get("VECTOR_DB_HOST", "http://192.168.54.124:6333")
request = st.text_input("request")
response = requests.get(f"{vector_db_host}/{request}").json()
st.json(response)
