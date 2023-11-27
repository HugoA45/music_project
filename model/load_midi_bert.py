from transformers import BertConfig
from MidiBERT.model import MidiBert
import pickle
import torch

def load_model(checkpoint_path):
    print("Loading Dictionary")
    with open('data_creation/prepare_data/dict/CP.pkl', 'rb') as f:
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

    # Load the checkpoint
    checkpoint = torch.load(checkpoint_path, map_location='cpu')

    # Remove the unexpected key from the state dictionary
    if "bert.embeddings.position_ids" in checkpoint['state_dict']:
        del checkpoint['state_dict']["bert.embeddings.position_ids"]

    # Load the state dictionary from the checkpoint into the model
    midibert.load_state_dict(checkpoint['state_dict'])
    model = midibert.bert.from_pretrained('bert-base-uncased')
    num_parameters = sum(p.numel() for p in model.parameters())

    print(f'The model has {num_parameters} parameters.')
    return model

# Example usage:
# model = load_model('/mnt/c/Users/Hugo Amaro/Desktop/bootcamp/project/MIDI_BERT/result/pretrain_model.ckpt')
