import requests
from pathlib import Path

# Returns path to downloaded file
def stream_download(url: str, output_path: Path, chunk_size: int, timeout: int) -> Path:

    # Make sure the destination folder exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Define temp path for storing parts of data
    tmp_path = output_path.with_suffix(output_path.suffix + ".part")
    
    # Get HTTP request with stream=True to make sure that response is not loaded into memory
    with requests.get(url, stream=True, timeout=timeout) as r:
        # Raise HTTPError if status is not Success (200-299)
        r.raise_for_status()
        # Open the target file for write in binary
        with open(tmp_path, "wb") as f:
            # Read the response in chunks and write to disk
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
    # Replace temp with actual path
    tmp_path.replace(output_path)
    
    return output_path