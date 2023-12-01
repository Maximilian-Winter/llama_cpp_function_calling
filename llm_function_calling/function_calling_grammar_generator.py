import os
from typing import List, Dict

from .function_call import FunctionCall, DataType, FunctionParameter


def format_function_names(function_calls):
    # Extract the names from each FunctionCall instance
    function_names = [capitalize_rule_name(func.name) for func in function_calls]

    # Join the names with ' | ' as separator
    formatted_names = ' | '.join(function_names)

    return formatted_names


def generate_object_rule(name: str, structure: Dict[str, FunctionParameter]) -> str:
    """
    Generate GBNF rules for an object with given structure.
    """
    rules = [f"{name} ::= \"{{\" ws "]
    for i, (field, param) in enumerate(structure.items()):
        if i > 0:
            rules.append("\",\" ws ")
        rules.append(f"\"\\\"{field}\\\":\" ws {param.type.value}")
    rules.append(" ws \"}\"")
    return ''.join(rules)


def generate_array_rule(name: str, element_type: FunctionParameter) -> str:
    """
    Generate GBNF rules for an array of a specific type.
    """
    return f"{name} ::= \"[\" ws ({element_type.type.value} (\",\" ws {element_type.type.value})*)? ws \"]\""


def generate_gbnf_rule(function_call):
    """
    Generate a GBNF grammar rule for a given FunctionCall with capitalized names and comma handling,
    including support for OBJECT and ARRAY data types.
    """

    # Capitalize and format the function name
    function_name = capitalize_rule_name(function_call.name)

    # Start the main function rule
    function_rule = f"{function_name} ::= \"{{\" ws \"\\\"function\\\":\" ws \"\\\"{function_call.name}\\\",\" ws \"\\\"params\\\":\" ws {function_name}Params \"}}\""

    # Initialize parameter rules
    param_rules = f"{function_name}Params ::= \"{{\" ws "

    # Iterate over parameters and generate rules
    for i, (param_name, param) in enumerate(function_call.parameters.properties.items()):
        if i > 0:
            param_rules += "\",\" ws "  # Include a comma separator for multiple parameters

        # Handling different data types
        if param.type in [DataType.OBJECT, DataType.ARRAY]:
            # Generate a specific rule for OBJECT or ARRAY type
            nested_rule_name = f"{function_name}{param_name.capitalize()}"
            param_rules += f"\"\\\"{param_name}\\\":\" ws {nested_rule_name} "

            if param.type == DataType.OBJECT:
                object_rule = generate_object_rule(nested_rule_name, param.structure)
                param_rules += "\n" + object_rule
            elif param.type == DataType.ARRAY:
                array_rule = generate_array_rule(nested_rule_name, param.element_type)
                param_rules += "\n" + array_rule
        else:
            # Handle basic data types
            param_rules += f"\"\\\"{param_name}\\\":\" ws {param.type.value}"

    # Close the parameter rules
    param_rules += " ws \"}}\""

    return function_rule, param_rules


def generate_gbnf_grammar(function_calls: List[FunctionCall]) -> str:
    """
    Generate a complete GBNF grammar from a list of FunctionCall instances,
    placing all function rules first followed by all parameter rules.
    """
    # Start with the root rule
    root_rule = "root ::= " + format_function_names(function_calls)

    # Initialize lists to store function rules and parameter rules separately
    function_rules = [root_rule]
    param_rules = []

    # Iterate over each FunctionCall and generate corresponding GBNF rules
    for function_call in function_calls:
        function_rule, param_rule = generate_gbnf_rule(function_call)

        # Append the generated rules to their respective lists
        function_rules.append(function_rule)
        param_rules.append(param_rule)

    # Combine function rules and parameter rules into a single grammar string
    complete_grammar = "\n".join(function_rules + param_rules)

    return complete_grammar


def capitalize_rule_name(name):
    """
    Capitalize each part of the rule name.
    """
    return ''.join(word.capitalize() for word in name.split('_'))


def save_grammar_to_file(grammar_str, file_path):
    try:
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        with open(f"{script_dir}/primitive.gbnf", 'r', encoding='utf-8') as file:
            primary_grammar = file.read()
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(grammar_str + "\n" + primary_grammar)
        print(f"Grammar successfully saved to {file_path}")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")


def generate_documentation(function_calls):
    """
    Generate documentation for a list of FunctionCall instances, including details of objects and arrays.
    """

    def document_parameter(param_name, param, indent_level):
        """
        Recursively document a parameter, handling objects and arrays.
        """
        indent = "  " * indent_level
        doc = f"{indent}{param_name} ({param.type.value}, {'required' if param.required else 'optional'}): {param.description}\n"

        if param.type == DataType.OBJECT and param.structure:
            doc += f"{indent}  Structure:\n"
            for sub_param_name, sub_param in param.structure.items():
                doc += document_parameter(sub_param_name, sub_param, indent_level + 2)

        elif param.type == DataType.ARRAY and param.element_type:
            doc += f"{indent}  Element Type:\n"
            doc += document_parameter("item", param.element_type, indent_level + 2)

        return doc

    documentation = "Available Functions:\n\n"
    for func in function_calls:
        # Function name and description
        documentation += f"{func.name}:\n  Description: {func.description}\n  Parameters:\n"

        # Parameters and their descriptions
        for param_name, param in func.parameters.properties.items():
            documentation += document_parameter(param_name, param, 2)

        documentation += "\n"  # Add a blank line between function calls

    return documentation


def save_documentation_to_file(documentation, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(documentation)
        print(f"Documentation successfully saved to {file_path}")
    except IOError as e:
        print(f"An error occurred while saving the file: {e}")
