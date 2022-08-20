import sqlite3
import streamlit as st
import pandas as pd
import os
import plotly.express as px


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


def create_database():
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


def upload_data():
    st.markdown("# Upload Data")
    # https://discuss.streamlit.io/t/uploading-csv-and-excel-files/10866/2
    sqlite_dbs = [file for file in os.listdir('.') if file.endswith('.db')]
    db_filename = st.selectbox('DB Filename', sqlite_dbs)
    table_name = st.text_input('Table Name to Insert')
    conn = create_connection(db_filename)
    uploaded_file = st.file_uploader('Choose a file')
    if uploaded_file is not None:
        #read csv
        try:
            df = pd.read_csv(uploaded_file)
            df.to_sql(name=table_name, con=conn)
            st.write('Data uploaded successfully. These are the first 5 rows.')
            st.dataframe(df.head(5))

        except Exception as e:
            st.write(e)


def run_query():
    st.markdown("# Run Query")
    sqlite_dbs = [file for file in os.listdir('.') if file.endswith('.db')]
    db_filename = st.selectbox('DB Filename', sqlite_dbs)

    query = st.text_area("SQL Query", height=100)
    conn = create_connection(db_filename)

    plot_options = [
        'bar',
        'line',
        'scatter',
    ]
    plot_type = st.selectbox(
        'Plot Type', 
        plot_options
    )

    # more fun if this is a selectbox from the query but quite awkward to get
    # that to work with streamlit
    x_axis = st.text_input('X Axis')
    y_axis = st.text_input('Y Axis')

    submitted = st.button('Run Analysis')

    if submitted:
        try:
            query = conn.execute(query)
            cols = [column[0] for column in query.description]
            results_df= pd.DataFrame.from_records(
                data = query.fetchall(), 
                columns = cols
            )
            st.dataframe(results_df)

            # TODO: will replace with a case statement soon
            if plot_type == 'bar':
                fig = px.bar(
                    results_df, 
                    x=x_axis,
                    y=y_axis, 
                )
            if plot_type == 'line':
                fig = px.line(
                    results_df, 
                    x=x_axis,
                    y=y_axis, 
                )
            if plot_type == 'scatter':
                fig = px.scatter(
                    results_df, 
                    x=x_axis,
                    y=y_axis, 
                )

            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.write(e)

page_names_to_funcs = {
    "Create Database": create_database,
    "Upload Data": upload_data,
    "Run Query": run_query,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()


