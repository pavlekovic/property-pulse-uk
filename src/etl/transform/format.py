from pyspark.sql import DataFrame
from pathlib import Path

def format_to_parquet(df: DataFrame, out_dir: Path, first_load: bool):
    
    # Make sure out_dir is str for PySpark
    out_dir = str(out_dir)
    
    #if not first_load:
    #    df.sparkSession.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

    # Repartition by year to create tidy partitions/files
    (
        df.repartition("year")
          .write
          .mode("overwrite")
          .partitionBy("year")
          .parquet(out_dir)
    )
        