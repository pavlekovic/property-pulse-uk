from pathlib import Path

# Base path: go two levels up from this config file
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

# Files directory
RAW_DIR = DATA_DIR / "raw"
TRANS_DIR = DATA_DIR / "transformed"
FULL_CSV = RAW_DIR / "pp_complete.csv"
MONTHLY_FILENAME = "pp_monthly.csv"

# State file
STATE_FILE = RAW_DIR / "_state.json" 

# Data marts
MARTS_DIR = DATA_DIR / "marts"
MART_FACT_BY_TYPE = MARTS_DIR / "fact_prices"             # partitioned by year
MART_PREDICTION = MARTS_DIR / "fact_prediction"           # single file
MART_BOUNDS_5Y = MARTS_DIR / "agg_bounds_5y"              # single file