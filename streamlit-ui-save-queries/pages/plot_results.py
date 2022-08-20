import streamlit as st
import plotly.express as px
from utils import create_connection
import os
import pandas as pd

sqlite_dbs = [file for file in os.listdir('.') if file.endswith('.db')]
db_filename = st.selectbox('DB Filename', sqlite_dbs)
analysis_conn = create_connection(db_filename)
queries_conn = create_connection("queries.db")


query = queries_conn.execute('select * from queries')
cols = [column[0] for column in query.description]
queries_df = pd.DataFrame.from_records(
    data = query.fetchall(), 
    columns = cols
)
st.dataframe(queries_df))

query = st.selectbox('Query to Execute', queries_df)


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
        query = analysis_conn.execute(query)
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