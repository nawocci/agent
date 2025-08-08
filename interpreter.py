import re
import inspect
import ast
from typing import Dict, Any, Callable
import commands


class CommandInterpreter:
    def __init__(self):
        self.commands = self._discover_commands()
    
    def _discover_commands(self) -> Dict[str, Callable]:
        cmd_dict = {}
        for name, func in inspect.getmembers(commands, inspect.isfunction):
            if not name.startswith('_'):
                cmd_dict[name] = func
        return cmd_dict
    
    def execute_commands(self, text: str, max_commands: int = 5) -> str:
        cmd_pattern = re.compile(r'COMMAND:\s*(\w+)\(([^)]*)\)')
        fence_pattern = re.compile(r"```.*?```", re.DOTALL)

        def replace_in_segment(segment: str) -> str:
            count = 0

            def _replace(match: re.Match) -> str:
                nonlocal count
                if count >= max_commands:
                    return match.group(0)
                command_name = match.group(1)
                params_str = match.group(2).strip()

                if command_name not in self.commands:
                    return f"[ERROR: Unknown command '{command_name}']"

                try:
                    params = self._parse_parameters(params_str)
                    result = self.commands[command_name](**params)
                    count += 1
                    return str(result)
                except Exception as e:
                    return f"[ERROR: {command_name}() failed - {str(e)}]"

            return cmd_pattern.sub(_replace, segment)

        # Split text by code fences and only process non-code parts
        result_parts = []
        last = 0
        for m in fence_pattern.finditer(text):
            non_code = text[last:m.start()]
            result_parts.append(replace_in_segment(non_code))
            result_parts.append(m.group(0))  # Keep code block unchanged
            last = m.end()
        result_parts.append(replace_in_segment(text[last:]))

        return "".join(result_parts)
    
    def _parse_parameters(self, params_str: str) -> Dict[str, Any]:
        if not params_str.strip():
            return {}

        try:
            fake_call = f"f({params_str})"
            node = ast.parse(fake_call, mode="eval")
            if not isinstance(node.body, ast.Call):
                raise ValueError("Invalid parameter format")
            params: Dict[str, Any] = {}
            for kw in node.body.keywords:
                if kw.arg is None:
                    raise ValueError("Only keyword arguments are supported")
                params[kw.arg] = ast.literal_eval(kw.value)
            return params
        except Exception as e:
            raise ValueError(f"Invalid parameters: {e}")
    
    def add_command(self, name: str, func: Callable) -> None:
        self.commands[name] = func
    
    def get_available_commands(self) -> list:
        return list(self.commands.keys())
    
    def get_system_prompt(self) -> str:
        # Keep prompt compact: list signatures and one-line docs
        lines = []
        for name, func in self.commands.items():
            sig = inspect.signature(func)
            doc = (func.__doc__ or "").strip().splitlines()[0] if func.__doc__ else ""
            line = f"- {name}{sig}" + (f" — {doc}" if doc else "")
            lines.append(line)
        functions_list = "\n".join(lines) if lines else "- (no commands available)"

        return f"""You may optionally invoke local functions using this exact format:
Format: COMMAND: function_name(param=value[, ...])

Available functions:
{functions_list}

Guidance:
- Use commands only when local/real-time data is required
- Do not place commands inside code blocks
- Otherwise, reply normally without commands

Examples:
- "What time is it?" → "The current time is COMMAND: get_time()"
- "What's 2+2?" → "2+2 equals 4"
"""
