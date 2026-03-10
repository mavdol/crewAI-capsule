import pytest
from crewai_capsule import CapsulePythonREPLTool, CapsuleJSREPLTool


# ---- Python : Basic tests ----
@pytest.mark.asyncio
async def test_python_basic_async():
    result = await CapsulePythonREPLTool()._arun("1 + 1")
    assert str(result).strip() == "2"

def test_python_basic_sync():
    result = CapsulePythonREPLTool()._run("2 + 2")
    assert str(result).strip() == "4"


# ---- Python : Multi-line & variables test ----
@pytest.mark.asyncio
async def test_python_multiline():
    code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

factorial(6)
"""
    result = await CapsulePythonREPLTool()._arun(code)
    assert str(result).strip() == "720"

@pytest.mark.asyncio
async def test_python_variables():
    code = """
x = 10
y = 32
x + y
"""
    result = await CapsulePythonREPLTool()._arun(code)
    assert str(result).strip() == "42"

@pytest.mark.asyncio
async def test_python_list_comprehension():
    code = "[i ** 2 for i in range(5)]"
    result = await CapsulePythonREPLTool()._arun(code)
    assert str(result).strip() == "[0, 1, 4, 9, 16]"

@pytest.mark.asyncio
async def test_python_stdlib():
    code = """
import json
data = {"hello": "world", "number": 42}
json.dumps(data)
"""
    result = await CapsulePythonREPLTool()._arun(code)
    assert '"hello"' in result
    assert '"world"' in result

@pytest.mark.asyncio
async def test_python_print_output():
    code = """
print("Hello")
print("World")
print("Test")
42
"""
    result = await CapsulePythonREPLTool()._arun(code)
    assert "Hello" in result
    assert "World" in result
    assert "Test" in result
    assert "42" in result


# ---- Python : Errors test ----
@pytest.mark.asyncio
async def test_python_syntax_error():
    result = await CapsulePythonREPLTool()._arun("def broken(")
    assert "was never closed" in result

@pytest.mark.asyncio
async def test_python_runtime_error():
    result = await CapsulePythonREPLTool()._arun("1 / 0")
    assert "division by zero" in result

@pytest.mark.asyncio
async def test_python_name_error():
    result = await CapsulePythonREPLTool()._arun("undefined_variable")
    assert "undefined_variable" in result


# ---- Python : error returns string ----
def test_python_error_returns_string():
    tool = CapsulePythonREPLTool()
    result = tool._run("1 / 0")
    assert isinstance(result, str)
    assert len(result) > 0


# ---- JavaScript : Basic tests ----
@pytest.mark.asyncio
async def test_js_basic_async():
    result = await CapsuleJSREPLTool()._arun("1 + 2")
    assert str(result).strip() == "3"

def test_js_basic_sync():
    result = CapsuleJSREPLTool()._run("3 + 3")
    assert str(result).strip() == "6"


# ---- JavaScript : Multi-line & variables test ----
@pytest.mark.asyncio
async def test_js_multiline():
    code = """
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
factorial(6)
"""
    result = await CapsuleJSREPLTool()._arun(code)
    assert str(result).strip() == "720"

@pytest.mark.asyncio
async def test_js_variables():
    code = """
const x = 10;
const y = 32;
x + y
"""
    result = await CapsuleJSREPLTool()._arun(code)
    assert str(result).strip() == "42"

@pytest.mark.asyncio
async def test_js_array_operations():
    code = "[1, 2, 3, 4, 5].map(x => x ** 2)"
    result = await CapsuleJSREPLTool()._arun(code)
    assert str(result).strip() == "[1, 4, 9, 16, 25]"

@pytest.mark.asyncio
async def test_js_object():
    code = """
const data = { hello: "world", number: 42 };
JSON.stringify(data)
"""
    result = await CapsuleJSREPLTool()._arun(code)
    assert "hello" in result
    assert "world" in result

@pytest.mark.asyncio
async def test_js_console_output():
    code = """
console.log("Hello");
console.log("World");
console.log("Test");
42
"""
    result = await CapsuleJSREPLTool()._arun(code)
    assert "Hello" in result
    assert "World" in result
    assert "Test" in result
    assert "42" in result


# ---- JavaScript : Errors test ----
@pytest.mark.asyncio
async def test_js_syntax_error():
    result = await CapsuleJSREPLTool()._arun("function broken(")
    assert "missing formal parameter" in result

@pytest.mark.asyncio
async def test_js_runtime_error():
    result = await CapsuleJSREPLTool()._arun("null.property")
    assert "null" in result

@pytest.mark.asyncio
async def test_js_reference_error():
    result = await CapsuleJSREPLTool()._arun("undefinedVariable")
    assert "undefinedVariable" in result


# ---- JavaScript : error returns string ----
def test_js_error_returns_string():
    tool = CapsuleJSREPLTool()
    result = tool._run("null.property")
    assert isinstance(result, str)
    assert len(result) > 0
