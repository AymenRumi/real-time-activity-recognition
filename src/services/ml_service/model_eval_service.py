import torch
import torch.nn.functional as F

from src.constants import index_mapping


def logits_to_probabilities(logits):
    probabilities = F.softmax(logits, dim=1)
    return probabilities


def logit_to_activity(logits):
    return index_mapping[torch.argmax(logits_to_probabilities(logits)).item()]
