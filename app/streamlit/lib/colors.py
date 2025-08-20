import numpy as np

def color_scale_quantiles(values, n_bins: int = 6):
    """Compute quantile breakpoints and a simple light→dark blue palette."""
    # Keep only real numbers (drop None, NaN, ±inf)
    vals = [float(v) for v in values if v is not None and np.isfinite(v)]

    # If no valid values, return a trivial scale
    if not vals:
        return [0, 1], [(200, 200, 200, 60)]

    # Quantile breakpoints: e.g., with n_bins=6 → 0%, 16.7%, …, 100%
    edges = list(np.quantile(vals, np.linspace(0, 1, n_bins + 1)))

    # A 6-step blue palette (light → dark) with semi-transparency
    palette = [
        (239, 243, 255), (198, 219, 239), (158, 202, 225),
        (107, 174, 214), (49, 130, 189), (8, 81, 156),
    ]
    colors = [(r, g, b, 190) for (r, g, b) in palette]

    return edges, colors


def assign_colors_quantiled(geojson: dict, value_field: str, edges, colors):
    """Assign each feature a color based on which quantile bin its value falls in."""
    for feat in geojson["features"]:
        v = feat["properties"].get(value_field)

        # Missing/invalid values → light grey
        if v is None or not np.isfinite(v):
            feat["properties"]["fill_rgba"] = [200, 200, 200, 60]
            continue

        # Default to darkest color; then find the matching bin
        chosen = colors[-1]
        for i in range(len(edges) - 1):
            if edges[i] <= v <= edges[i + 1]:
                chosen = colors[i]
                break

        # Write RGBA color into feature properties (used by PyDeck)
        feat["properties"]["fill_rgba"] = list(chosen)