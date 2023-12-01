import os
from typing import List, Dict

from .function_call import FunctionCall, DataType, FunctionParameter


def format_function_names(function_calls):
    # Extract the names from each FunctionCall instance
    function_names = [format_rule_name(func.name) for func in function_calls]

    # Join the names with ' | ' as separator
    formatted_names = ' | '.join(function_names)

    return formatted_names


def generate_enum_rule(enum_rule_name, enum_values):
    # Start the enum rule with its name
    enum_rule = f"{enum_rule_name} ::= "
    # Add each enum value
    for i, value in enumerate(enum_values):
        if i > 0:
            enum_rule += " | "  # Add a separator for multiple values
        enum_rule += f'\"\\"{value}\\\""'
    return enum_rule


def generate_object_rule(nested_rule_name, structure):
    object_rule = f"{format_rule_name(nested_rule_name)} ::= \"{{\" ws "
    for j, (sub_param_name, sub_param) in enumerate(structure.items()):
        if j > 0:
            object_rule += "\",\" ws "  # Include a comma separator for multiple sub-parameters

        if sub_param.type in [DataType.OBJECT, DataType.ARRAY]:
            # Recursive call for nested OBJECT or ARRAY
            sub_nested_rule_name = f"{format_rule_name(nested_rule_name)}-{format_rule_name(sub_param_name)}"
            object_rule += f"\"\\\"{sub_param_name}\\\":\" ws {sub_nested_rule_name} "
            if sub_param.type == DataType.OBJECT:
                sub_object_rule = generate_object_rule(sub_nested_rule_name, sub_param.structure)
                object_rule += "\n" + sub_object_rule
            elif sub_param.type == DataType.ARRAY:
                sub_array_rule = generate_array_rule(sub_nested_rule_name, sub_param.element_type)
                object_rule += "\n" + sub_array_rule
        elif sub_param.type == DataType.FLOAT and sub_param.precision is not None:
            # Handling FLOAT type with precision in nested object
            float_rule_name = f"float-{sub_param.precision}"
            object_rule += f"\"\\\"{sub_param_name}\\\":\" ws {float_rule_name} "
        else:
            # Basic data types or ENUM for nested parameters
            formatted_type = format_data_type(sub_param.type,
                                              nested_rule_name=f"{nested_rule_name}{sub_param_name.capitalize()}",
                                              precision=sub_param.precision)
            object_rule += f"\"\\\"{sub_param_name}\\\":\" ws {formatted_type}"

    object_rule += " ws \"}\""
    return object_rule


def generate_array_rule(nested_rule_name, element_type):
    array_rule = f"{nested_rule_name} ::= \"[\" ws "
    if element_type.type in [DataType.OBJECT, DataType.ARRAY]:
        # Recursive call for nested OBJECT or ARRAY in an array
        array_element_rule_name = f"{nested_rule_name}-element"
        array_rule += f"{array_element_rule_name} (\",\" ws {array_element_rule_name})* "
        if element_type.type == DataType.OBJECT:
            array_object_rule = generate_object_rule(array_element_rule_name, element_type.structure)
            array_rule += "\n" + array_object_rule
        elif element_type.type == DataType.ARRAY:
            array_array_rule = generate_array_rule(array_element_rule_name, element_type.element_type)
            array_rule += "\n" + array_array_rule
    else:
        # Basic data types for array elements
        array_rule += element_type.type.value + '("," ws ' + element_type.type.value + ')*'

    array_rule += " ws \"]\""
    return array_rule


def format_enum_values(enum_values):
    """Format enum values for GBNF grammar."""
    return ' | '.join(f'"{value}"' for value in enum_values)


def collect_float_precisions(function_calls):
    precisions = set()
    for func in function_calls:
        for param in func.parameters.properties.values():
            if param.type in [DataType.OBJECT, DataType.ARRAY]:
                test = collect_nested_float_precisions(param)
                if test is not None:
                    precisions.add(test)
            if param.type == DataType.FLOAT and param.precision is not None:
                precisions.add(param.precision)
    return precisions


