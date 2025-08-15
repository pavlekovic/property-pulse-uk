import sys
from pathlib import Path
from fetch_data import stream_download
from state_utils import read_state, write_state
from date_utils import last_month_ym
from config import (FULL_URL, MONTHLY_URL, RAW_DIR,CHUNK_SIZE, TIMEOUT, STATE_FILE)

def run() -> int:
    try:
        # Make sure the destination folder exists
        RAW_DIR.mkdir(parents=True, exist_ok=True)

        # Read and return last state to be able to choose full history or monthly download
        state = read_state(STATE_FILE)
        
        # Store state in a variable to be reused
        full_done = state.get("full_import_done", False)
        
        # If the state is DEFAULT_STATE
        if not full_done:
            # First run
            fetch_url = FULL_URL
            out_path = RAW_DIR / "pp_complete.csv"
        else:
            # Monthly update run
            #ym = "2025-07"
            fetch_url = MONTHLY_URL
            out_path = RAW_DIR / last_month_ym() / "pp_monthly.csv"
        
        # if this month's file already exists, skip
        if out_path.exists():
            print(f"[extract] FAILED: File already exists.")
            return 1
        
        # Perform fetch data and pass on parameters
        saved = stream_download(
            url=fetch_url,                  # Either full or monthly
            output_path=out_path,        # Either raw/ or raw/YYYY-MM
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
        
        if saved:
            print(f"[extract] SUCCESS: saved to {out_path}")
            return 0
        else:
            print(f"[extract] FAILED: no file saved")
            return 1
        
        
    # In case fetching data fails for whatever reason, print and return 1
    except Exception as e:
        print(f"[extract] FAILED: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run())