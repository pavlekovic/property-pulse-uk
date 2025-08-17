from pathlib import Path
from unittest.mock import patch
from src.utils.geojson_utils import ensure_geojson_once as ego

# Check that ego doesn't download already downloaded file
def test_returns_state_if_already_fetched_and_exists(tmp_path):
    geojson_file = tmp_path / "example.geojson"
    geojson_file.write_text("{}")  # create dummy file
    state = {"geojson_fetched": True}

    result = ego(state, tmp_path, geojson_file, "http://fake-url", timeout=5)

    assert result == state, "Downloading already downloaded file"

# Check if state is being changed if wrongly false (file exists)
def test_updates_state_if_file_exists_but_flag_false(tmp_path):
    geojson_file = tmp_path / "example.geojson"
    geojson_file.write_text("{}")
    state = {"geojson_fetched": False}

    result = ego(state, tmp_path, geojson_file, "http://fake-url", timeout=5)

    assert result["geojson_fetched"] is True, "State is not being updated properly"


# Check if function downloads file if state "geojson_fetched" is False
@patch("src.utils.geojson_utils.fetch_ons_geojson")
def test_calls_fetch_if_file_missing(mock_fetch, tmp_path):
    geojson_file = tmp_path / "example.geojson"
    state = {"geojson_fetched": False}

    result = ego(state, tmp_path, geojson_file, "http://fake-url", timeout=5)

    mock_fetch.assert_called_once()
    assert result["geojson_fetched"] is True, "File not downloaded despite 'geojson_fetched' = False"


# Check if directory is being created if non-existant
@patch("src.utils.geojson_utils.fetch_ons_geojson")
def test_creates_directory_if_missing(mock_fetch, tmp_path):
    mapping_dir = tmp_path / "nested" / "mapping"
    geojson_file = mapping_dir / "map.geojson"
    state = {}

    ego(state, mapping_dir, geojson_file, "http://fake-url", timeout=5)

    assert mapping_dir.exists(), "Directory for geojson not created successfully"