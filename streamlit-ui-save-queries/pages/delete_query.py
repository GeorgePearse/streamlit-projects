import streamlit as st
import plotly.express as px
from utils import create_connection, sql_to_df, instantiate_queries_table
import os
import pandas as pd

analysis_conn = create_connection('core.db')
queries_conn = create_connection("queries.db")

instantiate_queries_table()
queries_df = sql_to_df(queries_conn, 'select * from queries')
st.dataframe(queries_df)
query_to_delete = st.selectbox('Query to Delete', list(queries_df['query_name']))

if st.button('Delete'):
    statement = f"delete from queries where query_name = '{query_to_delete}'"
    st.write(statement)
    queries_conn.execute(statement)
    queries_conn.commit()
    queries_df = sql_to_df(queries_conn, 'select * from queries')
    st.dataframe(queries_df)