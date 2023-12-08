import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd
import numpy as np

def prediction(data, model, task='composer_classification'):

    res = model.forward(torch.from_numpy(data))

    if task == 'composer_classification':

        composer_names = ['Bethel Music',
                          'Richard Clayderman',
                          'Ludovico Einaudy',
                          'Herbie Hancock',
                          'Hillsong Worship',
                          'Joe Hisaishi',
                          'Ryuichy Sakamoto',
                          'Yiruma']

        model.classifier = nn.Linear(model.hidden_size, len(composer_names))
        logits = model.classifier(res.last_hidden_state)
        probs = F.softmax(logits, dim=-1)
        avg_probs = torch.mean(probs, dim=1)
        _, predicted_class = torch.max(avg_probs, 1)
        predicted_samples = [composer_names[idx.item()] for idx in predicted_class]
        predicted_samples = pd.Series(predicted_samples)
        predicted_samples.value_counts()/len(predicted_samples)

        #return predicted_samples


        outputs = []
        for i, etype in enumerate(model.e2w):
            print(type(res[i]))
            output = np.argmax(res[i].detach(), axis=-1)
            outputs.append(output)
        predicted_class = np.stack(outputs, axis=-1)
        #predicted_samples = [composer_names[idx.item()] for idx in predicted_class]
        #predicted_samples = pd.Series(predicted_samples)
        #predicted_samples.value_counts()/len(predicted_samples)
        return predicted_class
