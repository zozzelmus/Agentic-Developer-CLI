from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    import os 
    try:

        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not os.path.isdir(target_dir):
            raise ValueError(f'Error: Directory "{target_dir}" is not a directory')
        if not os.path.exists(target_dir):
            raise ValueError(f'Error: Directory "{target_dir}" does not exist')
        if not valid_target_dir:
            raise ValueError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
        files_info = []
        #note this should only do the current directory
        for entry in os.scandir(target_dir):
            if entry.is_file() or entry.is_dir():
                files_info.append({
                    "name": entry.name,
                    "size": entry.stat().st_size,
                    "is_dir": entry.is_dir()
                })

        output = f'Result for "{directory}" directory: \n'
        for info in files_info:
            output += f'  - {info["name"]}: file_size={info["size"]} bytes, is_dir={info["is_dir"]}\n'
    
        return output
    except Exception as e:
        output = f'Result for "{directory}" directory: \n'
        output += f"    Error: {str(e)}"
        return output
