import streamlit as st
from utils import sql_to_df, create_connection
import requests


queries_conn = create_connection('queries.db')
queries_df = sql_to_df(queries_conn, 'select * from queries')
selected_query = st.selectbox('Query to Execute', list(queries_df['query_name']))

json_formats = ['split', 'records', 'index', 'columns', 'values', 'table']
selected_json_format = st.selectbox('Json Format', json_formats)

url = f'http://127.0.0.1:8001/query/{selected_query}?json_format={selected_json_format}'

code = f"""
url = '{url}'
response = requests.get(url).json()
"""
st.code(code, language="python")

if st.button('Hit API'):
    response = requests.get(url).json()
    st.json(response)