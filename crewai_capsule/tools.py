"""
Capsule integration for CrewAI.
"""

import asyncio
from importlib import resources
from typing import Any, Type

from capsule import run
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


def _get_wasm(filename: str) -> str:
    """Resolve the path to a .wasm file bundled inside this package."""
    with resources.path("crewai_capsule.sandboxes", filename) as path:
        return str(path)


def _parse_capsule_error(error: Any) -> str:
    """Extract a human-readable message from a Capsule error payload."""
    if isinstance(error, dict):
        return error.get("message") or error.get("error_type") or str(error)
    return str(error)


async def _invoke_sandbox(wasm_file: str, action: str, arg: str) -> str:
    """Call the Capsule sandbox and return the result value only."""
    res = await run(file=wasm_file, args=[action, arg])

    if res.get("success"):
        return str(res.get("result", ""))

    raise Exception(_parse_capsule_error(res.get("error")))


class _CodeInput(BaseModel):
    code: str = Field(..., description="The code to execute in the sandbox.")


class CapsulePythonREPLTool(BaseTool):
    """Execute Python code inside an isolated Capsule WebAssembly sandbox."""

    name: str = "python_repl"
    description: str = (
        "Execute Python code in a secure isolated WebAssembly sandbox. "
        "Both standard output (print statements) and the last evaluated expression are returned. "
        "Supports pure Python only (no C extensions like numpy/pandas)."
    )
    args_schema: Type[BaseModel] = _CodeInput

    def _run(self, code: str) -> str:
        try:
            return asyncio.run(_invoke_sandbox(_get_wasm("sandbox_py.wasm"), "execute_code", code))
        except Exception as e:
            return f"Error: {e}"

    async def _arun(self, code: str) -> str:
        try:
            return await _invoke_sandbox(_get_wasm("sandbox_py.wasm"), "execute_code", code)
        except Exception as e:
            return f"Error: {e}"


class CapsuleJSREPLTool(BaseTool):
    """Execute JavaScript code inside an isolated Capsule WebAssembly sandbox."""

    name: str = "javascript_repl"
    description: str = (
        "Execute JavaScript code in a secure isolated WebAssembly sandbox. "
        "Both standard output (console logs) and the last evaluated expression are returned."
    )
    args_schema: Type[BaseModel] = _CodeInput

    def _run(self, code: str) -> str:
        try:
            return asyncio.run(_invoke_sandbox(_get_wasm("sandbox_js.wasm"), "execute_code", code))
        except Exception as e:
            return f"Error: {e}"

    async def _arun(self, code: str) -> str:
        try:
            return await _invoke_sandbox(_get_wasm("sandbox_js.wasm"), "execute_code", code)
        except Exception as e:
            return f"Error: {e}"
