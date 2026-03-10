import pytest
from unittest.mock import patch, AsyncMock

from crewai_capsule.tools import (
    CapsulePythonREPLTool,
    CapsuleJSREPLTool,
    _invoke_sandbox,
    _parse_capsule_error,
)


@pytest.fixture
def run_mock():
    with patch("crewai_capsule.tools.run", new_callable=AsyncMock) as mock:
        yield mock


# ── _parse_capsule_error ─────────────────────────────────────────────

def test_parse_error_dict_with_message():
    assert _parse_capsule_error({"message": "bad input", "error_type": "ValueError"}) == "bad input"

def test_parse_error_dict_with_only_error_type():
    assert _parse_capsule_error({"error_type": "RuntimeError"}) == "RuntimeError"

def test_parse_error_dict_empty():
    result = _parse_capsule_error({})
    assert isinstance(result, str)

def test_parse_error_plain_string():
    assert _parse_capsule_error("something went wrong") == "something went wrong"


# ── _invoke_sandbox ──────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_invoke_sandbox_success(run_mock):
    run_mock.return_value = {"success": True, "result": "2", "error": None}

    result = await _invoke_sandbox("any.wasm", "execute_code", "1+1")

    assert result == "2"
    run_mock.assert_called_once_with(file="any.wasm", args=["execute_code", "1+1"])


@pytest.mark.asyncio
async def test_invoke_sandbox_error_raises(run_mock):
    run_mock.return_value = {
        "success": False,
        "result": None,
        "error": {"error_type": "SyntaxError", "message": "invalid syntax"},
    }

    with pytest.raises(Exception, match="invalid syntax"):
        await _invoke_sandbox("any.wasm", "execute_code", "bad code")


# ── Tool wiring ──────────────────────────────────────────────────────

@pytest.mark.asyncio
@patch("crewai_capsule.tools.resources.path")
async def test_python_tool_uses_correct_wasm(mock_path, run_mock):
    run_mock.return_value = {"success": True, "result": "x", "error": None}
    mock_path.return_value.__enter__.return_value = "/fake/sandbox_py.wasm"

    result = await CapsulePythonREPLTool()._arun("x")

    run_mock.assert_called_once_with(file="/fake/sandbox_py.wasm", args=["execute_code", "x"])
    assert result == "x"


@pytest.mark.asyncio
@patch("crewai_capsule.tools.resources.path")
async def test_js_tool_uses_correct_wasm(mock_path, run_mock):
    run_mock.return_value = {"success": True, "result": "x", "error": None}
    mock_path.return_value.__enter__.return_value = "/fake/sandbox_js.wasm"

    result = await CapsuleJSREPLTool()._arun("x")

    run_mock.assert_called_once_with(file="/fake/sandbox_js.wasm", args=["execute_code", "x"])
    assert result == "x"


# ── Sync wrapper ─────────────────────────────────────────────────────

@patch("crewai_capsule.tools.resources.path")
def test_sync_run_delegates_to_async(mock_path, run_mock):
    run_mock.return_value = {"success": True, "result": "2", "error": None}
    mock_path.return_value.__enter__.return_value = "/fake/sandbox_py.wasm"

    result = CapsulePythonREPLTool()._run("1+1")

    assert result == "2"


# ── Error handling returns string (not raise) ────────────────────────

@patch("crewai_capsule.tools.resources.path")
def test_python_tool_error_returns_string(mock_path, run_mock):
    run_mock.return_value = {
        "success": False,
        "result": None,
        "error": {"message": "division by zero"},
    }
    mock_path.return_value.__enter__.return_value = "/fake/sandbox_py.wasm"

    result = CapsulePythonREPLTool()._run("1 / 0")

    assert "division by zero" in result
    assert result.startswith("Error:")
