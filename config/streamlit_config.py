from pathlib import Path

# Directories
# Base path: go two levels up from this config file
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
MARTS_DIR = DATA_DIR / "marts"
MAPPING_DIR = DATA_DIR / "mapping"

# Data marts
MART_PREDICTION = MARTS_DIR / "fact_prediction"
MART_FACT_BY_DISTRICT = MARTS_DIR / "fact_prices_district"
MART_BOUNDS_5Y = MARTS_DIR / "agg_bounds_5y.parquet"

# Geojson data
GEOJSON_PATH = MAPPING_DIR / "local_authority.geojson"

# Model path
MODEL_PATH = BASE_DIR / "models" / "xgb_price.pkl"
