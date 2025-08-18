import os
from sqlalchemy import create_engine
from src.utils.db_utils import build_db_url
from dotenv import load_dotenv

# Read .env
load_dotenv()

def get_engine():
    db_url = os.getenv("TARGET_DB_URL") or build_db_url()
    return create_engine(db_url, pool_pre_ping=True)

def get_target():
    schema = os.getenv("TARGET_DB_SCHEMA")
    table  = os.getenv("TARGET_DB_TABLE")
    return schema, table