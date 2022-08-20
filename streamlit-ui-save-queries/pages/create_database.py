import streamlit as st
from utils import create_connection


st.markdown("# Create Database")

st.write("""A database in SQLite is just a file on same server. 
By convention their names always end in .db""")


db_filename = st.text_input("DB Filename")
create_db = st.button('Create Database')

if create_db:
    if db_filename.endswith('.db'):
        conn = create_connection(db_filename)
        st.write(conn) # success message?
    else: 
        st.write('DB filename must end with .db, please retry.')
