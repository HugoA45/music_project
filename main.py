import os

from bert.load_midi_bert import load_model
from data_processing.split_data import load
from predict.model_prediction import prediction
from data_processing.mp3_2_midi import convert_mp3_to_midi
from data_processing.tokenizer import tokenize_midi
import file_paths


dict_path = file_paths.cp_dict
ckpt_path = file_paths.pretrain_ckpt

def predict_composer(input_file):

    file_type = input_file[-3:]

    cp_result_dir = '/music_project/music_project/result/cp_dir'

    if file_type == 'mp3':
        midi_path = convert_mp3_to_midi(input_file)
        cp_data = tokenize_midi(midi_path, cp_result_dir)
        model = load_model(dict_path, ckpt_path)
        composer = prediction(cp_data, model)
        return composer

    if file_type == 'mid':
        cp_data = tokenize_midi(input_file, cp_result_dir)
        model = load_model(dict_path, ckpt_path)
        composer = prediction(cp_data, model)
        return composer

input_file = '/ZZ_archive/midi_dir/unts.mid'
predict_composer(input_file)
