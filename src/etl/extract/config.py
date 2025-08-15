from pathlib import Path

# Full (historic) file – fetched on first run
FULL_URL = "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv"
OUTPUT_PATH = "data/raw"

# Raw files directory
RAW_DIR = Path("data/raw")

# Download details
CHUNK_SIZE = 1024 * 128   # 128 KB
TIMEOUT = 60              # in seconds