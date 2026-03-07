from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file reletive to the working directory, providing stdout, stderr outputs from the script",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to execute the script from, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="The list of additional arguements to pass into the python script which will be ran, by default the script will execute using the 'python' command passing the directory"
            )
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    import os 
    import subprocess
    try:
        working_dir_abs = os.path.abspath(working_directory)
        absolute_file_path = os.path.join(working_dir_abs, file_path)
        target_file = os.path.normpath(absolute_file_path)
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not os.path.isfile(target_file):
            raise ValueError(f'Error: "{file_path}" does not exist or is not a regular file')
        if not valid_target_file:
            raise ValueError(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not file_path.endswith('.py'):
            raise ValueError(f'Error: "{file_path}" is not a Python file')
        
        command = ["python", absolute_file_path]
        
        if args:
            command.extend(args)

        process = subprocess.run(
            args=command,
            timeout=30,
            capture_output=True,
            text=True
        )

        output = ''
        if process.returncode != 0:
            output += f'Process exited with code {process.returncode}\n'
        if not process.stderr and not process.stdout:
            output += f'No output provided\n'

        if process.stderr:
            output+= f'STDERR: {process.stderr}'
        if process.stdout:
            output+= f'STDOUT: {process.stdout}'

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"