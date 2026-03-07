from google.genai import types
from functions import get_file_content, get_files_info, write_file, run_python_file

available_functions = types.Tool(
    function_declarations=[get_files_info.schema_get_files_info,
                           get_file_content.schema_get_file_content,
                           write_file.schema_write_file,
                           run_python_file.schema_run_python_file],
)

def call_function(function_call:types.FunctionCall, working_directory, verbose=False) -> types.Content:
    function_map = {
        "get_file_content": get_file_content.get_file_content,
        "get_files_info": get_files_info.get_files_info,
        "write_files": write_file.write_file,
        "run_python_file": run_python_file.run_python_file
    }

    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_name = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    args = dict(function_call.args) if function_call.args else {}

    args['working_directory'] = working_directory

    function_result = function_map[function_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

