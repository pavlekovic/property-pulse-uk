import requests
from pathlib import Path

def fetch_ons_geojson(query_url: str, output_path: Path, timeout: int):
    """Fetch local authority GeoJSON from ArcGIS API and save to a local file."""

    # Run the get request
    r = requests.get(query_url, timeout=timeout)
    
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