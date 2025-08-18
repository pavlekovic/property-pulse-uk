from pyspark.sql import DataFrame
from pathlib import Path

def format_to_parquet(df: DataFrame, out_dir: Path, first_load: bool):
    
    # Make sure out_dir is str for PySpark
    out_dir = str(out_dir)
    
    if first_load:
        (
            df.write
            .mode("overwrite")
            .partitionBy("year", "month")
            .parquet(out_dir)
        )
    else:
        df.sparkSession.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
        (
           df.write
            .mode("overwrite")
            .partitionBy("year", "month")
            .parquet(out_dir) 
        )
        