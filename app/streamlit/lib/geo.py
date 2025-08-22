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

def detect_name_field(geojson: dict, level: str = "Local Authorities") -> str:
    """Pick a suitable name property from GeoJSON features."""
    
    props0 = geojson["features"][0]["properties"]
    preferred = {
        "Local Authorities": ["LAD25NM", "LAD24NM", "LAD23NM", "LAD22NM","LTLA23NM", "LTLA22NM",
            "NAME", "Name", "lad_name", "name"],
        "Counties":          ["CTYUA24NM"]
    }
    
    # Try all known candidates for the requested level
    for k in preferred.get(level, []):
        if k in props0:
            return k
    
    for k in preferred.get(level, []):
        if k in props0:
            return k

    return list(props0.keys())[0]

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