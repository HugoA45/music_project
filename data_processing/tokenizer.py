import subprocess

def run_python_script(script_path, input_dir):
    """
    Executes a Python script with the specified input directory.

    Args:
    script_path (str): Path to the Python script.
    input_dir (str): Input directory to pass to the script.

    Returns:
    int: The return code of the script execution. 0 indicates success.
    """
    # Define the command and arguments
    command = "python3"

    # Construct the full command
    full_command = [command, script_path, "--input_dir", input_dir]

    # Run the command
    process = subprocess.run(full_command, check=True)

    # Return the return code
    return process.returncode

# Example usage
script_path = '/path/to/data_processing/main.py'  # Replace with your actual script path
input_dir = '/path/to/output/dir'  # Replace with your actual input directory

return_code = run_python_script(script_path, input_dir)
if return_code == 0:
    print("Script executed successfully.")
else:
    print(f"Script returned an error. Return code: {return_code}")
