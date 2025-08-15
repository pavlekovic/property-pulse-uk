import requests
from pathlib import Path

def fetch_ons_geojson(query_url: str, output_path: Path, timeout: int):
    
    # Define parameters for the get request
    params = {
        "where": "1=1",          # get all features (no filtering)
        "outFields": "*",        # include all attributes
        "outSR": "4326",         # WGS84 lat/lon
        "f": "geojson",          # required for GeoJSON format
        "returnGeometry": "true"
    }

    # Run the get request
    r = requests.get(query_url, params=params, timeout=timeout)
    
    # Check HTTP response code (SUCCESS does nothing)
    r.raise_for_status()
    
    # Define temp path for storing parts of data
    tmp = output_path.with_suffix(output_path.suffix + ".part")
    
    # Write HTTP response to temporary file
    with open(tmp, "wb") as f:
        f.write(r.content)
    
    # Replace temp with actual file
    tmp.replace(output_path)

    return output_path