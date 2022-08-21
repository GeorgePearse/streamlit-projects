import streamlit as st
import plotly.express as px
from utils import create_connection
import os
import pandas as pd

sqlite_dbs = [file for file in os.listdir('.') if file.endswith('.db')]
db_filename = st.selectbox('DB Filename', sqlite_dbs)
analysis_conn = create_connection(db_filename)
queries_conn = create_connection("queries.db")

try: 
    queries_conn.execute("""
        create table queries (query_name varchar, query_contents varchar);
    """
    )
except:
    pass 

query = queries_conn.execute('select * from queries')
cols = [column[0] for column in query.description]
queries_df = pd.DataFrame.from_records(
    data = query.fetchall(), 
    columns = cols
)
st.dataframe(queries_df)

selected_query = st.selectbox('Query to Execute', list(queries_df['query_name']))

selected_mask = (queries_df['query_name'] == selected_query)
selected_query = queries_df[selected_mask]['query_contents'].iloc[0]

plot_options = [
    'bar',
    'line',
    'scatter',
]
plot_type = st.selectbox(
    'Plot Type', 
    plot_options
)

save_analysis = st.checkbox('Save Analysis')
submitted = st.button('Run Analysis')


if submitted:
    try:
        query = analysis_conn.execute(selected_query)
        cols = [column[0] for column in query.description]
        results_df= pd.DataFrame.from_records(
            data = query.fetchall(), 
            columns = cols
        )
        st.dataframe(results_df)

        x_axis = list(results_df.columns)[0]
        y_axis = list(results_df.columns)[1]

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