import streamlit as st
from utils import create_connection, instantiate_queries_table
import pandas as pd
import os


st.markdown("# Run Query")

query_name = st.text_input("Query Name")
query_contents = st.text_area("Json Query", height=100)
query_db_conn = create_connection("queries.db")
save_query = st.checkbox("Save Query")


if save_query:

    instantiate_queries_table()

    # the streamlit input box will add a bunch of backslash Ns
    query_contents = query_contents.replace("\n", " ")
    insert_statement = f"""
        insert into queries
        (query_name, query_contents)
        values
        {query_name, query_contents};
    """

    # don't know where the extra brackets come from
    st.write(insert_statement)
    insert_response = query_db_conn.execute(insert_statement)

    # I always forget to commit
    query_db_conn.commit()
    st.write(insert_response)
