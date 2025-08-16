from pathlib import Path
from src.utils.date_utils import last_month_ym


def resolve_url_and_out_path (
    full_done: bool,
    raw_dir: Path,
    full_url: str,
    monthly_url: str,
    full_filename: str,
    monthly_filename: str,
):
    # If the state is DEFAULT_STATE (full_done = False)
    if not full_done:
        # First run
        fetch_url = full_url
        out_path = raw_dir / full_filename
    else:
        # Monthly update run
        ym = last_month_ym()
        fetch_url = monthly_url
        out_path = raw_dir / ym / monthly_filename
    
    return fetch_url, out_path