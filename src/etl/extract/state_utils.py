from pathlib import Path
import json

# In case running for the first time
DEFAULT_STATE = {
    "full_import_done": False,
    "last_month_fetched": None,
    "geojson_fetched": False
}

# Read the current state from the JSON file
def read_state(state_file: Path):
    
    # If running for the first time return default state
    if not state_file.exists():
        return DEFAULT_STATE.copy()
    
    # If not running for the first time return contents of the file
    with open(state_file, "r") as f:
        return json.load(f)

def write_state (state_file: Path, state: dict):
    
    # Make sure the destination folder exists
    state_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Define temp file/path for storing data while being downloaded
    tmp = state_file.with_suffix(state_file.suffix + ".part") # Use Path handling instead of concat
    
    # Write to (temporary) file
    with open (tmp, "w") as f:
        json.dump(state, f) # Dump is a json lib built-in function for taking an object (dict) and writing it to JSON file
    
    # Replace temporary with actual file
    tmp.replace(state_file)