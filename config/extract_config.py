from pathlib import Path

# Full (historic) url – fetched on first run - and filename
FULL_URL = "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv"
FULL_FILENAME = "pp_complete.csv"

# Monthly url and filename
MONTHLY_URL = "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-monthly-update-new-version.csv"
MONTHLY_FILENAME = "pp_monthly.csv"

# Base path: go two levels up from this config file
BASE_DIR = Path(__file__).resolve().parents[1]

# Raw files directory
RAW_DIR = BASE_DIR / "data" / "raw"

# GEOJSON directory
MAPPING_DIR = BASE_DIR / "data" / "mapping"
GEOJSON_API_URL = "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD_MAY_2025_UK_BGC_V2/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
GEOJSON_PATH = MAPPING_DIR / "local_authority.geojson"

# Postcode centroids
GEOJSON_PC_API_URL = "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NSPL_Online_Latest_Centroids/FeatureServer/1/query?outFields=*&where=1&outFields=*&f=geojson"
GEOJSON_PC_PATH = MAPPING_DIR / "post_codes.geojson"


# Example output path for a specific file
OUTPUT_PATH = RAW_DIR / "pp_complete.csv"

# State file
STATE_FILE = RAW_DIR / "_state.json" 

# Log settings
LOG_FILE_EXTRACT = BASE_DIR / "logs" / "extract.log"

# Download details
CHUNK_SIZE = 1024 * 128   # 128 KB
TIMEOUT = 60              # in seconds