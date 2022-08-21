from fastapi import FastAPI, Path, Query
from utils import create_connection, sql_to_df
import pandas as pd

app = FastAPI()


@app.get("/queries/{query_name}")
async def root(
    query_name: str = Path(title="Query name of the query to run"),
):
    analysis_conn = create_connection("core.db")
    queries_conn = create_connection("queries.db")
    selected_query = queries_conn.execute(f"""
    select query_contents from queries where query_name = {query_name}
    """)  
    results_df = sql_to_df(analysis_conn, selected_query)
    return results_df.to_json()

