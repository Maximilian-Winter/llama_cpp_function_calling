import os
from typing import List

from .function_call import FunctionCall


def format_function_names(function_calls):
    # Extract the names from each FunctionCall instance
    function_names = [capitalize_rule_name(func.name) for func in function_calls]

    # Join the names with ' | ' as separator
    formatted_names = ' | '.join(function_names)

    return formatted_names


def generate_gbnf_grammar(functions: List[FunctionCall]) -> str:
    # Generate individual function and parameter rules

    functions_formatted = format_function_names(functions)
    function_rules = []
    param_rules_list = []
    for function_call in functions:
        function_name = capitalize_rule_name(function_call.name)
        param_rules = f"{function_name}Params ::= \"{{\" ws "
        i = 0
        # Generate parameter rules
        for _, (param_name, param) in enumerate(function_call.parameters.properties.items()):
            if i > 0:
                param_rules += "\",\" ws "  # Including the comma within quotes
            param_rules += f"\"\\\"{param_name}\\\":\" ws {param.type.value}"
            i += 1

        param_rules += " ws \"}\""

        # Main function rule
        function_rule = f"{function_name} ::= \"{{\" ws \"\\\"function\\\":\" ws \"\\\"{function_call.name}\\\",\" ws \"\\\"params\\\":\" ws {function_name}Params \"}}\""
        function_rules.append(function_rule)
        param_rules_list.append(param_rules)

    return "root ::= Function\n" + "Function ::= " + functions_formatted + "\n" + "\n".join(function_rules) + "\n" + "\n".join(param_rules_list)


def capitalize_rule_name(name):
    """
    Capitalize each part of the rule name.
    """
    return ''.join(word.capitalize() for word in name.split('_'))


def generate_gbnf_rule(function_call):
    """
    Generate a GBNF grammar rule for a given FunctionCall with capitalized names and comma handling.

    :param function_call: The FunctionCall instance to generate the rule for.
    :return: A string representing the GBNF rule.
    """
    function_name = capitalize_rule_name(function_call.name)
    param_rules = f"{function_name}Params ::= \"{{\" ws "

    # Generate parameter rules
    for i, (param_name, param) in enumerate(function_call.parameters.properties.items()):
        if i > 0:
            param_rules += " \",\" ws "  # Including the comma within quotes
        param_rules += f"\"\\\"{param_name}\\\":\" ws {param.type.value}"

    param_rules += " ws \"}}\""

    # Main function rule
    function_rule = f"{function_name} ::= \"{{\" ws \"\\\"function\\\":\" ws \"\\\"{function_call.name}\\\",\" ws \"\\\"params\\\":\" ws {function_name}Params \"}}\""

    return function_rule + "\n" + param_rules


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
    documentation = "Available Functions:\n\n"
    for func in function_calls:
        # Function name and description
        documentation += f"{func.name}:\n  Description:{func.description}\n  Parameters:\n"

        # Parameters and their descriptions
        for param_name, param in func.parameters.properties.items():
            documentation += f"    {param_name} ({param.type.value}, {'required' if param.required else 'optional'}): "
            documentation += f"{param.description}\n"
            if param.enum:
                documentation += f"        Enum: {', '.join(param.enum)}\n"

        documentation += "\n"  # Add a blank line between function calls

    return documentation


def save_documentation_to_file(documentation, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(documentation)
        print(f"Documentation successfully saved to {file_path}")
    except IOError as e:
        print(f"An error occurred while saving the file: {e}")
