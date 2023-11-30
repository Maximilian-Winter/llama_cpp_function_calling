from .function_call import DataType
from .function_calling_grammar_generator import generate_gbnf_grammar, generate_documentation, save_documentation_to_file
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
    name='core_memory_Append',
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
    function_calls = [send_message, core_memory_append, core_memory_replace, archival_memory_insert,
                      archival_memory_search, cmd_command, web_browsing, web_download, read_file,
                      write_file, python_interpreter_command]

    # Generate the documentation
    doc = generate_documentation(function_calls)
    print(doc)
    save_documentation_to_file(doc, 'function_documentation.txt')
    function_calls = [send_message, core_memory_append, core_memory_replace, archival_memory_insert,
                      archival_memory_search,
                      cmd_command, web_browsing, web_download, read_file, write_file, python_interpreter_command]
    save_grammar_to_file(generate_gbnf_grammar(function_calls), "gen_function_calling.gbnf")
