import sys
from pathlib import Path
from src.utils.pyspark_utils import create_spark
from src.utils.read_utils import read_input
from pyspark.sql import DataFrame
from pyspark.sql.functions import (col, avg, count, max as sf_max, min as sf_min, add_months, lit)


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

# Return df for only the last 60 months
def last_5_yrs_window(df: DataFrame, hist=60) -> DataFrame:
    max_date = df.select(sf_max(col("transfer_date")).alias("maxd")).collect()[0]["maxd"]
    cutoff = df.select(add_months(lit(max_date), -hist).alias("cutoff")).collect()[0]["cutoff"]
    return df.filter(col("transfer_date") >= lit(cutoff))

# Calc average price per property type
def fact_avg_monthly_ptype (df: DataFrame) -> DataFrame:
    """Monthly average price and transaction count by (district, property_type, year, month)."""
    
    # Define groups to use for grouping
    group_keys = ["district", "property_type", "year", "month"]
    fact = (
        df.groupBy(*group_keys).agg(
            avg(col("price")).alias("avg_price"), # Average property price in that group by property type
            count(lit(1)).alias("txn_count"),     # Count transactions in that group
          )
    )
    return fact

# Calc average price per district
def fact_avg_monthly_district (df: DataFrame) -> DataFrame:
    """Monthly average price by (district, year, month)."""
    
    group_keys = ["district", "year", "month"]
    fact = (
        df.groupBy(*group_keys).agg(
            avg(col("price")).alias("avg_price"), # Average property price in that group
            count(lit(1)).alias("txn_count"),     # Count transactions in that group
        )
    )
    return fact

# Define a range of price for input into ML model based on prices in the last 5 years
def bounds_years(df_years: DataFrame) -> DataFrame:
    """Min/Max price in the last X years by district."""
    
    # Define key for partition
    key = "district"
    
    # Create year bounds
    bounds = (
        df_years.groupBy(key).agg(
            sf_min(col("price")).alias("min_price_past"),
            sf_max(col("price")).alias("max_price_past"),
        )
    )
    return bounds

def write_partitioned(df: DataFrame, out_dir: Path) -> None:
    """Write a partitioned parquet by (year, month), using dynamic overwrite if incremental."""
    
    ensure_parent_dir(out_dir)
    # Coalesce a little so each partition isn't too tiny (tune as needed)
    df = df.repartition("year", "month")
    (
        df.write
          .mode("overwrite")
          .partitionBy("year", "month")
          .parquet(str(out_dir))
    )
    
def write_single(df: DataFrame, out_path: Path) -> None:
    """ Write a single parquet file (coalesce to 1 for small aggregates)."""
    
    ensure_parent_dir(out_path)
    (
        df.coalesce(1)
          .write
          .mode("overwrite")
          .parquet(str(out_path))
    )