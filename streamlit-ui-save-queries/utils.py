import streamlit as st
import sqlite3
from pandas.core.frame import DataFrame
import pandas as pd

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        st.write(e)

    return conn


def instantiate_queries_table():
    try: 
        conn = create_connection('queries.db')
        conn.execute("""
            create table queries (query_name varchar, query_contents varchar);
        """
        )
        conn.commit()
        # always go for default index names when possible
        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            ON queries(query_name);
        """
        )
        conn.commit()

    except:
        pass 


def sql_to_df(conn, query): 
    """
    Pandas does this well, maybe just copy there's
    """
    results = conn.execute(query)

    cols = [column[0] for column in results.description]
    results_df= pd.DataFrame.from_records(
        data = results.fetchall(), 
        columns = cols
    )
    return results_df