import json
import logging
from typing import Callable, Dict, Any


class LLMFunctionCaller:
    def __init__(self):
        self.function_map: Dict[str, Callable] = {}
        self.param_transformers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}
        logging.basicConfig(level=logging.INFO)

    def add_function(self, name: str, function: Callable) -> None:
        self.function_map[name] = function

    def add_param_transformer(self, function_name: str,
                              transformer: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
        self.param_transformers[function_name] = transformer

    def execute_function(self, json_input: str) -> Any:
        try:
            data: Dict[str, Any] = json.loads(json_input)
            func_name: str = data["function"]
            params: Dict[str, Any] = data["params"]

            if func_name not in self.function_map:
                raise ValueError("Function not defined")

            # Apply parameter transformation if available
            if func_name in self.param_transformers:
                params = self.param_transformers[func_name](params)

            return self.function_map[func_name](**params)

        except Exception as e:
            logging.error(f"Error executing function: {e}")
            raise e
