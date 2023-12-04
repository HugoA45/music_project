'''
Final function for predicting the composer of a certain piece of music.
The function:
    - takes an uploaded mp3 file as input (argument)
    - transforms this mp3 to tokens devided into 'bar', 'position', 'pitch', and 'duration'
    - predicts the composer based on a finetuned classification model
'''

import os
import io
import miditoolkit

from basic_pitch_module.basic_pitch.inference import predict

from data_processing.midi2CP import CP # CP not accessed
#from data_processing.extract import main
from bert.load_midi_bert import load_model
from predict.model_prediction import prediction
import file_paths
import pickle


#dict_path = file_paths.cp_dict
#ckpt_path = file_paths.pretrain_ckpt
#cp_dir = file_paths.cp_dir

current_directory = os.path.dirname(os.path.abspath(__file__))
dict_path = os.path.join(current_directory, 'resources', 'CP.pkl')
ckpt_path = os.path.join(current_directory, 'resources', 'pretrain_model.ckpt')
input_file = os.path.join(current_directory, 'temp/test', '1.mp3')
#input_file = 'temp/test/1.mp3'

def file_selection(input_file):

    file_type = input_file[-3:]

    if file_type != 'mp3' and file_type != 'mid':
        print('Filetype incorrect')
        return

    if file_type == 'mp3':
        midi_data = predict(input_file)[1]
        midi_stream = io.BytesIO()
        midi_data.write(midi_stream)
        midi_stream.seek(0)
        midi_object = miditoolkit.midi.parser.MidiFile(file = midi_stream)

        with open(dict_path, 'rb') as f:
            e2w, w2e = pickle.load(f)

            compact_classes = ['Bar', 'Position', 'Pitch', 'Duration']
            pad_CP = [e2w[subclass][f"{subclass} <PAD>"] for subclass in compact_classes]

        CP_model = CP(dict_path)
        events, tokens = CP_model.prepare_data(midi_object, 512)

        midi_bert = load_model(dict_path, ckpt_path)

        predicted_samples = prediction(tokens, midi_bert, task='composer_classification')
        predicted_samples = predicted_samples.value_counts()/len(predicted_samples)
        return predicted_samples

    if file_type == 'mid':
        pass

    elif file_type == 'mid':
        midi_object = input_file

file_selection(input_file)
