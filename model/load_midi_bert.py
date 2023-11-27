from transformers import BertConfig
from model import MidiBert
import pickle
import torch
import sys

sys.path.insert(0, '.')

def load_model():

    print("Loading Dictionary")
    with open('/root/code/HugoA45/music_project/music_project/model/CP.pkl', 'rb') as f:
        e2w, w2e = pickle.load(f)

    # Define the configuration for the BERT model
    configuration = BertConfig(
        max_position_embeddings=512,
        position_embedding_type='relative_key_query',
        hidden_size=768,
        num_attention_heads=12,
        num_hidden_layers=12
    )

    # Initialize the model
    midibert = MidiBert(bertConfig=configuration, e2w=e2w, w2e=w2e)

    # Define the path to your checkpoint here
    ckpt_path = '/root/code/HugoA45/music_project/music_project/model/pretrain_model.ckpt'

    # Load the checkpoint
    checkpoint = torch.load(ckpt_path, map_location='cpu')


    # Remove the unexpected key from the state dictionary
    if "bert.embeddings.position_ids" in checkpoint['state_dict']:
        del checkpoint['state_dict']["bert.embeddings.position_ids"]

    # Load the state dictionary from the checkpoint into the model
    midibert.load_state_dict(checkpoint['state_dict'])


    return midibert.bert

model = load_model()

print(model)
