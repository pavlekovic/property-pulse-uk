from pathlib import Path                 
from unittest.mock import patch, MagicMock # Testing tools
import pytest
from requests import HTTPError
from src.etl.extract.fetch_data import stream_download


# Test whether get request checks for response status code
@patch("src.etl.extract.fetch_data.requests.get")
def test_fetch_data_http_error_raises(mock_get, tmp_path):
    
    # --- Arrange ---
    # Build a fake HTTP response
    mock_response = MagicMock()
    mock_response.iter_content.return_value = [b"data"]     # Pretend downloaded file contains one chunk "data"
    mock_response.raise_for_status.return_value = None      # Pretend server returned status 200 (OK)
    mock_response.__enter__.return_value = mock_response    # Makes the mock object work with "with requests.get() as r"
    mock_get.return_value = mock_response                   # Makes mock_get return a fake HTTP response (mock_response)
    # Provide a fake file path inside a temporary folder
    out = tmp_path / "test.csv"
    
    # --- Act ---
    stream_download(
        url="http://example.com/file.csv",
        output_path=out,
        chunk_size=1024,
        timeout=5)

    # -- Assert --
    mock_response.raise_for_status.assert_called_once(), "Response status not checked correctly."


# Test whether error is raised in case of bad status
@patch("src.etl.extract.fetch_data.requests.get")
def test_fetch_data_http_ok_calls_raise_for_status(mock_get, tmp_path):
    
    # --- Arrange ---
    # Build a fake HTTP response
    mock_response = MagicMock()
    mock_response.iter_content.return_value = []                        # Pretend downloaded file is empty
    mock_response.raise_for_status.side_effect = HTTPError("boom")      # Pretend server returned bad status
    mock_response.__enter__.return_value = mock_response                # Makes the mock object work with "with requests.get() as r"
    mock_get.return_value = mock_response                               # Makes mock_get return a fake HTTP response (mock_response)
    # Provide a fake file path inside a temporary folder
    out = tmp_path / "test.csv"
    
    # --- Act ---
    with pytest.raises(HTTPError):
        stream_download(
        url="http://example.com/file.csv",
        output_path=out,
        chunk_size=1024,
        timeout=5)

    # -- Assert --
    assert not out.exists() # Pytest handles error message


# Test whether stream_download returns a path
@patch("src.etl.extract.fetch_data.requests.get")
def test_fetch_data_return_type(mock_get, tmp_path):
# Parameters: mock_get -> fake get response object
#             tmp_path -> temporary folder for this test that will be cleaned after

    # --- Arrange ---
    # Build a fake HTTP response
    mock_response = MagicMock()
    mock_response.iter_content.return_value = [b"data"]     # Pretend downloaded file contains one chunk "data"
    mock_response.raise_for_status.return_value = None      # Pretend server returned status 200 (OK)
    mock_response.__enter__.return_value = mock_response    # Makes the mock object work with "with requests.get() as r"
    mock_get.return_value = mock_response                   # Makes mock_get return a fake HTTP response (mock_response)
    
    # Provide a fake file path inside a temporary folder
    out = tmp_path / "test.csv"
    
    # --- Act ---
    result = stream_download(
        url="http://example.com/file.csv",
        output_path=out,
        chunk_size=1024,
        timeout=5)

    # -- Assert --
    assert isinstance(result, Path), "Return object is not a Path"


# Test whether writing from fetched to local works
@patch("src.etl.extract.fetch_data.requests.get")
def test_fetch_data_file_written (mock_get, tmp_path):
# Parameters: mock_get -> fake get response object
#             tmp_path -> temporary folder for this test that will be cleaned after

    # --- Arrange ---
    # Build a fake HTTP response
    mock_response = MagicMock()
    mock_response.iter_content.return_value = [b"example ", b"data ", b"being ", b"written"]     # Pretend downloaded file contains one chunk "data"
    mock_response.raise_for_status.return_value = None      # Pretend server returned status 200 (OK)
    mock_response.__enter__.return_value = mock_response    # Makes the mock object work with "with requests.get() as r"
    mock_get.return_value = mock_response                   # Makes mock_get return a fake HTTP response (mock_response)
    
    # Provide a fake file path inside a temporary folder
    out = tmp_path / "written.csv"
    
    # --- Act ---
    result = stream_download(
        url="http://example.com/file.csv",
        output_path=out,
        chunk_size=1024,
        timeout=5)

    # -- Assert --
    assert result.exists(), "File was not created locally"
    with open(result, "rb") as f:
        content = f.read()
    assert content == b"example data being written", "File content does not match expected data"