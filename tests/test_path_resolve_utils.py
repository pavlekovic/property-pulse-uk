from pathlib import Path
from src.utils.date_utils import last_month_ym
from src.utils.path_resolve_utils import resolve_url_and_out_path

# Check that if full_done is False, full csv is downloaded
def test_first_run_returns_full_url_and_path(tmp_path: Path):
    full_url = "http://example.com/full.csv"
    monthly_url = "http://example.com/monthly.csv"
    fetch_url, out_path = resolve_url_and_out_path(
        full_done=False,
        raw_dir=tmp_path,
        full_url=full_url,
        monthly_url=monthly_url,
        full_filename="full.csv",
        monthly_filename="monthly.csv",
    )

    assert fetch_url == full_url
    assert out_path == tmp_path / "full.csv"


# Check that if full_done is True, monthly csv is downloaded
def test_monthly_run_returns_monthly_url_and_nested_path(tmp_path: Path):
    monthly_url = "http://example.com/monthly.csv"
    ym = last_month_ym()
    fetch_url, out_path = resolve_url_and_out_path(
        full_done=True,
        raw_dir=tmp_path,
        full_url="http://example.com/full.csv",
        monthly_url=monthly_url,
        full_filename="full.csv",
        monthly_filename="monthly.csv",
    )

    assert fetch_url == monthly_url
    assert out_path == tmp_path / ym / "monthly.csv"