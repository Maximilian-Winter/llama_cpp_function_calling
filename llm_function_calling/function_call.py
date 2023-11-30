from typing import Optional, Dict, List


class FunctionParameter:
    def __init__(self, parameter_type: str, required: bool, description: Optional[str] = None,
                 enum: Optional[List[str]] = None):
        self.type = parameter_type
        self.required = required
        self.description = description
        self.enum = enum


class FunctionParameters:
    def __init__(self, properties: Dict[str, FunctionParameter]):
        self.properties = properties


class FunctionCall:
    def __init__(self, name: str, parameters: FunctionParameters):
        self.name = name
        self.parameters = parameters

