### llama.cpp Grammar Generator for LLM Function Calls

#### Overview
This package is designed for generating grammars and documentation for structured function calls in GGML BNF (GGML Backus-Naur Form), tailored for Large Language Models (LLMs) used with llama.cpp. The documentation is designed to explain the functions to the LLM. The `LLMFunctionCaller` is for dynamic function execution based on JSON inputs generated through the grammar generated.

At the moment it supports the following types as function parameters:

- `object`
- `array`
- `string`
- `boolean`
- `number`
- `float`

#### Components
`function_call.py`:
- `FunctionParameter`: Class to define a parameter of a function, including type, requirement status, description, and enumeration values if applicable.
- `FunctionParameters`: Class to encapsulate multiple `FunctionParameter` instances.
- `FunctionCall`: Class representing a function call, including its name and parameters.

`function_calling_grammar_generator.py`:
- `format_function_names`, `generate_gbnf_grammar`, `generate_gbnf_rule`, `capitalize_rule_name`: Functions to generate GGML BNF grammar based on the defined functions.
- `generate_documentation`, `save_documentation_to_file`: Functions to generate and save documentation for the function calls.
- `save_grammar_to_file`: Function to save the generated GGML BNF grammar to a file.

`gpt_functions.py`:
Example usage showing generating `MemGPT` like functions.

`llm_function_caller.py`:
- Dynamically executes functions based on JSON input generated through the grammar generated.
- Supports adding new functions and parameter transformers at runtime.
- Incorporates robust error handling and logging.

#### Usage
1. **Defining Function Calls**: Create `FunctionCall` instances for each function you want the LLM to call, defining parameters using `FunctionParameter` and `FunctionParameters`.
2. **Generating GGML BNF Grammar**: Use `generate_gbnf_grammar` to create GGML BNF grammar rules for these function calls, for use with llama.cpp.
3. **Generating Documentation**: Use `generate_documentation` to produce human-readable documentation for these function calls.
4. **Generate Function Call with LLM**: Use llama.cpp to generate a JSON function call with the grammar.
5. **Executing Function Calls with LLMFunctionCaller**: Use the `LLMFunctionCaller` to execute these defined function calls dynamically.

#### LLMFunctionCaller Methods
- `add_function(name, function)`: Adds a function to the executor.
- `add_param_transformer(function_name, transformer)`: Adds a parameter transformer for a specific function.
- `execute_function(json_input)`: Executes a function based on JSON input generated through the grammar generated.

#### Example for LLMFunctionCaller
```python
function_caller = LLMFunctionCaller()
function_caller.add_function("sample_function", sample_function)
function_caller.add_param_transformer("sample_function", example_transformer)
json_input = '{"function":"sample_function","params":{"arg1": "hello", "arg2": "world"}}'
result = function_caller.execute_function(json_input)
print(result)
```

#### File Saving
- Use `save_grammar_to_file` to save the generated GGML BNF grammar.
- Use `save_documentation_to_file` to save the documentation.

### Example output using OpenHermes and the example functions in `gpt_functions.py` converted to a grammar


````text
>Can you write a long poem about the USA in the "HelloUSA.txt" file?
<|im_start|>system
Available Functions:

send_message:
  Description:Sends a message to the User.
  Parameters:
    inner_thoughts (string, required): Your inner thoughts or inner monologue while writing the message.
    message (string, required): Message you want to send to the user.

read_file:
  Description:Returns content of a file.
  Parameters:
    inner_thoughts (string, required): Your inner thoughts or inner monologue while writing the file path.
    File (string, required): The path of the file you want to open.
    require_heartbeat (boolean, required): Set this to true to get control back after execution, to chain functions together.

write_file:
  Description:Writes to a file.
  Parameters:
    inner_thoughts (string, required): Your inner thoughts or inner monologue while writing the file.
    File (string, required): The path of the file you want to write.
    Content (string, required): The content of the file you want to write.
    require_heartbeat (boolean, required): Set this to true to get control back after execution, to chain functions together.

python_interpreter_command:
  Description:Execute Python command.
  Parameters:
    inner_thoughts (string, required): Your inner thoughts or inner monologue while writing the command.
    command (string, required): The Python command to execute.
    require_heartbeat (boolean, required): Set this to true to get control back after execution, to chain functions together.<|im_end|>
<|im_start|>user
Maximilian: "Can you write a long poem about the USA in the "HelloUSA.txt" file?" <|im_end|>
<|im_start|>assistant
Llama.generate: prefix-match hit
{"function":"write_file","params":{"inner_thoughts":"I'm thinking about composing a poem on the United States and saving it as 'HelloUSA.txt'.","File":"HelloUSA.txt","Content":"In search of liberty, they came from far and wide,\nA melting pot of cultures, a land so grand and vast.\nFrom coast to coast, through mountains high and tide,\nTheir dreams intertwined, their stories merged at last.\n\nBoldly they ventured, brave and free,\nSeeking opportunity, hope, and solace too,\nWith unity and strength, they forged a nation strong,\nAnd freedom's light would forever shine anew.\n\nThrough strife and struggle, battles fierce and fight,\nThey built a home where all could find their place,\nWhere justice reigns, and rights are right,\nAnd every soul can carve its own unique grace.\n\nUnited we stand, with colors bold,\nRed, white, and blue our flag unfurls,\nTogether now, our future told,\nOf unity, not division, evermore.\n\nThis land of dreams, where destiny unfolds,\nA beacon bright, a shining star that guides,\nA story written by hearts of gold,\nAcross these lands, across these tides.","require_heartbeat":true}}
````