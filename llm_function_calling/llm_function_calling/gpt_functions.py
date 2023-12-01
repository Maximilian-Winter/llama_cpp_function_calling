from enum import Enum
from typing import List

from .function_call import DataType
from .function_calling_grammar_generator import generate_documentation, \
    save_documentation_to_file, format_rule_name, generate_enum_rule, generate_object_rule, generate_array_rule, \
    format_function_names, generate_gbnf_grammar
from .function_calling_grammar_generator import save_grammar_to_file
from .function_call import FunctionCall, FunctionParameters, FunctionParameter




# SendMessage FunctionCall
send_message = FunctionCall(
    name='send_message',
    description="Sends a message to the User.",
    parameters=FunctionParameters({
        "inner_thoughts": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                            description="Your inner thoughts or inner monologue while writing the message."),
        "message": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                     description="Message you want to send to the user.")
    })
)

# CoreMemoryAppend FunctionCall
core_memory_append = FunctionCall(
    name='core_memory_append',
    description="Append to Core Memory.",
    parameters=FunctionParameters({
        "inner_thoughts": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                            description="Your inner thoughts or inner monologue while writing the value."),
        "key": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                 description="The memory key, like 'persona', 'goals', 'situation' or 'human'."),
        "field": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                   description="The field which should be appended."),
        "value": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                   description="The information you would like to save."),
        "require_heartbeat": FunctionParameter(parameter_type=DataType.BOOLEAN, required=True,
                                               description="Set this to true to get control back after execution, to chain functions together.")
    })
)

# CoreMemoryReplace FunctionCall
core_memory_replace = FunctionCall(
    name='core_memory_replace',
    description="Replace parts of Core Memory.",
    parameters=FunctionParameters({
        "inner_thoughts": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                            description="Your inner thoughts or inner monologue while writing the value."),
        "key": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                 description="The memory key, like 'persona', 'goals', 'situation' or 'human'."),
        "field": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                   description="The field where the memory should be replaced like 'personality' or 'traits'."),
        "value": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                   description="The information you would like to write into the field."),
        "require_heartbeat": FunctionParameter(parameter_type=DataType.BOOLEAN, required=True,
                                               description="Set this to true to get control back after execution, to chain functions together.")
    })
)

# ArchivalMemoryInsert FunctionCall
archival_memory_insert = FunctionCall(
    name='archival_memory_insert',
    description="Add memory to Archival Memory.",
    parameters=FunctionParameters({
        "inner_thoughts": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                            description="Your inner thoughts or inner monologue while writing the value,"),
        "value": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                   description="The content you want to add."),
        "memory_importance": FunctionParameter(parameter_type=DataType.FLOAT, required=True,
                                               description="The importance of the current memory considering situation and persona."),
        "require_heartbeat": FunctionParameter(parameter_type=DataType.BOOLEAN, required=True,
                                               description="Set this to true to get control back after execution, to chain functions together.")
    })
)

# ArchivalMemorySearch FunctionCall
archival_memory_search = FunctionCall(
    name='archival_memory_search',
    description="Search in Archival Memory.",
    parameters=FunctionParameters({
        "inner_thoughts": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                            description="Your inner thoughts or inner monologue while writing the query."),
        "query": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                   description="Your search query."),
        "require_heartbeat": FunctionParameter(parameter_type=DataType.BOOLEAN, required=True,
                                               description="Set this to true to get control back after execution, to chain functions together.")
    })
)

# RecallMemorySearch FunctionCall
recall_memory_search = FunctionCall(
    name='recall_memory_search',
    description="Search in Recall Memory.",
    parameters=FunctionParameters({
        "inner_thoughts": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                            description="Your inner thoughts or inner monologue while writing the query."),
        "query": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                   description="Your search query."),
        "page": FunctionParameter(parameter_type=DataType.NUMBER, required=True,
                                  description="The page number you want to retrieve."),
        "start_date": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                        description="The start date for your search in '%Y-%m-%d %H:%M:%S' format."),
        "end_date": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                      description="The end date for your search in '%Y-%m-%d %H:%M:%S' format."),
        "require_heartbeat": FunctionParameter(parameter_type=DataType.BOOLEAN, required=True,
                                               description="Set this to true to get control back after execution, to chain functions together.")
    })
)

