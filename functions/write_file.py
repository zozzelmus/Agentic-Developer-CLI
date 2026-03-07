from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a given file in the context of the working directory given a file path and the context to write to the file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to write the file to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The raw context to write to the file"
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    import os 
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if os.path.exists(target_file) and os.path.isdir(target_file):
            raise ValueError(f'Error: Target "{target_file}" is a directory')
        if not valid_target_file:
            raise ValueError(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')

        # make sure all parent directories exist
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, 'w') as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: writing to "{file_path}": {str(e)}'