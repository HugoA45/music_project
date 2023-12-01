import numpy as np
import subprocess
import os
import sys

def tokenize_midi(midi_dir, cp_dir):
    """
    Executes a Python script with the specified input directory and returns the content of the generated .npy file.
    Args:
    script_path (str): Path to the Python script.
    input_dir (str): Input directory to pass to the script.
    output_dir (str): Directory where the .npy file is expected to be saved.
    Returns:
    ndarray or None: The content of the .npy file as a NumPy array, or None if no file is found.
    """

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_path = os.path.join(base_dir, 'data_processing', 'preprocess.py')

    # Construct and run the command
    full_command = ["python", script_path, "--input_dir", midi_dir]
    subprocess.run(full_command, check=True)

    # Assuming the script saves a single .npy file in the output_dir
    for file in os.listdir(cp_dir):
        if file.endswith('.npy'):
            npy_path = os.path.join(cp_dir, file)
            npy_content = np.load(npy_path, allow_pickle=True)
            return npy_content
    # If no .npy file is found
    return None

# # Determine the base directory of the project
# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # Construct paths relative to the base directory
# script_path = os.path.join(base_dir, 'data_processing', 'main.py')
# input_dir = os.path.join(base_dir, 'Output_Dir')
# output_dir = os.path.join(base_dir, 'data', 'CP_data', 'tmp')
# # Execute the function
# npy_content = tokenize_midi(script_path, input_dir, output_dir)
# if npy_content is not None:
#     print("Script executed successfully and .npy file content obtained.")
# else:
#     print("No .npy file was found in the output directory.")