# CmdCommand FunctionCall
cmd_command = FunctionCall(
    name='cmd_command',
    description="Execute CMD command.",
    parameters=FunctionParameters({
        "inner_thoughts": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                            description="Your inner thoughts or inner monologue while writing the command."),
        "command": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                     description="The CMD command to execute."),
        "require_heartbeat": FunctionParameter(parameter_type=DataType.BOOLEAN, required=True,
                                               description="Set this to true to get control back after execution, to chain functions together.")
    })
)

# WebBrowsing FunctionCall
web_browsing = FunctionCall(
    name='web_browsing',
    description="Opens a website and returns content.",
    parameters=FunctionParameters({
        "inner_thoughts": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                            description="Your inner thoughts or inner monologue while writing the url."),
        "URL": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                 description="The URL you want to access."),
        "require_heartbeat": FunctionParameter(parameter_type=DataType.BOOLEAN, required=True,
                                               description="Set this to true to get control back after execution, to chain functions together.")
    })
)

# WebDownload FunctionCall
web_download = FunctionCall(
    name='web_download',
    description="Downloads a file.",
    parameters=FunctionParameters({
        "inner_thoughts": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                            description="Your inner thoughts or inner monologue while writing the url."),
        "URL": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                 description="The URL you want to download."),
        "Path": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                  description="The Path you want to download the file to."),
        "require_heartbeat": FunctionParameter(parameter_type=DataType.BOOLEAN, required=True,
                                               description="Set this to true to get control back after execution, to chain functions together.")
    })
)

# ReadFile FunctionCall
read_file = FunctionCall(
    name='read_file',
    description="Returns content of a file.",
    parameters=FunctionParameters({
        "inner_thoughts": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                            description="Your inner thoughts or inner monologue while writing the file path."),
        "File": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                  description="The path of the file you want to open."),
        "require_heartbeat": FunctionParameter(parameter_type=DataType.BOOLEAN, required=True,
                                               description="Set this to true to get control back after execution, to chain functions together.")
    })
)

# WriteFile FunctionCall
write_file = FunctionCall(
    name='write_file',
    description="Writes to a file.",
    parameters=FunctionParameters({
        "inner_thoughts": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                            description="Your inner thoughts or inner monologue while writing the file."),
        "File": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                  description="The path of the file you want to write."),
        "Content": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                     description="The content of the file you want to write."),
        "require_heartbeat": FunctionParameter(parameter_type=DataType.BOOLEAN, required=True,
                                               description="Set this to true to get control back after execution, to chain functions together.")
    })
)

# PythonInterpreterCommand FunctionCall
python_interpreter_command = FunctionCall(
    name='python_interpreter_command',
    description="Execute Python command.",
    parameters=FunctionParameters({
        "inner_thoughts": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                            description="Your inner thoughts or inner monologue while writing the command."),
        "command": FunctionParameter(parameter_type=DataType.STRING, required=True,
                                     description="The Python command to execute."),
        "require_heartbeat": FunctionParameter(parameter_type=DataType.BOOLEAN, required=True,
                                               description="Set this to true to get control back after execution, to chain functions together.")
    })
)


