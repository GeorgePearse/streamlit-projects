import streamlit as st
import plotly.express as px
from utils import create_connection, sql_to_df
import os
import pandas as pd

sqlite_dbs = [file for file in os.listdir('.') if file.endswith('.db')]
db_filename = st.selectbox('DB Filename', sqlite_dbs)
analysis_conn = create_connection(db_filename)
queries_conn = create_connection("queries.db")

query = sql_to_df(queries_conn, 'select * from queries')
cols = [column[0] for column in query.description]
queries_df = pd.DataFrame.from_records(
    data = query.fetchall(), 
    columns = cols
)
st.dataframe(queries_df)

query_to_delete = st.selectbox('Query to Delete', list(queries_df['query_name']))
queries_conn.execute(f'delete from queries where query_name = {query_to_delete}')
queries_conn.commit()