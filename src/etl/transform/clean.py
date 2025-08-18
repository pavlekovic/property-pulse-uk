from pyspark.sql import DataFrame
from pyspark.sql.functions import col, to_date, year, month, upper, regexp_replace

def standardize_data (df: DataFrame):
    """Standardize datetime and postcode"""
    df = (
        df
        .withColumn("transfer_date", to_date(col("transfer_datetime").substr(1,10)))    # Create a column transfer_date from transfer_datetime by taking first 10 characters
        .withColumn("year", year(col("transfer_date")))                                 # Create a column year from transfer_date
        .withColumn("month", month(col("transfer_date")))                               # Create a column month from transfer_date
        .withColumn("postcode", upper(regexp_replace(col("postcode"), r"\s+", "")))     # Remove all whitespaces
        )
    return df

def remove_bad_rows (df: DataFrame):
    """Remove rows where transfer_datetime or price are null"""
    df = (
        df
        .filter(col("transfer_datetime").isNotNull())       # Keep rows where transfer_datetime is not null
        .filter(col("price").isNotNull())                   # Keep rows where price is not null
        .filter(col("price") > 0)                           # Keep rows where price is not 0
    )
    return df

def drop_duplicates (df:DataFrame):
    """Remove duplicates by transaction_id (keeps first)"""
    df = (
        df
        .dropDuplicates(["transaction_id"])                # Drop rows with the same transaction_id
    )
    return df