from pathlib import Path
from pyspark.sql import DataFrame
import pandas as pd
from typing import Literal
from config.transform_config import TRANS_DIR

Engine = Literal["pandas", "spark"]

PARQUET_DIR = TRANS_DIR

def read_input(limit: int | None = None, engine: Engine = "pandas", spark=None) -> DataFrame:
    """
    Read Parquet as pandas or Spark DataFrame.

    - engine="pandas": returns pandas.DataFrame
    - engine="spark":  returns pyspark.sql.DataFrame (requires `spark` session)
    - limit: if provided, apply head(limit) in pandas, .limit(limit) in Spark
    """
    
    if not PARQUET_DIR.exists():
        raise FileNotFoundError(f"No input found at {PARQUET_DIR}")
    
    # PySpark
    if engine == "spark":
        if spark is None:
            raise ValueError("When engine='spark', pass a SparkSession via `spark`.")
        sdf = spark.read.parquet(str(PARQUET_DIR))
        return sdf

    # Pandas
    pdf = pd.read_parquet(PARQUET_DIR)
    if limit is not None and len(pdf) > limit:
        pdf = pdf.head(int(limit))
    return pdf
