from fastapi import FastAPI, Path
from utils import create_connection, sql_to_df
import pandas as pd

app = FastAPI()


@app.get("/query/{query_name}/{json_format}")
async def root(
    query_name: str,
    json_format: str,
):
    analysis_conn = create_connection("core.db")
    queries_conn = create_connection("queries.db")
    selected_query = list(
        queries_conn.execute(
            f"""
        select query_contents from queries where query_name = '{query_name}'
    """,
        ).fetchall(),
    )[0]
    selected_query = selected_query[0]
    results_df = sql_to_df(analysis_conn, selected_query)
    return results_df.to_json(orient=json_format)
