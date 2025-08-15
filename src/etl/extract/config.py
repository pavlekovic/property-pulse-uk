from pathlib import Path

# Full (historic) file – fetched on first run
FULL_URL = "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv"

# Monthly url
MONTHLY_URL = "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-monthly-update-new-version.csv"

# Base path: go three levels up from this config file
BASE_DIR = Path(__file__).resolve().parents[3]

# Raw files directory
RAW_DIR = BASE_DIR / "data" / "raw"

# Example output path for a specific file
OUTPUT_PATH = RAW_DIR / "pp_complete.csv"

# State file
STATE_FILE = RAW_DIR / "_state.json" 

# Download details
CHUNK_SIZE = 1024 * 128   # 128 KB
TIMEOUT = 60              # in seconds