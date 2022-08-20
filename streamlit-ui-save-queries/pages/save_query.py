import streamlit as st 
from utils import create_connection
import pandas as pd
import os


st.markdown("# Run Query")
sqlite_dbs = [file for file in os.listdir('.') if file.endswith('.db')]
db_filename = st.selectbox('DB Filename', sqlite_dbs)

query_name = st.text_input('Query Name')
query_contents = st.text_area("SQL Query", height=100)

analysis_conn = create_connection(db_filename)
query_db_conn = create_connection('queries.db')

query = analysis_conn.execute(query_contents)
cols = [column[0] for column in query.description]
results_df= pd.DataFrame.from_records(
    data = query.fetchall(), 
    columns = cols
)
st.dataframe(results_df)

st.button('Save Query')

try:
    query_db_conn.execute("""
        create table queries (query_name varchar, query_contents varchar)
    """
    )
except Exception as e:
    st.write(e)

insert_response = query_db_conn.execute(f"""
insert into queries 
(query_name, query_contents) 
values 
({query_name, query_contents});
""")

st.write(insert_response)