def collect_nested_float_precisions(nested):
    if nested.type == DataType.OBJECT:
        for param in nested.structure.values():
            if param.type == DataType.OBJECT:
                return collect_nested_float_precisions(param)
            if param.type == DataType.ARRAY:
                if param.element_type.type == DataType.OBJECT:
                    return collect_nested_float_precisions(param)
                if param.element_type.type == DataType.FLOAT and param.element_type.precision is not None:
                    return param.element_type.precision
            if param.type == DataType.FLOAT and param.precision is not None:
                return param.precision
    else:
        if nested.element_type.type == DataType.OBJECT:
            return collect_nested_float_precisions(nested.element_type)
        if nested.element_type.type == DataType.FLOAT and nested.element_type.precision is not None:
            return nested.element_type.precision


def format_data_type(data_type, nested_rule_name=None, precision=None):
    """Return the formatted data type or a nested rule name for complex types."""
    if data_type in [DataType.OBJECT, DataType.ARRAY]:
        return nested_rule_name if nested_rule_name else 'object'
    elif data_type == DataType.FLOAT and precision is not None:
        return f"float-{precision}"  # Custom float rule name based on precision
    else:
        return data_type.value


def generate_gbnf_float_rules(precisions):
    gbnf_rules = ""
    gbnf_rules2 = ""

    for precision in precisions:
        # Define the floating point rules with specific precision
        gbnf_rules += f"\nfloat-{precision} ::= integer-part \".\" fractional-part-{precision}\n"
        rule_part = ''.join(["[0-9]" for _ in range(precision)])
        gbnf_rules2 += f"fractional-part-{precision} ::= {rule_part}\n"
    # Define the integer_part rule only once
    gbnf_rules += "\ninteger-part ::= [0-9]+\n"
    return gbnf_rules + gbnf_rules2 + "\n"


def generate_nested_rule(nested_rule_name, param):
    """Generate rules for nested structures like OBJECT and ARRAY."""
    if param.type == DataType.OBJECT:
        return generate_object_rule(nested_rule_name, param.structure)
    elif param.type == DataType.ARRAY:
        return generate_array_rule(nested_rule_name, param.element_type)


def generate_parameter_rules(function_name, parameters):
    """Generate GBNF rules for function parameters."""
    param_rules = f"{function_name}-params ::= \"{{\" ws "

    for i, (param_name, param) in enumerate(parameters.items()):
        param_rules += "\",\" ws " if i > 0 else ""  # Add comma separator for multiple parameters
        nested_rule_name = f"{function_name}-{format_rule_name(param_name)}"
        param_rules += f"\"\\\"{format_rule_name(param_name)}\\\":\" ws "
        if param.type in [DataType.OBJECT, DataType.ARRAY]:
            param_rules += f"{nested_rule_name} "
            param_rules += "\n" + generate_nested_rule(nested_rule_name, param)
        elif param.enum:
            param_rules += f"{nested_rule_name} "
            param_rules += "\n" + generate_enum_rule(nested_rule_name, param.enum)
        else:
            param_rules += format_data_type(param.type)
    param_rules += " ws \"}\""
    return param_rules


def generate_gbnf_rule(function_call):
    """Generate a GBNF grammar rule for a given FunctionCall."""
    function_name = format_rule_name(function_call.name)
    function_rule = f"{function_name} ::= \"{{\" ws \"\\\"function\\\":\" ws \"\\\"{function_call.name}\\\",\" ws \"\\\"params\\\":\" ws {function_name}-params \"}}\""
    param_rules = generate_parameter_rules(function_name, function_call.parameters.properties)
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

    # Collect required float precisions
    float_precisions = collect_float_precisions(function_calls)

    # Generate precision-specific float rules
    float_rules = generate_gbnf_float_rules(float_precisions)
    function_rules[0] += """ ws "}" """
    # Combine all rules
    complete_grammar = "\n".join(function_rules + param_rules + [float_rules])

    return complete_grammar


def format_rule_name(name):
    """
    Convert rule names from snake_case to kebab-case and ensure 'Params' becomes 'params'.
    """
    # Replace underscores with dashes and convert to lowercase
    return name.replace('_', '-').lower()


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
        Recursively document a parameter, handling objects, arrays, and enums.
        """
        indent = "  " * indent_level

        # Handling Enum type
        if param.type == DataType.ENUM and param.enum:
            enum_values = ", ".join(param.enum[:-1]) + " or " + param.enum[-1]
            param_description = f"{param.description} (Valid values: {enum_values})"
        else:
            param_description = param.description

        doc = f"{indent}{param_name} ({param.type.value}, {'required' if param.required else 'optional'}): {param_description}\n"

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
