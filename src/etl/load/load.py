import sys
import pandas as pd
from src.etl.load.db import get_engine, get_target
from src.utils.read_utils import read_input
from src.utils.logging_utils import setup_logger

# Initialize logger
logger = setup_logger(name="load", log_file="load.log")

def load() -> int:
    
    """Load Transformed Property Data into Postgres"""
    
    try:
        logger.info("=== LOAD STARTED ===")
        
        # Read data (Parquet preferred)
        df = read_input(limit=10_000, engine="pandas")

        # Load to Postgres (creates table automatically if missing)
        engine = get_engine()
        schema, table = get_target()

        logger.info(f"Loading {len(df)} rows into {schema}.{table} …")
        
        # Write to sql table
        df.to_sql(
            name=table,
            con=engine,
            schema=schema if schema else None,
            if_exists="replace",
            index=False,
            chunksize=2000,
            method="multi",
        )
        logger.info("DONE")
        logger.info("=== LOAD COMPLETED ===")
        return 0

    except Exception as e:
        logger.error(f"FAILED: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(load())