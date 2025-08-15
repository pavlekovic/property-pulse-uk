import sys
from pathlib import Path
from fetch_data import stream_download
from geojson_utils import ensure_geojson_once
from state_utils import read_state, write_state
from date_utils import last_month_ym
from path_resolve_utils import resolve_url_and_out_path
from config import (FULL_URL, MONTHLY_URL, RAW_DIR,CHUNK_SIZE, TIMEOUT, STATE_FILE, 
                    FULL_FILENAME, MONTHLY_FILENAME, MAPPING_DIR, GEOJSON_PATH, GEOJSON_API_URL)

def run() -> int:
    try:
        # Make sure the destination folder exists
        RAW_DIR.mkdir(parents=True, exist_ok=True)

        # Load info from state JSON file
        state = read_state(STATE_FILE)
        
        
        # --------------------------------------
        # GEOJSON DATA
        # --------------------------------------
        
        saved_geojson = ensure_geojson_once(
                state=state,
                mapping_dir=MAPPING_DIR,
                geojson_path=GEOJSON_PATH,
                geojson_url=GEOJSON_API_URL,
                timeout=TIMEOUT,
            )
        
        # Write state for geojson
        write_state(STATE_FILE, saved_geojson)
        
        
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
            print(f"[extract] Price paid data already fetched: {out_path}")
            return 1
        
        # Perform fetch data and pass on parameters
        saved_data = stream_download(
            url=fetch_url,                  # Either full or monthly
            output_path=out_path,           # Either raw/ or raw/YYYY-MM
            chunk_size=CHUNK_SIZE,
            timeout=TIMEOUT
        )
        
        # Update state
        if not full_done:                                   # If first run
            state["full_import_done"] = True
            state["last_month_fetched"] = None
        else:                                               # If monthly run
            state["last_month_fetched"] = last_month_ym()
        
        # Write state
        write_state(STATE_FILE, state)
        
        if saved_data:
            print(f"[extract] SUCCESS: saved to {out_path}")
        else:
            print(f"[extract] FAILED: no file saved")
            
    # In case fetching data fails for whatever reason, print and return 1
    except Exception as e:
        print(f"[extract] FAILED: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run())