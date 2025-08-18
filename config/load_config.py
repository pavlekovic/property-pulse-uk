from pathlib import Path

# Base path: go two levels up from this config file
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

# Parquet file
PARQUET_DIR = DATA_DIR / "transform"