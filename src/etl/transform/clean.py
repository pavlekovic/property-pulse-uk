from pyspark.sql import DataFrame
from pyspark.sql.functions import col, to_timestamp, to_date, year, trim, upper, regexp_replace, coalesce, lit

def standardize_data (df: DataFrame) -> DataFrame:
    """Standardize datetime and postcode"""
    
    # Try multiple timestamp formats; if none match, fall back to date-only
    ts1 = to_timestamp(col("transfer_datetime"), "yyyy-MM-dd HH:mm:ss")
    ts2 = to_timestamp(col("transfer_datetime"), "yyyy-MM-dd HH:mm")
    ts3 = to_timestamp(col("transfer_datetime"), "yyyy-MM-dd'T'HH:mm:ss")
    # If no timestamp matched, parse date-only
    date_only = to_date(col("transfer_datetime"), "yyyy-MM-dd")

    df = df.withColumn("transfer_ts", coalesce(ts1, ts2, ts3))
    df = df.withColumn("transfer_date", coalesce(to_date(col("transfer_ts")), date_only))
    df = df.withColumn("year", year(col("transfer_date")))
    
    # Normalize postcode: uppercase + strip all whitespace
    df = df.withColumn("postcode", upper(regexp_replace(col("postcode"), r"\s+", "")))
    
    # Exclude property_type == 'O'
    df = df.filter(upper(trim(col("property_type"))) != lit("O"))
    
    return df
    
def remove_bad_rows (df: DataFrame) -> DataFrame:
    """Remove rows where transfer_datetime or price are null"""
    df = (
        df
        .filter(col("transfer_datetime").isNotNull())       # Keep rows where transfer_datetime is not null
        .filter(col("price").isNotNull())                   # Keep rows where price is not null
        .filter(col("price") > 0)                           # Keep rows where price is not 0
    )
    return df

def drop_duplicates (df:DataFrame) -> DataFrame:
    """Remove duplicates by transaction_id (keeps first)"""
    df = (
        df
        .dropDuplicates(["transaction_id"])                # Drop rows with the same transaction_id
    )
    return df