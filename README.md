# crewAI-capsule
CrewAI integration for Capsule — `crewai-capsule` gives CrewAI agents the ability to safely execute tasks in an isolated WebAssembly sandbox. No configuration or network request is necessary to execute the sandboxed tasks.

## Installation

```bash
pip install crewai-capsule
```

## Usage

The package provides tools for executing code inside an isolated environment.

```python
import asyncio
from crewai_capsule import CapsulePythonREPLTool, CapsuleJSREPLTool

# Python Example
python_tool = CapsulePythonREPLTool()
result = python_tool.run("1 + 1")
print(result) # "2"

# JavaScript Example
js_tool = CapsuleJSREPLTool()
result = asyncio.run(js_tool.arun("1 + 2"))
print(result) # "3"
```

## More information

Visit [Capsule](https://github.com/mavdol/capsule) repository for more information.

## License

MIT License
