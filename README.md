### llama.cpp Grammar Generator for LLM Function Calls

#### Overview
This system is designed for generating grammars and documentation for structured function calls in GGML BNF (GGML Backus-Naur Form), tailored for Large Language Models (LLMs) used with llama.cpp . It allows LLMs to understand and execute function calls in a syntactically correct and semantically meaningful manner.

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

#### Usage
1. **Defining Function Calls**: Create `FunctionCall` instances for each function you want the LLM to call, defining parameters using `FunctionParameter` and `FunctionParameters`.
   
2. **Generating GGML BNF Grammar**: Use `generate_gbnf_grammar` to create GGML BNF grammar rules for these function calls, formatted for LLMs.
   
3. **Generating Documentation**: Use `generate_documentation` to produce human-readable documentation for these function calls.

#### Example
Define a function call like `send_message`:
```python
send_message = FunctionCall(
    name='send_message',
    parameters=FunctionParameters({
        "message": FunctionParameter(parameter_type="string", required=True,
                                     description="Message you want to send.")
    })
)
```
Then generate its GGML BNF grammar and documentation:
```python
generate_gbnf_grammar([send_message])
generate_documentation([send_message])
```
You can find a complete example in `gpt_functions.py`
#### File Saving
- Use `save_grammar_to_file` to save the generated GGML BNF grammar.
- Use `save_documentation_to_file` to save the documentation.