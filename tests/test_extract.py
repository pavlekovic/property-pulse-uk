import types
import src.etl.extract.extract as ex

# Test if extract is callable function
def test_extract_is_callable():
    """extract() should be a function you can call."""
    assert isinstance(ex.extract, types.FunctionType)

# Test if return is int
def test_extract_returns_int():
    """extract() should always return an int exit code."""
    result = ex.extract()
    assert isinstance(result, int)

# Check return options
def test_extract_returns_0_or_1():
    """extract() should only return 0 (success) or 1 (failure)."""
    result = ex.extract()
    assert result in [0, 1]