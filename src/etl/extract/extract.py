import sys
from src.etl.extract.fetch_data import stream_download
from src.utils.geojson_utils import ensure_geojson_once
from src.utils.state_utils import read_state, write_state
from src.utils.date_utils import last_month_ym
from src.utils.path_resolve_utils import resolve_url_and_out_path
from src.utils.logging_utils import setup_logger
from config.extract_config import (FULL_URL, MONTHLY_URL, RAW_DIR,CHUNK_SIZE, TIMEOUT, 
    STATE_FILE, FULL_FILENAME, MONTHLY_FILENAME, MAPPING_DIR, GEOJSON_PATH, GEOJSON_API_URL, GEOJSON_PC_PATH, GEOJSON_PC_API_URL)

# Initialize logger
logger = setup_logger(name="extract", log_file="extract.log")

# Master extract function
def extract() -> int:
    
    """Run the extract step: fetch GeoJSON, fetch full/monthly CSV, and update state."""
    
    try:
        logger.info("=== EXTRACT STARTED ===")
        
        # Make sure the destination folder exists
        RAW_DIR.mkdir(parents=True, exist_ok=True)

        # Load info from state JSON file
        state = read_state(STATE_FILE)
        
        # --------------------------------------
        # GEOJSON DATA
        # --------------------------------------
        
        # Local authority
        if GEOJSON_PATH.exists():
            logger.info(f"GeoJSON (local authority) already exists, skipping API request: {GEOJSON_PATH}")
        else:
            saved_geojson = ensure_geojson_once(
                    state=state,
                    mapping_dir=MAPPING_DIR,
                    geojson_path=GEOJSON_PATH,
                    geojson_url=GEOJSON_API_URL,
                    timeout=TIMEOUT,
                )
            
            # Write state for geojson
            write_state(STATE_FILE, saved_geojson)
            
            if state.get("geojson_fetched"):
                logger.info(f"GeoJSON (local authority) ready at: {GEOJSON_PATH}")
            else:
                logger.warning("GeoJSON (local authority) not marked as fetched; continuing.")
                
        # Post codes
        if GEOJSON_PC_PATH.exists():
            logger.info(f"GeoJSON (post_codes) already exists, skipping API request: {GEOJSON_PC_PATH}")
        else:
            saved_geojson = ensure_geojson_once(
                    state=state,
                    mapping_dir=MAPPING_DIR,
                    geojson_path=GEOJSON_PC_PATH,
                    geojson_url=GEOJSON_PC_API_URL,
                    timeout=TIMEOUT,
                )
            
            # Write state for geojson
            write_state(STATE_FILE, saved_geojson)
            
            if state.get("geojson_fetched"):
                logger.info(f"GeoJSON (post_codes) ready at: {GEOJSON_PC_PATH}")
            else:
                logger.warning("GeoJSON (post_codes) not marked as fetched; continuing.")
        
        # --------------------------------------
        # PROPERTY PRICE DATA
        # --------------------------------------
        
        # Store state in a variable to be reused
        full_done = state.get("full_import_done", False)
        
        fetch_url, out_path = resolve_url_and_out_path(
            full_done=full_done,
            raw_dir=RAW_DIR,
            full_url=FULL_URL,
            monthly_url=MONTHLY_URL,
            full_filename=FULL_FILENAME,
            monthly_filename=MONTHLY_FILENAME,
        )
        
        # if this month's file already exists, skip
        if out_path.exists():
            logger.info(f"Price paid data already exists; skipping download: {out_path}")
            logger.info("=== EXTRACT COMPLETED (PARTIAL) ===")
            return 0
        
        # Perform fetch data and pass on parameters
        saved_path = stream_download(
            url=fetch_url,                  # Either full or monthly
            output_path=out_path,           # Either raw/ or raw/YYYY-MM
            chunk_size=CHUNK_SIZE,
            timeout=TIMEOUT
        )
        
        # Update state
        if not full_done:                                   # If first run
            state["full_import_done"] = True
            state["last_month_fetched"] = None
            logger.info(f"Full history dataset ready at: {saved_path}")
        else:                                               # If monthly run
            state["last_month_fetched"] = last_month_ym()
            logger.info(f"Monthly dataset ready at: {saved_path}")
        
        # Write state
        write_state(STATE_FILE, state)
        logger.info("=== EXTRACT COMPLETED ===")
        
        return 0
            
    # In case fetching data fails for whatever reason, print and return 1
    except Exception as e:
        logger.error(f"Data extraction failed: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(extract())