import streamlit as st
import plotly.express as px
from utils import (
    create_connection,
    sql_to_df,
    instantiate_queries_table,
    save_plot,
)
import os
import pandas as pd

analysis_conn = create_connection("core.db")
queries_conn = create_connection("queries.db")

# in case it doesn't already exist
instantiate_queries_table()
queries_df = sql_to_df(queries_conn, "select * from queries")
selected_query = st.selectbox("Query to Execute", list(queries_df["query_name"]))

plotly_code_name = st.text_input("Plotly Code Name")

selected_mask = queries_df["query_name"] == selected_query
selected_query = queries_df[selected_mask]["query_contents"].iloc[0]

st.write("Plotly code here (example below)")
st.code(
    """
px.bar(
    results_df,
    x="Hospital Name",
    y="count(*)",
)
""",
)

plotly_code = st.text_area("Plotly Code")

submitted = st.button("Run Analysis")

save_query_button = st.checkbox("Save Analysis")

if submitted:
    try:
        results_df = sql_to_df(analysis_conn, selected_query)
        st.dataframe(results_df)

        fig = eval(plotly_code)
        st.plotly_chart(fig, use_container_width=True)

        save_plot(
            plotly_code_name,
            plotly_code,
        )
        # TODO: will replace with a case statement soon

    except Exception as e:
        st.write(e)
