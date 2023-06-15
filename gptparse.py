import json
import argparse
from typing import Generator, Any

def from_parsers(parsers: list[argparse.ArgumentParser]) -> list[dict]:
    functions = []
    for parser in parsers:
        function = {}
        function["name"] = parser.prog
        function["description"] = parser.description
        function["parameters"] = {"type": "object", "properties": {}}

        for action in parser._actions:
            if action.dest == 'help': continue
            
            if action.nargs is not None:
                function["parameters"]["properties"][action.dest] = {
                    "type": "array",
                    "description": action.help,
                    "items": {
                        "type": "string",
                        "enum": [str(choice) for choice in action.choices]
                    }
                }
            
            else:
                function["parameters"]["properties"][action.dest] = {
                    "type": "string",
                    "description": action.help
                }
                if action.choices is not None:
                    function["parameters"]["properties"][action.dest]["enum"] = [str(choice) for choice in action.choices]
        
        functions.append(function)
    return functions

def get_arguments(completition: (Generator[Any | list | dict, None, None] | Any | list | dict)) -> tuple:
    prog =completition.choices[0].message['function_call']['name']
    kwargs = json.loads(completition.choices[0].message.to_dict()['function_call']['arguments'])
    return prog, kwargs
