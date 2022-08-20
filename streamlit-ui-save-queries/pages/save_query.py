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


save_query = st.checkbox('Save Query')
run_query = st.button('Run Query')

if run_query:

    try:
        query = analysis_conn.execute(query_contents)

        cols = [column[0] for column in query.description]
        results_df= pd.DataFrame.from_records(
            data = query.fetchall(), 
            columns = cols
        )
        st.dataframe(results_df)
    except:
        pass

    if save_query:

        try:
            query_db_conn.execute("""
                create table queries (query_name varchar, query_contents varchar)
            """
            )
        except Exception as e:
            pass # don't let user see this
        
        # the streamlit input box will add a bunch of backslash Ns 
        
        query_contents = query_contents.replace('\n',' ')
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
