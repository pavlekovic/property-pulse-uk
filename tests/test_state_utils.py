from pathlib import Path
import json
import pytest
from src.utils.state_utils import read_state, write_state, DEFAULT_STATE

# Test whether write and read work successfully
def test_write_then_read_back_round_trip(tmp_path: Path):
    state_file = tmp_path / "_state.json"
    original = {
        "full_import_done": True,
        "last_month_fetched": "2025-07",
        "geojson_fetched": True,
    }

    write_state(state_file, original)
    loaded = read_state(state_file)

    assert loaded == original


# Check if parent directory is being created in case it's missing
def test_write_creates_parent_directories(tmp_path: Path):
    state_file = tmp_path / "nested" / "deeper" / "_state.json"
    payload = {"full_import_done": False, 
               "last_month_fetched": None, 
               "geojson_fetched": False}

    assert not state_file.parent.exists()
    write_state(state_file, payload)

    assert state_file.parent.exists()
    assert read_state(state_file) == payload

# Check that write_state writes to part first before replacing
def test_atomic_write_uses_part_file(tmp_path: Path):
    state_file = tmp_path / "_state.json"
    tmp_part = state_file.with_suffix(state_file.suffix + ".part")
    payload = {"full_import_done": True, 
               "last_month_fetched": "2025-08", 
               "geojson_fetched": True}

    write_state(state_file, payload)

    # Final file exists with correct content
    assert state_file.exists()
    assert read_state(state_file) == payload

    # Temp part should be gone after replace
    assert not tmp_part.exists()


# Check if state file is corrupted
def test_read_state_corrupted_file_returns_default(tmp_path: Path):
    state_file = tmp_path / "_state.json"
    state_file.write_text("{ not valid json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        read_state(state_file)


# Check that DEFAULT_STATE is unchanged after reading from state and changing dict value
def test_modifying_returned_state_does_not_mutate_default(tmp_path: Path):
    state_file = tmp_path / "_state.json"

    # First run -> copy of DEFAULT_STATE
    s = read_state(state_file)
    s["full_import_done"] = True

    # DEFAULT_STATE must remain unchanged
    assert DEFAULT_STATE["full_import_done"] is False