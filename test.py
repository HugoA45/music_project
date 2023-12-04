import file_paths
from basic_pitch_module.basic_pitch.inference import predict
from data_processing.midi2CP import CP
import pickle
import miditoolkit
import io


midi_data = predict('temp/test/1.mp3')[1]

midi_stream = io.BytesIO()
midi_data.write(midi_stream)
midi_stream.seek(0)
midi_data = miditoolkit.midi.parser.MidiFile(file = midi_stream)


#ith open(file_paths.cp_dict, 'rb') as f:
with open('/Users/d.haverkort/code/HugoA45/music_project/music_project/resources/CP.pkl', 'rb') as f:
    e2w, w2e = pickle.load(f)

    compact_classes = ['Bar', 'Position', 'Pitch', 'Duration']
    pad_CP = [e2w[subclass][f"{subclass} <PAD>"] for subclass in compact_classes]

    # preprocess input file
    CP_model = CP('/Users/d.haverkort/code/HugoA45/music_project/music_project/resources/CP.pkl')
    events, tokens = CP_model.prepare_data(midi_data, 512)
