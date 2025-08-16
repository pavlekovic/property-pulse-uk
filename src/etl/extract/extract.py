import sys
from pathlib import Path
from fetch_data import stream_download
from geojson_utils import ensure_geojson_once
from state_utils import read_state, write_state
from date_utils import last_month_ym
from path_resolve_utils import resolve_url_and_out_path
from config import (FULL_URL, MONTHLY_URL, RAW_DIR,CHUNK_SIZE, TIMEOUT, STATE_FILE, 
                    FULL_FILENAME, MONTHLY_FILENAME, MAPPING_DIR, GEOJSON_PATH, 
                    GEOJSON_API_URL, LOG_FILE_EXTRACT)
import logging

# Logging setup
logging.basicConfig(
    filename=str(LOG_FILE_EXTRACT),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger("extract")

def run() -> int:
    try:
        log.info("=== EXTRACT STARTED ===")
        log.info(f"RAW_DIR={RAW_DIR}")
        log.info(f"STATE_FILE={STATE_FILE}")
        
        # Make sure the destination folder exists
        RAW_DIR.mkdir(parents=True, exist_ok=True)

        # Load info from state JSON file
        state = read_state(STATE_FILE)
        log.info(f"Loaded state: full_done={state.get('full_import_done')}, "
                 f"last_month_fetched={state.get('last_month_fetched')}, "
                 f"geojson_fetched={state.get('geojson_fetched')}")
        
        # --------------------------------------
        # GEOJSON DATA
        # --------------------------------------
        
        if GEOJSON_PATH.exists():
            log.info(f"GeoJSON already exists, skipping API request: {GEOJSON_PATH}")
        else:
            log.info(f"Starting download: {GEOJSON_API_URL}")
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
                    log.info(f"GeoJSON ready at: {GEOJSON_PATH}")
            else:
                log.warning("GeoJSON not marked as fetched; continuing.")
        
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
        log.info(f"Selected mode={'full' if not full_done else 'monthly'}")
        
        # if this month's file already exists, skip
        if out_path.exists():
            log.info(f"Price paid data already exists; skipping download: {out_path}")
            log.info("=== EXTRACT COMPLETED (PARTIAL) ===")
            return 0
        
        # Perform fetch data and pass on parameters
        log.info(f"Starting download: {fetch_url}")
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
            log.info(f"Full history dataset ready at: {saved_path}")
            log.info("State updated: full_import_done=True")
        else:                                               # If monthly run
            state["last_month_fetched"] = last_month_ym()
            log.info(f"Monthly dataset ready at: {saved_path}")
            log.info(f"State updated: last_month_fetched={state['last_month_fetched']}")
        
        # Write state
        write_state(STATE_FILE, state)
        log.info(f"State saved to {STATE_FILE}")
        log.info("=== EXTRACT COMPLETED ===")
        
        return 0
            
    # In case fetching data fails for whatever reason, print and return 1
    except Exception as e:
        log.exception("=== EXTRACT FAILED ===")
        return 1

if __name__ == "__main__":
    sys.exit(run())