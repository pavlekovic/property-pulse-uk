from pyspark.sql import DataFrame
from pyspark.sql.functions import col


def simple_report (df: DataFrame):
    """Return quality metrics for check and logging."""
    total = df.count()
    null_price = df.filter(col("price").isNull()).count()
    null_date = df.filter(col("transfer_date").isNull()).count()
    neg_zero_price = df.filter(col("price")<=0).count()
    dup_rows = total - df.select("transaction_id").distinct().count()
    
    return {
        "rows": total,
        "null_price": null_price,
        "null_date": null_date,
        "neg_and_zero_price": neg_zero_price,
        "duplicate_tx_ids": dup_rows
    }