import streamlit as st
import plotly.express as px
from utils import create_connection, sql_to_df, instantiate_queries_table
import os
import pandas as pd

st.write('# Delete Table')
analysis_conn = create_connection('core.db')

query = "SELECT name FROM sqlite_master WHERE type='table';"
df = sql_to_df(analysis_conn, query)
st.dataframe(df)
table_to_delete = st.selectbox('Table to Delete', list(df['name']))

if st.button('Delete'):
    statement = f"drop table '{table_to_delete}'"
    st.write(statement)
    analysis_conn.execute(statement)
    analysis_conn.commit()
    # results after
    analysis_df = sql_to_df(analysis_conn, query)
    st.dataframe(analysis_df)
