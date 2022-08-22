import os

from mongo import MongoConnection

# config.py is the approach that Superset takes, can't be that bad
vector_db_host = os.environ.get("VECTOR_DB_HOST", "http://192.168.54.124:6333")
fast_api_host = os.environ.get("FAST_API_HOST", "http://127.0.0.1:8004")
query_results_path = "./pages/results/"
saved_queries_path = "./pages/saved_queries/"

ml_dataset = MongoConnection(
    user=os.environ.get("ML_MONGO_USER"),
    password=os.environ.get("ML_MONGO_PASSWORD"),
    host=os.environ.get("ML_MONGO_HOST"),
).get_collection("ml-cxr-datalake")
