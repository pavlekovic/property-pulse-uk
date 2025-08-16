from pathlib import Path
from src.etl.extract.fetch_geojson import fetch_ons_geojson

def ensure_geojson_once(state: dict, mapping_dir: Path, geojson_path: Path, geojson_url: str, timeout: int):

    # Check if file exists and state is True (so that there are no unnecessary get requests)
    if state.get("geojson_fetched") and geojson_path.exists():
        print(f"[extract] GeoJSON already fetched: {geojson_path}")
        return state

    # Make sure the destination folder exists
    mapping_dir.mkdir(parents=True, exist_ok=True)

    # Check if file exists (so that there are no unnecessary get requests)
    if geojson_path.exists():
        # File is there but flag is false so update state
        state["geojson_fetched"] = True
        return state
    
    # Fetch data from API
    fetch_ons_geojson(
        query_url=geojson_url,
        output_path=geojson_path,
        timeout=timeout,
    )
    
    # Update state
    state["geojson_fetched"] = True
    
    return state