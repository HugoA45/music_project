from model.load_midi_bert import load_model
from data_processing.load_data import load
from predict.model_prediction import prediction

data = load(task = 'composer')

dict_path = '/root/code/HugoA45/music_project/music_project/model/CP.pkl'
ckpt_path = '/root/code/HugoA45/music_project/music_project/model/pretrain_model.ckpt'

midibert = load_model(dict_path, ckpt_path)

predicted_composers = prediction(data['X_test'][0:11,0:100,:], midibert, task='composer_classification')



print(predicted_composers)
