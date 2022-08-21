from fastapi import FastAPI, Path, Query
from utils import create_connection
import pandas as pd

app = FastAPI()


@app.get("/queries/{query_name}")
async def root(
    query_name: str = Path(title="The ID of the item to get"),
):
    analysis_conn = create_connection("core.db")
    queries_conn = create_connection("queries.db")
    query = queries_conn.execute(f"""
    select query_contents from queries where query_name = {query_name}
    """)  
    cols = [column[0] for column in query.description]
    results_df = pd.DataFrame.from_records(
        data = query.fetchall(), 
        columns = cols
    )
    return results_df.to_json()

