from typing import Dict
import numpy as np

# Aliases - solves inconsistencies between geojson and csv data
ALIASES: Dict[str, str] = {
    "CITY OF BRISTOL": "BRISTOL",
    "BRISTOL, CITY OF": "BRISTOL",
    "HEREFORDSHIRE, COUNTY OF": "HEREFORDSHIRE",
    "CITY OF PLYMOUTH": "PLYMOUTH",
    "RHONDDA CYNON TAFF": "RHONDDA CYNON TAF",
    "ST HELENS": "ST. HELENS",
    "WREKIN": "TELFORD AND WREKIN",
    "CITY OF WESTMINSTER": "WESTMINSTER",
    "THE VALE OF GLAMORGAN": "VALE OF GLAMORGAN",
    "PETERBOROUGH": "CITY OF PETERBOROUGH",
    "NOTTINGHAM": "CITY OF NOTTINGHAM",
    "CITY OF KINGSTON UPON HULL": "KINGSTON UPON HULL, CITY OF",
    "CITY OF DERBY": "DERBY",
}

# Resolve multi-name
def detect_name_field(geojson: dict, level: str = "Local Authorities") -> str:
    """Return a column name with codes for different geo layers."""
    
    preferred = {
        "Local Authorities": ["LAD25CD"],               # District level
        "Counties":          ["CTYUA24NM"]            # County level
    }
    
    # Get possible field names for this level
    candidates = preferred.get(level, [])
    
    # Return the first in the GeoJSON properties
    for field in candidates:
        if any(field in feature.get("properties", {}) for feature in geojson.get("features", [])):
            return field
        

# Normalize name and return (apply alias if possible)
def normalize_name(x: str) -> str:
    """Upper + strip + alias replacement."""
    
    s = str(x).strip().upper()
    return ALIASES.get(s, s)


def attach_values(geojson: dict, lookup: dict, name_field: str, value_field: str = "avg_price"):
    """Attach value_field and display name to each feature based on normalized name."""
    
    values = []
    
    for feature in geojson["features"]:
        raw = feature["properties"].get(name_field, "")
        disp = str(raw).strip()
        norm = normalize_name(disp)
        val = lookup.get(norm)
        feature["properties"]["__display_name"] = disp
        feature["properties"][value_field] = float(val) if val is not None and np.isfinite(val) else None
        
        if val is not None:
            values.append(float(val))
            
    return values