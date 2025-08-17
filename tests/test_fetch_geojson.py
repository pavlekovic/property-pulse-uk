from pathlib import Path                 
from unittest.mock import patch, MagicMock # Testing tools
import pytest
from requests import HTTPError
from src.etl.extract.fetch_geojson import fetch_ons_geojson

# Check whether fetch_geojson returns a path
@patch("src.etl.extract.fetch_geojson.requests.get")
def test_fetch_geojson_return_type(mock_get, tmp_path):
    
    # --- Arrange ---
    # Build a fake HTTP response
    mock_response = MagicMock()
    mock_response.content = b'{"type":"FeatureCollection","features":[]}'    # Pretend downloaded file contains one chunk "data"
    mock_response.raise_for_status.return_value = None                       # Pretend server returned status 200 (OK)
    mock_get.return_value = mock_response                                    # Makes mock_get return a fake HTTP response (mock_response)
    
    # Provide a fake file path inside a temporary folder
    out = tmp_path / "test.geojson"
    
    # --- Act ---
    result = fetch_ons_geojson(
        query_url = "http://apiexample.com/query",
        output_path = out,
        timeout = 5
    )

    # -- Assert --
    assert isinstance(result, Path), "Return object is not a Path"
    
    
# Test whether error is raised in case of bad status
@patch("src.etl.extract.fetch_geojson.requests.get")
def test_fetch_geojson_http_ok_calls_raise_for_status(mock_get, tmp_path):

    # --- Arrange ---
    # Build a fake HTTP response
    mock_response = MagicMock()
    mock_response.content = ""                                                           # Pretend response is empty
    mock_response.raise_for_status.side_effect = HTTPError("boom")                       # Pretend server returned bad status
    mock_get.return_value = mock_response                                                # Makes mock_get return a fake HTTP response (mock_response)
    
    # Provide a fake file path inside a temporary folder
    out = tmp_path / "test.geojson"
    
    # --- Act ---
    with pytest.raises(HTTPError):
        fetch_ons_geojson(
        query_url = "http://apiexample.com/query",
        output_path = out,
        timeout = 5
    )

    # -- Assert --
    assert not out.exists() # Pytest handles error message


# Test whether get request checks for response status code
@patch("src.etl.extract.fetch_geojson.requests.get")
def test_fetch_geojson_http_error_raises(mock_get, tmp_path):
    
    # --- Arrange ---
   # Build a fake HTTP response
    mock_response = MagicMock()
    mock_response.content = b'{"type":"FeatureCollection","features":[]}'    # Pretend downloaded file contains some data
    mock_response.raise_for_status.return_value = None                       # Pretend server returned status 200 (OK)
    mock_get.return_value = mock_response                                    # Makes mock_get return a fake HTTP response (mock_response)
    
    # Provide a fake file path inside a temporary folder
    out = tmp_path / "test.geojson"
    
    # --- Act ---
    result = fetch_ons_geojson(
        query_url = "http://apiexample.com/query",
        output_path = out,
        timeout = 5
    )

    # -- Assert --
    mock_response.raise_for_status.assert_called_once(), "Response status not checked correctly."


# Test whether writing from fetched to local works
@patch("src.etl.extract.fetch_geojson.requests.get")
def test_fetch_geojson_file_written (mock_get, tmp_path):
# Parameters: mock_get -> fake get response object
#             tmp_path -> temporary folder for this test that will be cleaned after

    # --- Arrange ---
    # Build a fake HTTP response
    mock_response = MagicMock()
    mock_response.content = b'{"type":"FeatureCollection","features":[]}'    # Pretend downloaded file contains some data
    mock_response.raise_for_status.return_value = None                                           # Pretend server returned status 200 (OK)
    mock_get.return_value = mock_response                                                        # Makes mock_get return a fake HTTP response (mock_response)
    
    # Provide a fake file path inside a temporary folder
    out = tmp_path / "test.geojson"
    
    # --- Act ---
    result = fetch_ons_geojson(
        query_url = "http://apiexample.com/query",
        output_path = out,
        timeout = 5
    )

    # -- Assert --
    assert result.exists(), "File was not created locally"
    assert result.read_bytes() == mock_response.content, "File content does not match HTTP content"