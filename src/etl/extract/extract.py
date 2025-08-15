import sys
from pathlib import Path
from fetch_data import stream_download
from config import (FULL_URL, OUTPUT_PATH, RAW_DIR,CHUNK_SIZE, TIMEOUT)

def run() -> int:
    try:
        # Make sure the destination folder exists
        RAW_DIR.mkdir(parents=True, exist_ok=True)

        # Perform fetch data and pass on parameters
        saved = stream_download(
            url=FULL_URL,
            output_path=OUTPUT_PATH,
            chunk_size=CHUNK_SIZE,
            timeout=TIMEOUT
        )

        if saved:
            return 0

    # In case fetching data fails for whatever reason, print and return 1
    except Exception as e:
        print(f"[extract] FAILED: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run())