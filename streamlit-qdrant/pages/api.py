import os

import pandas as pd
import requests
import streamlit as st

from utils import get_json_formats_select_box

st.write("# API Interface")

saved_queries = "./pages/saved_queries/"
examples = os.listdir(saved_queries)
examples_clean = [example.replace(".json", "") for example in examples]
selected_query = st.selectbox("Examples", examples_clean)

json_formats = ["split", "records", "index", "columns", "values", "table"]
selected_json_format = get_json_formats_select_box()

url = f"http://127.0.0.1:8004/query/{selected_query}/{selected_json_format}"

code = f"""
url = '{url}'
response = requests.get(url).json()
"""
st.code(code, language="python")

if st.button("Hit API"):
    response = requests.get(url).json()
    st.json(response)
