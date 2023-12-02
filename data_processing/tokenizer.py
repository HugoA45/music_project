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

    #base_dir =
    #script_path = os.path.join(base_dir, 'data_processing', 'preprocess.py')
    script_path='/root/code/HugoA45/music_project/music_project/data_processing/preprocess.py'
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

# os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
