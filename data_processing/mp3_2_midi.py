import os
import subprocess

def convert_mp3_to_midi(mp3_path, output_dir):
    """
    Converts an MP3 file to MIDI and saves it to the specified output directory.

    Args:
    mp3_file (str): Path to the MP3 file.
    output_dir (str): Path to the directory where the MIDI file will be saved.

    Returns:
    str: Path to the converted MIDI file.
    """
    # Make sure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Construct the conversion command
    command = f'basic-pitch "{output_dir}" "{mp3_path}"'
    subprocess.run(command, shell=True)

    # Create the path for the output MIDI file
    midi_name = os.path.splitext(os.path.basename(mp3_path))[0] + '.midi'
    output_file = os.path.join(output_dir, midi_name)

    print(f"Converted {mp3_path} to MIDI in {output_dir}")

    return output_file
