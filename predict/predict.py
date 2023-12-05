import torch
import numpy as np
from finetune.finetune_model import SequenceClassification

def tuned_predicton(midibert, tokens, checkpoint):

    composer_names = ['Bethel Music (Religious)',
                          'Richard Clayderman',
                          'Ludovico Einaudy',
                          'Herbie Hancock',
                          'Hillsong Worship (Religious)',
                          'Joe Hisaishi (Contemporary)',
                          'Ryuichy Sakamoto (Contemporary)',
                          'Yiruma (pop)']

    classification_model = SequenceClassification(midibert, 8, 768)
    classification_model.load_state_dict(checkpoint['state_dict'])
    classification_model.eval()

    attn = torch.ones((tokens.shape[0], 512))
    y_hat = classification_model.forward(torch.from_numpy(tokens), attn, -1)

    output = np.argmax(y_hat.cpu().detach().numpy(), axis=-1)

    res = [composer_names[idx.item()] for idx in output]

    unique_values, counts = np.unique(res, return_counts=True)
    normalized_counts = counts / len(res)
    res_dict = dict(zip(unique_values, normalized_counts))
    print(res_dict)

    #return res_dict
    return output
