from pathlib import Path
import pandas as pd
from config.transform_config import TRANS_DIR

PARQUET_DIR = TRANS_DIR

def read_input(limit: int):

    # Read X rows into df
    if PARQUET_DIR.exists():
        df = pd.read_parquet(PARQUET_DIR)
    else:
        raise FileNotFoundError("No input found: missing Parquet file.")
    if len(df) > limit:
        df = df.head(limit)
    return df