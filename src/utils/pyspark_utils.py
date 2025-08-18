from pyspark.sql import SparkSession

def create_spark(app="Transform", max_part="128m", shuffles="200"):
    """Create a PySpark session"""
    return (
        SparkSession.builder
        .appName(app)
        .master("local[*]")
        .config("spark.sql.files.maxPartitionBytes", max_part)
        .config("spark.sql.shuffle.partitions", shuffles)
        
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.driver.host", "127.0.0.1")       # avoids reverse-DNS hostnames
        .config("spark.driver.port", "0")               # pick any free port
        .config("spark.blockManager.port", "0")         # pick any free port
        
        .getOrCreate()
    )