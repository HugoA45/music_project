import os
import glob
import subprocess

# Directory containing MP3 files
input_dir = '/Users/tobiaslandgraf/code/HugoA45/music_project/music_project/MP3_Files_Input'

# Output directory for MIDI files
output_dir = '/Users/tobiaslandgraf/code/HugoA45/music_project/music_project/Output_Dir'

# Find all MP3 files in the input directory
mp3_files = glob.glob(os.path.join(input_dir, '*.mp3'))

for mp3_file in mp3_files:
    # Construct and run the conversion command with quotes around file paths
    # Note: 'basic-pitch' is provided with the output directory, not the output file path
    command = f'basic-pitch "{output_dir}" "{mp3_file}"'
    subprocess.run(command, shell=True)

    # Assuming basic-pitch creates the MIDI file with a similar name as the MP3
    midi_name = os.path.splitext(os.path.basename(mp3_file))[0] + '.midi'
    output_file = os.path.join(output_dir, midi_name)

    print(f"Converted {mp3_file} to MIDI in {output_dir}")
