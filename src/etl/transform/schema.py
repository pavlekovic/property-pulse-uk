from pyspark.sql.types import *

def pp_schema() -> StructType:
    """Schema for UK Price Paid data (no header)."""
    return StructType([
        StructField("transaction_id", StringType(), True),
        StructField("price", IntegerType(), True),
        StructField("transfer_datetime", StringType(), True),
        StructField("postcode", StringType(), True),
        StructField("property_type", StringType(), True),   # D/S/T/F/O
        StructField("new_build", StringType(), True),       # Y/N
        StructField("tenure", StringType(), True),          # F/L
        StructField("paon", StringType(), True),
        StructField("saon", StringType(), True),
        StructField("street", StringType(), True),
        StructField("locality", StringType(), True),
        StructField("town", StringType(), True),
        StructField("district", StringType(), True),
        StructField("county", StringType(), True),
        StructField("ppd_category", StringType(), True),    # A/B
        StructField("record_status", StringType(), True)    # A/C/D
    ])