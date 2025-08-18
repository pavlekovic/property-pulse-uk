import os
from dotenv import load_dotenv

load_dotenv()  # load from .env

def build_db_url():
    """Build Postgres connection URL from .env components."""
    user = os.getenv("TARGET_DB_USER")
    password = os.getenv("TARGET_DB_PASSWORD")
    host = os.getenv("TARGET_DB_HOST")
    port = os.getenv("TARGET_DB_PORT", "5432")
    dbname = os.getenv("TARGET_DB_NAME")

    if not all([user, password, host, dbname]):
        raise ValueError("Missing one or more DB env variables.")

    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"