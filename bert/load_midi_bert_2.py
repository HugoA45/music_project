from finetune.finetune_model import SequenceClassification
from transformers import BertConfig
from bert.model import MidiBert
import numpy as np
import miditoolkit
import pickle
import torch
import os
import io

from basic_pitch_module.basic_pitch.inference import predict
from predict.model_prediction import prediction
from data_processing.midi2CP import CP

batch_size = 12
num_workers = 5
index_layer = -1
lr = 2e-5
class_num = 8
hs = 768
cpu = False
cuda_devices = [0]
seq_class = True # composer, emotion, False = velocity, melody
task = 'composer'
epochs = 10

current_directory = os.path.dirname(os.path.abspath(__file__))
dict_path = os.path.join(current_directory, 'resources', 'CP.pkl')

def load_model(dict_path, model_stage = 'pre_trained'):

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

    # Initialize the model
    midibert = MidiBert(bertConfig=configuration, e2w=e2w, w2e=w2e)

    #load the checkpoint
    checkpoint = load_checkpoint(model_stage)
    if "bert.embeddings.position_ids" in checkpoint['state_dict']:
        embeddings_position_ids =  checkpoint['state_dict']["bert.embeddings.position_ids"]
        del checkpoint['state_dict']["bert.embeddings.position_ids"]
    midibert.load_state_dict(checkpoint['state_dict'])
    midibert.eval()

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

#Loading the mp3 file on to variable
midi_data = predict('/temp/test/1.mp3')[1]
midi_stream = io.BytesIO()
midi_data.write(midi_stream)
midi_stream.seek(0)
midi_object = miditoolkit.midi.parser.MidiFile(file = midi_stream)

CP_model = CP(dict_path)
events, tokens = CP_model.prepare_data(midi_object, 512)

midibert = load_model(dict_path, model_stage='fine_tuned')

checkpoint = load_checkpoint('fine_tuned')

if "midibert.bert.embeddings.position_ids" in checkpoint['state_dict']:
    del checkpoint['state_dict']["midibert.bert.embeddings.position_ids"]

model = SequenceClassification(midibert, 8, 768)

model.load_state_dict(checkpoint['state_dict'])
model.eval()

attn = torch.ones((tokens.shape[0], 512))
y_hat = model.forward(torch.from_numpy(tokens), attn, -1)

output = np.argmax(y_hat.cpu().detach().numpy(), axis=-1)
output
