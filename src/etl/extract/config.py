from pathlib import Path

# Full (historic) file – fetched on first run
FULL_URL = "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv"

# Base path: go three levels up from this config file
BASE_DIR = Path(__file__).resolve().parents[3]

# Raw files directory
RAW_DIR = BASE_DIR / "data" / "raw"

# Example output path for a specific file
OUTPUT_PATH = RAW_DIR / "pp_complete.csv"

# Download details
CHUNK_SIZE = 1024 * 128   # 128 KB
TIMEOUT = 60              # in seconds