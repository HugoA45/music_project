from transformers import BertConfig
from bert.model import MidiBert
import numpy as np
import miditoolkit
import pickle
import torch
import os
import io

from basic_pitch_module.basic_pitch.inference import predict
from finetune.finetune_model import SequenceClassification
from predict.predict import tuned_predicton
from data_processing.midi2CP import CP

current_directory = os.path.dirname(os.path.abspath(__file__))
dict_path = os.path.join(current_directory, 'resources', 'CP.pkl')
music_file = os.path.join(current_directory,'temp/bethel2.mp3')

model_stage = 'fine_tuned'

def load_bert_model(dict_path):

    print("Loading Dictionary")
    with open(dict_path, 'rb') as f:
        e2w, w2e = pickle.load(f)

    # Define the configuration for the BERT model according to
    # https://github.com/wazenmai/MIDI-BERT
    configuration = BertConfig(
        max_position_embeddings=512,
        position_embedding_type='relative_key_query',
        hidden_size=768,
        num_attention_heads=12,
        num_hidden_layers=12
    )

    # Initialize the bert model
    midibert = MidiBert(bertConfig=configuration, e2w=e2w, w2e=w2e)
    return midibert

def load_checkpoint(model_stage):
    if model_stage == 'pre_trained':
        ckpt_path = os.path.join(current_directory, 'resources', 'pretrain_model.ckpt')
        checkpoint = torch.load(ckpt_path, map_location='cpu')
        return checkpoint

    if model_stage == 'fine_tuned':
        ckpt_path = os.path.join(current_directory, 'resources', 'composer_best.ckpt')
        checkpoint = torch.load(ckpt_path, map_location='cpu')
        return checkpoint

def load_mp3(mp3_file_path):
    midi_data = predict(mp3_file_path)[1]
    midi_stream = io.BytesIO()
    midi_data.write(midi_stream)
    midi_stream.seek(0)
    midi_object = miditoolkit.midi.parser.MidiFile(file = midi_stream)
    return midi_object

def main(music_file, model_stage):
    midi_object = load_mp3(music_file)

    CP_model = CP(dict_path)
    events, tokens = CP_model.prepare_data(midi_object, 512)

    midibert = load_bert_model(dict_path)

    checkpoint = load_checkpoint(model_stage)

    if "midibert.bert.embeddings.position_ids" in checkpoint['state_dict']:
        del checkpoint['state_dict']["midibert.bert.embeddings.position_ids"]

    output = tuned_predicton(midibert, tokens, checkpoint)

    return output

#main(music_file, model_stage)