def generate_gpt_functions_grammar_and_documentation():
    # List of FunctionCall instances
    # function_calls = [send_message, core_memory_append, core_memory_replace, archival_memory_insert,
    #                   archival_memory_search, cmd_command, web_browsing, web_download, read_file,
    #                   write_file, python_interpreter_command]

    # Enum values for a hypothetical "role" parameter
    roles_enum = ["Admin", "User", "Guest"]

    # Nested structure for address parameter
    address_structure = {
        "street": FunctionParameter(DataType.STRING, True),
        "city": FunctionParameter(DataType.STRING, True),
        "zip_code": FunctionParameter(DataType.STRING, True)
    }

    # Parameters for the CreateUserProfile function
    create_user_profile_params = FunctionParameters({
        "username": FunctionParameter(DataType.STRING, True),
        "email": FunctionParameter(DataType.STRING, True),
        "address": FunctionParameter(DataType.OBJECT, True, structure=address_structure),
        "is_active": FunctionParameter(DataType.BOOLEAN, True),
        "role": FunctionParameter(DataType.ENUM, True, enum=roles_enum)
    })

    # Enum for processing options
    processing_options_enum = ["Standard", "Extended", "Custom"]

    # Nested structure for experiment instrumentation
    instrumentation_structure = {
        "type": FunctionParameter(DataType.STRING, True),
        "model": FunctionParameter(DataType.STRING, True)
    }

    # Nested structure for experiment details
    experiment_details_structure = {
        "title": FunctionParameter(DataType.STRING, True),
        "researcher": FunctionParameter(DataType.STRING, True),
        "date": FunctionParameter(DataType.STRING, True),
        "instrumentation": FunctionParameter(DataType.OBJECT, True, structure=instrumentation_structure)
    }

    # Sample measurements structure (array of floats)
    sample_structure = {
        "sampleId": FunctionParameter(DataType.STRING, True),
        "measurements": FunctionParameter(DataType.ARRAY, True, element_type=FunctionParameter(DataType.FLOAT, precision=5, required=True))
    }

    # Parameters for AnalyzeScientificData function
    analyze_scientific_data_params = FunctionParameters({
        "experiment_details": FunctionParameter(DataType.OBJECT, True, structure=experiment_details_structure),
        "samples": FunctionParameter(DataType.ARRAY, True,
                                     element_type=FunctionParameter(DataType.OBJECT, True, structure=sample_structure)),
        "processing-options": FunctionParameter(DataType.ENUM, True, enum=processing_options_enum)
    })

    # Create the FunctionCall instance
    analyze_scientific_data_function_call = FunctionCall("analyze_scientific_data",
                                                         "Process scientific data from experiments",
                                                         analyze_scientific_data_params)

    # Create the FunctionCall instance
    create_user_profile_function_call = FunctionCall("create_user_profile", "Create a user profile",
                                                     create_user_profile_params)


    function_calls = [send_message, core_memory_append, core_memory_replace, archival_memory_insert,
                      archival_memory_search, recall_memory_search]
    function_calls = [analyze_scientific_data_function_call]
    # Generate the documentation
    doc = generate_documentation(function_calls)
    print(doc)
    save_documentation_to_file(doc, 'function_documentation.txt')

    save_grammar_to_file(generate_gbnf_grammar(function_calls), "gen_function_calling.gbnf")


class Address:
    def __init__(self, street, city, zip_code):
        self.street = street
        self.city = city
        self.zip_code = zip_code


class UserProfile:
    def __init__(self, username, email, address: Address, is_active):
        self.username = username
        self.email = email
        self.address = address
        self.is_active = is_active


# Define an Enum for item categories
class ItemCategory(Enum):
    ELECTRONICS = "Electronics"
    CLOTHING = "Clothing"
    FOOD = "Food"
    BOOKS = "Books"


# Updated OrderItem class with an additional category attribute
class OrderItem:
    def __init__(self, item_id, quantity, category: ItemCategory):
        self.item_id = item_id
        self.quantity = quantity
        self.category = category


# Define the structure for an OrderItem in GBNF with the category enum
order_item_structure = {
    "item_id": FunctionParameter(DataType.STRING, True, "Unique identifier for the item"),
    "quantity": FunctionParameter(DataType.NUMBER, True, "Number of items to order"),
    # Adding the category as an Enum type
    "category": FunctionParameter(DataType.ENUM, True, "Category of the item",
                                  enum=[e.value for e in ItemCategory])
}


class Order:
    def __init__(self, user_id, items: [OrderItem]):
        self.user_id = user_id
        self.items = items


# Define the structure for an Address in GBNF
address_structure = {
    "street": FunctionParameter(DataType.STRING, True, "Street name and number"),
    "city": FunctionParameter(DataType.STRING, True, "City name"),
    "zip_code": FunctionParameter(DataType.STRING, True, "Postal or ZIP code")
}

# Define the structure for a UserProfile in GBNF
user_profile_params = FunctionParameters({
    "username": FunctionParameter(DataType.STRING, True, "User's unique username"),
    "email": FunctionParameter(DataType.STRING, True, "User's email address"),
    "address": FunctionParameter(DataType.OBJECT, True, "User's physical address", structure=address_structure),
    "is_active": FunctionParameter(DataType.BOOLEAN, True, "Indicates if the user profile is active")
})

# Create FunctionCall instance for creating a user profile
create_user_profile = FunctionCall("create_user_profile",
                                   "Create a new user profile with username, email, address, and activity status",
                                   user_profile_params)

# Define the structure for an Order in GBNF
order_params = FunctionParameters({
    "user_id": FunctionParameter(DataType.STRING, True, "Identifier of the user placing the order"),
    "items": FunctionParameter(DataType.ARRAY, True, "List of items to be included in the order",
                               element_type=FunctionParameter(DataType.OBJECT, True, structure=order_item_structure))
})

# Create FunctionCall instance for creating an order
create_order = FunctionCall("create_order",
                            "Create a new order for a user, including a list of items and quantities",
                            order_params)
