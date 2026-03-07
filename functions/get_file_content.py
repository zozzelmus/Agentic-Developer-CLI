import config
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of a file considering a maximum size",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to return content from, relative to the working directory (default is the working directory itself)",
            ),
        },
    )
)

def get_file_content(working_directory, file_path):
    import os 
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not os.path.isfile(target_file):
            raise ValueError(f'Error: File "{target_file}" is not a file')
        if not os.path.exists(target_file):
            raise ValueError(f'Error: File "{target_file}" does not exist')
        if not valid_target_file:
            raise ValueError(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

        with open(target_file, 'r') as f:
            content = f.read(config.MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'
        
        return f"Content of '{file_path}': '{content}'"
    except Exception as e:
        return f'Content of "{file_path}":\n    Error: {str(e)}'