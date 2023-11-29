from transformers import BertConfig
from model.model import MidiBert
import pickle
import torch

def load_model(dict_path, ckpt_path):

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
    checkpoint = load_checkpoint(ckpt_path)

    # Remove embeddings.position_ids from the state dictionary
    # and save it in case it is necessary
    if "bert.embeddings.position_ids" in checkpoint['state_dict']:
        embeddings_position_ids =  checkpoint['state_dict']["bert.embeddings.position_ids"]
        del checkpoint['state_dict']["bert.embeddings.position_ids"]

    # Load the state dictionary from the checkpoint into the model
    midibert.load_state_dict(checkpoint['state_dict'])
    midibert.eval()

    return midibert

def load_checkpoint(ckpt_path):

    checkpoint = torch.load(ckpt_path, map_location='cpu')

    return checkpoint
