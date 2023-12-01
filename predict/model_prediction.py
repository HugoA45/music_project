import torch
import torch.nn as nn
import torch.nn.functional as F

def prediction(data, model, task='composer_classification'):

    res = model.forward(torch.from_numpy(data))

    if task == 'composer_classification':

        composer_names = ['M', 'C', 'E','H','W','J','S','Y']

        model.classifier = nn.Linear(model.hidden_size, len(composer_names))
        logits = model.classifier(res.last_hidden_state)
        probs = F.softmax(logits, dim=-1)
        avg_probs = torch.mean(probs, dim=1)
        _, predicted_class = torch.max(avg_probs, 1)
        predicted_composers = [composer_names[idx.item()] for idx in predicted_class]

        return predicted_composers
